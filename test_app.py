import json
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from openai import OpenAI
from streamlit.testing.v1 import AppTest

import app


class Stage2Tests(unittest.TestCase):
    def setUp(self):
        self.payloads = []
        self.config = {"openai_api_key": "test-key", "model": "gpt-5.6-sol"}

    def client(self, **kwargs):
        def respond(request):
            self.payloads.append(json.loads(request.content))
            return httpx.Response(200, json={
                "id": "resp_test", "object": "response", "created_at": 0,
                "status": "completed", "model": self.config["model"],
                "output": [{"id": "msg_test", "type": "message",
                            "role": "assistant", "status": "completed",
                            "content": [{"type": "output_text", "text": "Đã nhận.",
                                         "annotations": []}]}],
            })
        return OpenAI(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(respond)))

    def test_payloads_and_history_in_all_modes(self):
        ci_bytes = app.HUB_CI_PATH.read_bytes()
        for mode in app.MODES[:3]:
            with self.subTest(mode=mode), patch.object(app, "OpenAI", self.client):
                history = []
                for prompt in ("Lượt một", "Lượt hai"):
                    messages = history + [{"role": "user", "content": prompt}]
                    answer = app.call_model(self.config, messages, mode)
                    expected = {"model": self.config["model"], "input": messages, "store": False}
                    if mode == app.MODES[1]:
                        expected["instructions"] = ci_bytes.decode("utf-8")
                        self.assertEqual(expected["instructions"].encode("utf-8"), ci_bytes)
                    elif mode == app.MODES[2]:
                        expected["instructions"] = ci_bytes.decode("utf-8") + app.T2_BINDING_BRIDGE + app.TECHNICAL_PATH.read_bytes().decode("utf-8")
                    self.assertEqual(self.payloads[-1], expected)
                    history = messages + [{"role": "assistant", "content": answer}]
                self.assertEqual([m["role"] for m in history], ["user", "assistant"] * 2)

    def test_t0_never_reads_ci(self):
        with patch.object(app, "HUB_CI_PATH") as path, patch.object(app, "TECHNICAL_PATH") as technical, patch.object(app, "OpenAI", self.client):
            app.call_model(self.config, [{"role": "user", "content": "T0"}])
            path.read_bytes.assert_not_called()
            technical.read_bytes.assert_not_called()
            self.assertNotIn("instructions", self.payloads[-1])

    def test_t1_reads_ci_on_every_request_without_normalization(self):
        with patch.object(app, "HUB_CI_PATH") as path, patch.object(app, "TECHNICAL_PATH") as technical, patch.object(app, "OpenAI", self.client):
            contents = [b"\xef\xbb\xbfCI\r\n", b"Updated CI\r\n\n"]
            path.read_bytes.side_effect = contents
            for content in contents:
                app.call_model(self.config, [], app.MODES[1])
                self.assertEqual(self.payloads[-1]["instructions"].encode("utf-8"), content)
            self.assertEqual(path.read_bytes.call_count, 2)
            technical.read_bytes.assert_not_called()

    def test_runtime_technical_is_byte_exact_active_source(self):
        source = Path("upstream/Central Hub/candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md").read_bytes()
        self.assertEqual(app.TECHNICAL_PATH.read_bytes(), source)
        self.assertIn(b"Status: ACTIVE", source)
        self.assertIn(b"Version: 1.0", source)

    def test_t2_reads_both_each_request_without_normalization(self):
        with patch.object(app, "HUB_CI_PATH") as ci, patch.object(app, "TECHNICAL_PATH") as technical, patch.object(app, "OpenAI", self.client):
            ci_contents = [b"\xef\xbb\xbfCI\r\n", b"Updated CI\n"]
            technical_contents = [b"Technical\r\n", b"\xef\xbb\xbfUpdated Technical\n\n"]
            ci.read_bytes.side_effect = ci_contents
            technical.read_bytes.side_effect = technical_contents
            for ci_body, technical_body in zip(ci_contents, technical_contents):
                app.call_model(self.config, [], app.MODES[2])
                self.assertEqual(self.payloads[-1]["instructions"].encode("utf-8"),
                                 ci_body + app.T2_BINDING_BRIDGE.encode("utf-8") + technical_body)
            self.assertEqual(ci.read_bytes.call_count, 2)
            self.assertEqual(technical.read_bytes.call_count, 2)

    def test_t2_read_failures_do_not_send_or_fall_back(self):
        for target in ("HUB_CI_PATH", "TECHNICAL_PATH"):
            for error in (FileNotFoundError(), PermissionError(), OSError(),
                          UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid")):
                with self.subTest(target=target, error=type(error).__name__), patch.object(app, target) as path, patch.object(app, "OpenAI") as client:
                    path.read_bytes.side_effect = error
                    with self.assertRaisesRegex(ValueError, "T2:.*không chuyển sang T1/T0"):
                        app.call_model(self.config, [], app.MODES[2])
                    client.assert_not_called()

    def test_t1_read_failures_do_not_send(self):
        for error in (FileNotFoundError(), PermissionError(), OSError(),
                      UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid")):
            with self.subTest(error=type(error).__name__), patch.object(app, "HUB_CI_PATH") as path, patch.object(app, "OpenAI") as client:
                path.read_bytes.side_effect = error
                with self.assertRaisesRegex(ValueError, "T1:.*không chuyển sang T0"):
                    app.call_model(self.config, [], app.MODES[1])
                client.assert_not_called()

    def ui_context(self):
        original = Path.read_text
        config = self.config

        def read_text(path, *args, **kwargs):
            if path.resolve() == app.CONFIG_PATH:
                return json.dumps(config)
            return original(path, *args, **kwargs)
        return patch.object(Path, "read_text", read_text)

    def test_ui_switch_preserves_history_and_response_labels(self):
        with self.ui_context(), patch("openai.OpenAI", self.client):
            ui = AppTest.from_file("app.py").run()
            self.assertFalse(ui.exception)
            self.assertEqual(list(ui.radio[0].options), list(app.MODES))
            modes = [app.MODES[0], app.MODES[1], app.MODES[2], app.MODES[1], app.MODES[0], app.MODES[2]]
            for index, mode in enumerate(modes):
                prompt = f"Lượt {index + 1}"
                ui.radio[0].set_value(mode).run()
                ui.text_area[0].set_value(prompt)
                ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertFalse(ui.error)
                self.assertEqual(len(self.payloads), len(ui.session_state.messages) // 2)
                self.assertEqual(self.payloads[-1]["input"], ui.session_state.messages[:-1])
                self.assertEqual("instructions" in self.payloads[-1], mode != app.MODES[0])
                if mode == app.MODES[1]:
                    self.assertEqual(self.payloads[-1]["instructions"].encode("utf-8"), app.HUB_CI_PATH.read_bytes())
                elif mode == app.MODES[2]:
                    self.assertEqual(self.payloads[-1]["instructions"].encode("utf-8"),
                                     app.HUB_CI_PATH.read_bytes() + app.T2_BINDING_BRIDGE.encode("utf-8") + app.TECHNICAL_PATH.read_bytes())
            self.assertEqual([m["role"] for m in ui.session_state.messages], ["user", "assistant"] * len(modes))
            self.assertEqual([c.caption[0].value for c in ui.chat_message if c.name == "assistant"],
                             modes)
            self.assertIn(modes[-1], ui.caption[1].value)

    def test_ui_ci_error_keeps_history_and_prompt(self):
        original = Path.read_bytes
        for mode, target, error in ((mode, target, error)
                                    for mode, target in ((app.MODES[1], app.HUB_CI_PATH),
                                                         (app.MODES[2], app.TECHNICAL_PATH))
                                    for error in (FileNotFoundError(), PermissionError())):
            def read_bytes(path):
                if path.resolve() == target:
                    raise error
                return original(path)
            with self.subTest(mode=mode, error=type(error).__name__), self.ui_context(), patch("openai.OpenAI", self.client):
                ui = AppTest.from_file("app.py").run()
                ui.text_area[0].set_value("T0")
                ui.button[0].click().run()
                history = list(ui.session_state.messages)
                calls = len(self.payloads)
                ui.radio[0].set_value(mode).run()
                with patch.object(Path, "read_bytes", read_bytes):
                    ui.text_area[0].set_value("Giữ prompt")
                    ui.button[0].click().run()
                self.assertFalse(ui.exception)
                self.assertIn(mode[:2] + ":", ui.error[0].value)
                self.assertEqual(ui.session_state.messages, history)
                self.assertEqual(ui.text_area[0].value, "Giữ prompt")
                self.assertEqual(len(self.payloads), calls)


if __name__ == "__main__":
    unittest.main()
