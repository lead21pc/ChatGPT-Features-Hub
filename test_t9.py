import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import app
import runtime_host
import t8
import t9


AIS_PIPELINE_PATH = t9.BINDINGS_PATH.parent / "packages/ais/AIS_PIPELINE_v1.1.md"
AIS_ROUTER_PATH = AIS_PIPELINE_PATH.with_name("AIS_ROUTER_v1.2.yaml")


def root_package(package_id):
    identities = {
        "HUB-PKG-TECHNICAL": ("HUB-DOM-TECHNICAL", "REASONING_PROFILE", "1.0", ""),
        "HUB-PKG-CONCEPT-DEVELOPMENT": ("HUB-DOM-CONCEPT-DEVELOPMENT", "DOMAIN_CONTROL", "1.1", ""),
        "HUB-PKG-AUTHORING": ("HUB-CAP-AUTHORING", "CAPABILITY", "0.7", ""),
        "HUB-PKG-AIS": ("HUB-PIPE-AIS", "TOOL_PIPELINE", "1.1", "tool_pipelines/AIS/AIS_PIPELINE_v1.1.md"),
    }
    module, role, version, source = identities[package_id]
    return {
        "package_id": package_id,
        "entrypoint_module_id": module,
        "runtime_role": role,
        "application_scope": "current scoped portion",
        "reason": "mock semantic route",
        "version": version,
        "declared_source_path": source,
    }


def message(text, annotations=None):
    return {
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [{
            "type": "output_text",
            "text": text,
            "annotations": annotations or [],
        }],
    }


class FakeResponse:
    def __init__(self, text, output=None, status="completed"):
        self.output_text = text
        self._data = {"status": status, "output": output if output is not None else [message(text)]}

    def model_dump(self):
        return copy.deepcopy(self._data)


class T9Tests(unittest.TestCase):
    def setUp(self):
        self.config = {"openai_api_key": "mock-only", "model": "mock-model"}
        self.messages = [{"role": "user", "content": "Verify a current external claim."}]
        self.route = {
            "task_scope": "external verification only",
            "selected_packages": [root_package(t9.AIS)],
            "unresolved_blockers": [],
        }
        self.payloads = []
        self.reads = []
        self.overrides = {}
        self.original_read = Path.read_bytes
        self.ais_status = "completed"
        self.final_status = "completed"
        self.ais_output = [
            {
                "type": "web_search_call",
                "id": "ws1",
                "status": "completed",
                "action": {
                    "type": "search",
                    "queries": ["current external claim"],
                    "sources": [
                        {"url": "https://example.com/a"},
                        {"url": "https://example.com/b"},
                        {"url": "https://example.com/a"},
                    ],
                },
            },
            {
                "type": "web_search_call",
                "id": "ws2",
                "status": "completed",
                "action": {
                    "type": "open_page",
                    "sources": [{"url": "https://example.com/b"}],
                },
            },
            message("AIS evidence", [
                {"type": "url_citation", "url": "https://example.com/a"},
                {"type": "url_citation", "url": "https://example.com/c"},
                {"type": "url_citation", "url": "https://example.com/a"},
            ]),
        ]

    def read(self, path):
        self.reads.append(path)
        value = self.overrides.get(path)
        if isinstance(value, Exception):
            raise value
        return value if value is not None else self.original_read(path)

    def openai(self, **kwargs):
        self.assertEqual(kwargs["base_url"], "https://api.openai.com/v1")
        self.assertEqual(kwargs["max_retries"], 0)
        parent = self

        class Responses:
            def create(self, **payload):
                parent.payloads.append(copy.deepcopy(payload))
                fmt = payload.get("text", {}).get("format", {})
                if fmt.get("name") == "hub_t9_root":
                    text = json.dumps(parent.route)
                    return FakeResponse(text, [message(text)])
                if "tools" in payload:
                    return FakeResponse("AIS evidence", parent.ais_output, parent.ais_status)
                return FakeResponse("Final Hub answer", [message("Final Hub answer")], parent.final_status)

        class Client:
            responses = Responses()
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False

        return Client()

    def run_t9(self):
        before = copy.deepcopy(self.messages)
        with patch.object(Path, "read_bytes", lambda path: self.read(path)), patch.object(runtime_host, "OpenAI", self.openai):
            result = t9.call_t9(self.config, self.messages)
        self.assertEqual(self.messages, before)
        return result

    def test_binding_inventory_and_runtime_pair(self):
        manifest = json.loads(t9.BINDINGS_PATH.read_text(encoding="utf-8"))
        old = json.loads(t8.BINDINGS_PATH.read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["packages"]), set(old["packages"]) | {t9.AIS})
        self.assertEqual({k: manifest["packages"][k] for k in old["packages"]}, old["packages"])
        self.assertNotIn("HUB-PKG-IMAGET", manifest["packages"])
        binding = t9.load_bindings(t9.BINDINGS_PATH.read_text(encoding="utf-8"))
        for key, runtime_path, upstream_path in (
            ("pipeline", AIS_PIPELINE_PATH, app.HUB_CI_PATH.parent / "tool_pipelines/AIS/AIS_PIPELINE_v1.1.md"),
            ("router", AIS_ROUTER_PATH, app.HUB_CI_PATH.parent / "tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml"),
        ):
            self.assertEqual(runtime_path.read_bytes(), upstream_path.read_bytes())
            self.assertEqual(hashlib.sha256(runtime_path.read_bytes()).hexdigest(), binding[key]["sha256"])

    def test_no_ais_path_reads_no_ais_and_exposes_no_tool(self):
        self.route["selected_packages"] = []
        answer, trace = self.run_t9()
        self.assertEqual(answer, "Final Hub answer")
        self.assertFalse(trace["ais_selected"])
        self.assertFalse(trace["ais_web_search_executed"])
        self.assertNotIn(AIS_PIPELINE_PATH, self.reads)
        self.assertNotIn(AIS_ROUTER_PATH, self.reads)
        self.assertEqual(len(self.payloads), 2)
        self.assertNotIn("tools", self.payloads[-1])

    def test_root_sees_controls_not_manifest_or_ais_bodies(self):
        self.run_t9()
        root = self.payloads[0]["instructions"]
        for path in (app.HUB_CI_PATH, app.HUB_ROUTER_PATH, app.HUB_ARCHITECTURE_PATH, app.HUB_CATALOG_PATH):
            self.assertIn(self.original_read(path).decode("utf-8"), root)
        self.assertNotIn(t9.BINDINGS_PATH.read_text(encoding="utf-8"), root)
        self.assertNotIn(self.original_read(AIS_PIPELINE_PATH).decode("utf-8"), root)
        self.assertNotIn(self.original_read(AIS_ROUTER_PATH).decode("utf-8"), root)

    def test_native_web_search_payload_and_final_without_tools(self):
        answer, trace = self.run_t9()
        self.assertEqual(answer, "Final Hub answer")
        self.assertTrue(trace["ais_selected"])
        self.assertEqual(trace["ais_retrieved_module_ids"], ["HUB-PIPE-AIS", "AIS_ROUTER_v1.2"])
        ais_payload = self.payloads[1]
        self.assertEqual(ais_payload["tools"], [{"type": "web_search"}])
        self.assertEqual(ais_payload["tool_choice"], "required")
        self.assertEqual(ais_payload["include"], ["web_search_call.action.sources"])
        self.assertFalse(ais_payload["store"])
        self.assertNotIn("tools", self.payloads[2])
        self.assertFalse(self.payloads[2]["store"])

    def test_observable_trace_dedupes_sources_and_citations(self):
        _, trace = self.run_t9()
        self.assertTrue(trace["ais_web_search_executed"])
        self.assertEqual([a["type"] for a in trace["web_search_actions"]], ["search", "open_page"])
        self.assertEqual(trace["web_search_actions"][0]["queries"], ["current external claim"])
        self.assertEqual(trace["source_urls"], ["https://example.com/a", "https://example.com/b"])
        self.assertEqual(trace["citation_urls"], ["https://example.com/a", "https://example.com/c"])
        self.assertEqual(trace["ais_output_text"], "AIS evidence")

    def test_mixed_root_records_non_ais_without_loading_them(self):
        self.route["selected_packages"] = [
            root_package(t9.AIS),
            root_package("HUB-PKG-TECHNICAL"),
            root_package("HUB-PKG-CONCEPT-DEVELOPMENT"),
            root_package("HUB-PKG-AUTHORING"),
        ]
        _, trace = self.run_t9()
        self.assertEqual(trace["non_ais_selected_but_not_executed"], [
            "HUB-PKG-TECHNICAL", "HUB-PKG-CONCEPT-DEVELOPMENT", "HUB-PKG-AUTHORING"
        ])
        final = self.payloads[-1]["instructions"]
        self.assertIn("AIS evidence", final)
        self.assertIn("https://example.com/a", final)
        self.assertNotIn(self.original_read(app.TECHNICAL_PATH).decode("utf-8"), final)
        self.assertNotIn(self.original_read(app.CONCEPT_CORE_PATH).decode("utf-8"), final)

    def test_missing_web_search_call_fails_even_if_model_claims_search(self):
        self.ais_output = [message("I searched the web.")]
        with self.assertRaisesRegex(ValueError, "web_search_call"):
            self.run_t9()
        self.assertEqual(len(self.payloads), 2)

    def test_incomplete_empty_refusal_ais_fail_no_final(self):
        cases = [
            ("incomplete", [message("AIS evidence")]),
            ("completed", [message("")]),
            ("completed", [{"type": "message", "content": [{"type": "refusal", "refusal": "no"}]}]),
        ]
        for status, output in cases:
            with self.subTest(status=status, output=output):
                self.ais_status = status
                self.ais_output = output
                self.payloads.clear()
                with self.assertRaises(ValueError):
                    self.run_t9()
                self.assertEqual(len(self.payloads), 2)

    def test_noncompleted_search_action_is_blocker(self):
        self.ais_output[0]["status"] = "failed"
        with self.assertRaises(ValueError) as caught:
            self.run_t9()
        self.assertTrue(caught.exception.trace["ais_web_search_executed"])
        self.assertTrue(caught.exception.trace["unresolved_blockers"])
        self.assertEqual(len(self.payloads), 2)

    def test_final_failure_preserves_call_boundary(self):
        self.final_status = "incomplete"
        with self.assertRaises(ValueError):
            self.run_t9()
        self.assertEqual(len(self.payloads), 3)

    def test_artifact_failures_block_before_search_without_fallback(self):
        for path in (AIS_PIPELINE_PATH, AIS_ROUTER_PATH):
            for failure in (FileNotFoundError(), PermissionError(), OSError(), b"tampered", b"\xff"):
                with self.subTest(path=path, failure=type(failure).__name__ if isinstance(failure, Exception) else failure):
                    self.overrides = {path: failure}
                    self.payloads.clear()
                    self.reads.clear()
                    with self.assertRaises(ValueError):
                        self.run_t9()
                    self.assertEqual(len(self.payloads), 1)

    def test_bad_manifest_duplicate_inventory_version_and_path_fail(self):
        bad = [b"{}", b"[]", b"{", b'{"binding_version":"0.3","binding_version":"0.3"}']
        manifest = json.loads(t9.BINDINGS_PATH.read_text(encoding="utf-8"))
        item = copy.deepcopy(manifest); item["binding_version"] = "0.2"; bad.append(json.dumps(item).encode())
        item = copy.deepcopy(manifest); item["packages"]["HUB-PKG-IMAGET"] = {}; bad.append(json.dumps(item).encode())
        item = copy.deepcopy(manifest); item["packages"][t9.AIS]["router"]["version"] = "9.9"; bad.append(json.dumps(item).encode())
        item = copy.deepcopy(manifest); item["packages"][t9.AIS]["pipeline"]["path"] = "../outside.md"; bad.append(json.dumps(item).encode())
        for content in bad:
            with self.subTest(content=content[:50]):
                self.overrides = {t9.BINDINGS_PATH: content}
                self.payloads.clear()
                with patch.object(Path, "read_bytes", lambda path: self.read(path)), patch.object(runtime_host, "OpenAI") as client:
                    with self.assertRaises(ValueError):
                        t9.call_t9(self.config, self.messages)
                    client.assert_not_called()

    def test_hash_mismatch_blocks_after_root_before_search(self):
        manifest = json.loads(t9.BINDINGS_PATH.read_text(encoding="utf-8"))
        item = copy.deepcopy(manifest)
        item["packages"][t9.AIS]["pipeline"]["sha256"] = "0" * 64
        self.overrides = {t9.BINDINGS_PATH: json.dumps(item).encode()}
        with self.assertRaises(ValueError):
            self.run_t9()
        self.assertEqual(len(self.payloads), 1)

    def test_root_identity_version_or_source_mismatch_fails_before_retrieval(self):
        for field, value in (
            ("runtime_role", "CAPABILITY"),
            ("version", "9.9"),
            ("declared_source_path", "wrong.md"),
        ):
            with self.subTest(field=field):
                self.route["selected_packages"] = [root_package(t9.AIS)]
                self.route["selected_packages"][0][field] = value
                self.payloads.clear(); self.reads.clear()
                with self.assertRaises(ValueError):
                    self.run_t9()
                self.assertNotIn(AIS_PIPELINE_PATH, self.reads)
                self.assertEqual(len(self.payloads), 1)

    def test_controls_manifest_reread_and_mode_wiring(self):
        self.run_t9()
        first = list(self.reads)
        self.payloads.clear(); self.reads.clear()
        self.run_t9()
        for path in (app.HUB_CI_PATH, app.HUB_ROUTER_PATH, app.HUB_ARCHITECTURE_PATH, app.HUB_CATALOG_PATH, t9.BINDINGS_PATH):
            self.assertIn(path, first)
            self.assertIn(path, self.reads)
        self.assertEqual(app.MODES[-1], "T9 - AIS Local Execution")
        self.assertEqual(json.loads(app.T7_BINDINGS_PATH.read_text(encoding="utf-8"))["binding_version"], "0.1")
        self.assertEqual(json.loads(t8.BINDINGS_PATH.read_text(encoding="utf-8"))["binding_version"], "0.2")


if __name__ == "__main__":
    unittest.main()
