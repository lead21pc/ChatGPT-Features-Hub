import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from openai import OpenAI
from streamlit.testing.v1 import AppTest

import app
import test_app


class T3Tests(unittest.TestCase):
    ui_context = test_app.Stage2Tests.ui_context

    def setUp(self):
        self.config = {"openai_api_key": "test-key", "model": "gpt-5.6-sol"}
        self.payloads = []
        self.paths = (app.HUB_CI_PATH, app.HUB_ROUTER_PATH,
                      app.HUB_ARCHITECTURE_PATH, app.HUB_CATALOG_PATH)
        self.record = {
            "task_scope": "Kiểm tra nguyên nhân máy khựng.",
            "selected_packages": [{
                "package_id": "HUB-PKG-TECHNICAL",
                "entrypoint_module_id": "HUB-DOM-TECHNICAL",
                "runtime_role": "REASONING_PROFILE",
                "application_scope": "Chẩn đoán nguyên nhân.",
                "reason": "Cần phân biệt các giả thuyết cạnh tranh.",
            }],
            "unresolved_blockers": [],
        }
        self.body = {
            "id": "resp_t3", "object": "response", "created_at": 0,
            "status": "completed", "model": self.config["model"],
            "output": [{"id": "msg_t3", "type": "message", "role": "assistant",
                        "status": "completed", "content": [{"type": "output_text",
                        "text": json.dumps(self.record), "annotations": []}]}],
        }

    def client(self, **kwargs):
        self.assertEqual(kwargs["max_retries"], 0)
        self.assertEqual(kwargs["base_url"], "https://api.openai.com/v1")

        def respond(request):
            self.payloads.append(json.loads(request.content))
            return httpx.Response(200, json=self.body)
        return OpenAI(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(respond)))

    def test_exact_controls_payload_schema_and_no_package_reads(self):
        controls = [path.read_bytes() for path in self.paths]
        reads = []

        def read_bytes(path):
            reads.append(path)
            self.assertIn(path, self.paths, "T3 phải chỉ đọc bốn control")
            return controls[self.paths.index(path)]

        with patch.object(Path, "read_bytes", read_bytes), patch.object(app, "OpenAI", self.client):
            for turn in range(2):
                prompt = f"Yêu cầu {turn}"
                self.assertEqual(app.inspect_route(self.config, prompt), self.record)
                payload = self.payloads[-1]
                self.assertEqual(set(payload), {"model", "input", "instructions", "text", "store"})
                self.assertEqual(payload["model"], self.config["model"])
                self.assertIs(payload["store"], False)
                self.assertEqual(payload["input"], [{"role": "user", "content": prompt}])
                self.assertEqual(payload["instructions"].encode("utf-8"),
                                 b"\n\n".join(controls + [app.T3_SIMULATION_ADAPTER.encode("utf-8")]))
                self.assertEqual(payload["text"]["format"], {
                    "type": "json_schema", "name": "hub_route_inspection",
                    "schema": app.ROUTE_SCHEMA, "strict": True,
                })
                controls = [b"\xef\xbb\xbfupdated\r\n" + body for body in controls]
        self.assertEqual(reads, list(self.paths) * 2)

    def test_all_control_failures_before_client_without_fallback(self):
        original = Path.read_bytes
        for target in self.paths:
            for error in (FileNotFoundError(), PermissionError(), OSError(),
                          UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid")):
                def read_bytes(path):
                    if path == target:
                        raise error
                    return original(path)
                with self.subTest(target=target.name, error=type(error).__name__), \
                     patch.object(Path, "read_bytes", read_bytes), \
                     patch.object(app, "OpenAI") as client, patch.object(app, "call_model") as normal:
                    with self.assertRaisesRegex(ValueError, "T3:.*" + target.name):
                        app.inspect_route(self.config, "Kiểm tra")
                    client.assert_not_called()
                    normal.assert_not_called()

    def invalid_responses(self):
        baseline = copy.deepcopy(self.body)
        for text in ("{", "[]", "null", "{}", json.dumps({**self.record, "extra": True}),
                     json.dumps({**self.record, "task_scope": 1}),
                     json.dumps({**self.record, "selected_packages": ["bad"]}),
                     json.dumps({**self.record, "selected_packages": [{}]}),
                     json.dumps({**self.record, "unresolved_blockers": [None]}), " "):
            body = copy.deepcopy(baseline)
            body["output"][0]["content"][0]["text"] = text
            yield body
        body = copy.deepcopy(baseline)
        body["output"][0]["content"] = [{"type": "refusal", "refusal": "Refused"}]
        yield body
        body = copy.deepcopy(baseline)
        body["status"] = "incomplete"
        body["incomplete_details"] = {"reason": "max_output_tokens"}
        yield body
        yield {**baseline, "output": []}
        yield {**baseline, "output": None}
        body = copy.deepcopy(baseline)
        body["output"][0]["content"] = None
        yield body
        body = copy.deepcopy(baseline)
        body["output"][0]["content"][0]["text"] = None
        yield body

    def test_invalid_refused_incomplete_no_text_fail_clearly(self):
        with patch.object(app, "OpenAI", self.client):
            for body in self.invalid_responses():
                self.body = body
                with self.subTest(body=body), self.assertRaisesRegex(ValueError, "T3:.*chưa lưu"):
                    app.inspect_route(self.config, "Kiểm tra")

    def test_ui_renders_record_and_none_without_polluting_normal_history(self):
        with self.ui_context(), patch("openai.OpenAI", self.client):
            ui = AppTest.from_file("app.py").run()
            ui.radio[0].set_value(app.MODES[3]).run()
            for selected in (self.record["selected_packages"], []):
                record = {**self.record, "selected_packages": selected}
                self.body["output"][0]["content"][0]["text"] = json.dumps(record)
                ui.text_area[0].set_value("Kiểm tra")
                ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertFalse(ui.error)
                self.assertEqual(json.loads(ui.json[-1].value), record)
                self.assertEqual(ui.session_state.route_records[-1]["record"], record)
                self.assertEqual(ui.session_state.messages, [])
                self.assertEqual(ui.session_state.response_modes, {})
                self.assertIn(app.MODES[3], [caption.value for caption in ui.caption])
            self.assertTrue(any("NONE" in caption.value for caption in ui.caption))
            self.body["output"][0]["content"][0]["text"] = "Đã nhận."
            ui.radio[0].set_value(app.MODES[0]).run()
            ui.text_area[0].set_value("T0")
            ui.button[0].click().run()
            self.assertFalse(ui.error)
            self.assertEqual(self.payloads[-1], {"model": self.config["model"], "store": False,
                                               "input": [{"role": "user", "content": "T0"}]})
            ui.radio[0].set_value(app.MODES[3]).run()
            self.body["output"][0]["content"][0]["text"] = json.dumps(self.record)
            history = list(ui.session_state.messages)
            ui.text_area[0].set_value("T3 mới")
            ui.button[0].click().run()
            self.assertEqual(self.payloads[-1]["input"], [{"role": "user", "content": "T3 mới"}])
            self.assertEqual(ui.session_state.messages, history)

    def test_ui_failures_keep_prior_state_and_prompt(self):
        original = Path.read_bytes
        with self.ui_context(), patch("openai.OpenAI", self.client):
            ui = AppTest.from_file("app.py").run()
            ui.radio[0].set_value(app.MODES[3]).run()
            ui.text_area[0].set_value("Thành công")
            ui.button[0].click().run()
            previous = list(ui.session_state.route_records)
            for body in self.invalid_responses():
                self.body = body
                ui.text_area[0].set_value("Giữ prompt")
                ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertIn("T3:", ui.error[0].value)
                self.assertEqual(ui.session_state.route_records, previous)
                self.assertEqual(ui.session_state.messages, [])
                self.assertEqual(ui.text_area[0].value, "Giữ prompt")
            for target in self.paths:
                for error in (FileNotFoundError(), PermissionError()):
                    def read_bytes(path):
                        if path == target:
                            raise error
                        return original(path)
                    calls = len(self.payloads)
                    with patch.object(Path, "read_bytes", read_bytes):
                        ui.button[0].click().run()
                    self.assertFalse(ui.exception)
                    self.assertIn(target.name, ui.error[0].value)
                    self.assertEqual(ui.session_state.route_records, previous)
                    self.assertEqual(ui.session_state.messages, [])
                    self.assertEqual(ui.text_area[0].value, "Giữ prompt")
                    self.assertEqual(len(self.payloads), calls)


if __name__ == "__main__":
    unittest.main()
