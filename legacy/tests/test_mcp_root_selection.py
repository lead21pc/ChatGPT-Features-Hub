"""M2-C2 root seam: deterministic validation/protocol, not live model evidence."""
import asyncio
import copy
import hashlib
from datetime import timedelta
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import mcp_server as hub


REPO = Path(__file__).resolve().parents[2]


def record(*pids):
    text = hub.host.t7_read(hub.host.HUB_CATALOG_PATH)
    catalog = hub.host.t7_catalog_identities(text, "packages", "package_id")
    sources = hub.t9.catalog_sources(text)
    return dict(task_scope="Fixture scope, not a model routing result", selected_packages=[
        {**{k: catalog[pid][k] for k in ("package_id", "entrypoint_module_id", "runtime_role", "version")},
         "declared_source_path": sources.get(pid, ""), "application_scope": "Fixture portion",
         "reason": "Declared fixture selection"} for pid in pids], unresolved_blockers=[])


class RootSelectionTests(unittest.TestCase):
    def test_prepare_exact_controls_schema_read_set_and_rereads(self):
        read = hub.host.t7_read
        paths = [hub.host.HUB_CI_PATH, hub.host.HUB_ROUTER_PATH,
                 hub.host.HUB_ARCHITECTURE_PATH, hub.host.HUB_CATALOG_PATH]
        for suffix in ("", "\r\n# current edit\r\n"):
            def current(path):
                return read(path) + suffix if path in paths else read(path)
            with patch.object(hub.host, "t7_read", side_effect=current) as reads, \
                 patch.object(hub.host, "t7_retrieve", side_effect=AssertionError("body read")), \
                 patch.object(hub, "hub_runtime_inventory", side_effect=AssertionError("leaf inventory")):
                result = hub.hub_prepare_root_selection()
            self.assertEqual([c.args[0] for c in reads.call_args_list], paths + [hub.t9.BINDINGS_PATH])
            self.assertEqual(result["controls"], [
                {"control_id": cid, "path": p.relative_to(REPO).as_posix(), "total_length": len(read(p) + suffix),
                 "sha256": hashlib.sha256((read(p) + suffix).encode("utf-8")).hexdigest()}
                for cid, p in zip(hub.ROOT_CONTROL_IDS, paths)])
            self.assertTrue(all("text" not in control for control in result["controls"]))
            self.assertEqual(result["result_schema"], hub.t9.ROUTE_SCHEMA)
            self.assertNotIn("leaves", str(result["local_binding_context"]))
            self.assertEqual([p["binding_declared"] for p in result["local_binding_context"]],
                             [True, True, True, True, False, False])
        result["result_schema"].clear()
        self.assertEqual(hub.hub_prepare_root_selection()["result_schema"], hub.t9.ROUTE_SCHEMA)

    def test_exact_chunk_reconstruction_and_read_set(self):
        prepared = hub.hub_prepare_root_selection()
        read = hub.host.t7_read
        with patch.object(hub.host, "t7_retrieve", side_effect=AssertionError("body read")), \
             patch.object(hub, "hub_runtime_inventory", side_effect=AssertionError("leaf inventory")):
            for manifest in prepared["controls"]:
                self.assertFalse(Path(manifest["path"]).is_absolute())
                path = hub.REPO_ROOT / manifest["path"]
                expected = path.read_bytes().decode("utf-8")
                for size in (None, 137, hub.ROOT_CONTROL_MAX_CHARS):
                    offset, chunks = 0, []
                    while True:
                        args = {} if size is None else {"max_chars": size}
                        with patch.object(hub.host, "t7_read", wraps=read) as reads:
                            result = hub.hub_read_root_control(manifest["control_id"], offset, **args)
                        reads.assert_called_once_with(path)
                        self.assertEqual({key: result[key] for key in manifest}, manifest)
                        self.assertEqual(result["offset"], offset)
                        self.assertEqual(result["text"], expected[offset:result["next_offset"]])
                        self.assertLessEqual(len(result["text"]), size or hub.ROOT_CONTROL_DEFAULT_CHARS)
                        chunks.append(result["text"])
                        self.assertEqual(result["next_offset"], offset + len(result["text"]))
                        self.assertEqual(result["has_more"], result["next_offset"] < len(expected))
                        if not result["has_more"]:
                            break
                        self.assertGreater(result["next_offset"], offset)
                        offset = result["next_offset"]
                    self.assertEqual("".join(chunks), expected)
                eof = hub.hub_read_root_control(manifest["control_id"], len(expected))
                self.assertEqual(eof["text"], "")
                self.assertFalse(eof["has_more"])

    def test_invalid_chunk_arguments_rejected_before_read(self):
        good = {"control_id": "hub_ci", "offset": 0}
        bad = [{**good, "control_id": v} for v in ("unknown", "../file", "HUB-PKG-TECHNICAL", None, [], 1)]
        bad += [{**good, "offset": v} for v in (-1, True, 1.5, "0", None)]
        bad += [{**good, "max_chars": v} for v in (0, -1, True, 1.5, "2", None, 4001)]
        bad += [{}, {"control_id": "hub_ci"}, {**good, "path": "other"}, None, []]
        with patch.object(hub.host, "t7_read", side_effect=AssertionError("invalid read")):
            for args in bad:
                with self.subTest(args=args), self.assertRaises(ValueError):
                    asyncio.run(hub.call_tool("hub_read_root_control", args))
        with self.assertRaisesRegex(ValueError, "exceeds"):
            hub.hub_read_root_control("hub_ci", len(hub.host.HUB_CI_PATH.read_bytes().decode("utf-8")) + 1)

    def test_current_file_hash_length_unicode_and_newlines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ci.md"
            with patch.object(hub.host, "HUB_CI_PATH", path), patch.object(hub, "REPO_ROOT", path.parent):
                previous = None
                for text in ("a\r\nb\nVi\u1ec7t\U0001f600", "a\r\nb\nVi\u1ec7t\U0001f601",
                             "a\r\nb\nVi\u1ec7t\U0001f601 th\u00eam", ""):
                    path.write_bytes(text.encode("utf-8"))
                    first = hub.hub_read_root_control("hub_ci", 0, 2)
                    self.assertEqual(first["text"], text[:2])
                    self.assertEqual(first["total_length"], len(text))
                    self.assertEqual(first["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
                    if previous:
                        self.assertNotEqual(first["sha256"], previous["sha256"])
                    tail = hub.hub_read_root_control("hub_ci", first["next_offset"])
                    self.assertEqual(first["text"] + tail["text"], text)
                    previous = first

    def test_empty_and_each_bound_root_no_leaf_reads(self):
        retrieve = hub.host.t7_retrieve
        for pid in (None, "HUB-PKG-TECHNICAL", "HUB-PKG-CONCEPT-DEVELOPMENT",
                    "HUB-PKG-AUTHORING", "HUB-PKG-AIS"):
            route = record(*([pid] if pid else []))
            before = copy.deepcopy(route)
            with patch.object(hub.host, "t7_retrieve", wraps=retrieve) as reads:
                result = hub.hub_validate_root_selection(route)
            self.assertEqual(route, before)
            self.assertEqual(result["route_record"], route)
            self.assertTrue(result["record_valid"])
            self.assertEqual(result["unresolved_blockers"], [])
            self.assertEqual(len(reads.call_args_list), 0 if pid is None else 2 if pid == hub.t9.AIS else 1)
            self.assertTrue(all("leaf" not in c.args[0]["path"] and
                                "CATALOG" not in c.args[0]["path"] for c in reads.call_args_list))

    def test_imaget_selection_and_host_blockers_preserved(self):
        route = record("HUB-PKG-TECHNICAL", "HUB-PKG-IMAGET")
        route["unresolved_blockers"] = ["Host-declared unresolved condition"]
        result = hub.hub_validate_root_selection(route)
        self.assertEqual(result["selected_package_ids"], [s["package_id"] for s in route["selected_packages"]])
        self.assertEqual(result["route_record"], route)
        self.assertEqual([p["available"] for p in result["selected_package_availability"]], [True, False])
        self.assertEqual(result["unresolved_blockers"][0], route["unresolved_blockers"][0])
        self.assertIn("HUB-PKG-IMAGET: local-runtime unavailable", result["unresolved_blockers"][1])

    def test_reject_malformed_duplicates_and_exact_identity_mismatches_before_reads(self):
        good = record("HUB-PKG-TECHNICAL")
        bad = [None, [], {}, {**good, "extra": True}, {**good, "task_scope": 1},
               {**good, "selected_packages": {}}, {**good, "unresolved_blockers": "x"},
               {**good, "unresolved_blockers": [{}]},
               {**good, "selected_packages": good["selected_packages"] * 2}]
        for key in good["selected_packages"][0]:
            route = copy.deepcopy(good)
            route["selected_packages"][0][key] = 42
            bad.append(route)
        for key in ("package_id", "entrypoint_module_id", "runtime_role", "version", "declared_source_path"):
            route = copy.deepcopy(good)
            route["selected_packages"][0][key] += "-wrong"
            bad.append(route)
        for selection in ({}, {**good["selected_packages"][0], "extra": "x"}, "wrong"):
            bad.append({**good, "selected_packages": [selection]})
        with patch.object(hub.host, "t7_retrieve", side_effect=AssertionError("premature read")):
            for route in bad:
                with self.subTest(route=route), self.assertRaises(ValueError):
                    hub.hub_validate_root_selection(route)

    def test_current_catalog_and_binding_artifact_failures(self):
        route = record("HUB-PKG-TECHNICAL")
        read = hub.host.t7_read
        def changed(path):
            text = read(path)
            return text.replace("version: '1.0'", "version: '9.9'", 1) if path == hub.host.HUB_CATALOG_PATH else text
        with patch.object(hub.host, "t7_read", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "mismatch"):
                hub.hub_validate_root_selection(route)
        with patch.object(hub.host, "t7_retrieve", side_effect=ValueError("SHA-256 failure")):
            result = hub.hub_validate_root_selection(route)
        self.assertEqual(result["selected_package_ids"], ["HUB-PKG-TECHNICAL"])
        self.assertFalse(result["selected_package_availability"][0]["available"])
        self.assertIn("SHA-256 failure", result["unresolved_blockers"][0])
        for invalid in ("", "\x00", "not a manifest"):
            with patch.object(hub.host, "t7_read", return_value=invalid):
                with self.assertRaises(ValueError):
                    hub.hub_prepare_root_selection()

    def test_no_ui_model_runtime_or_file_write(self):
        code = '''
import sys
class BlockUI:
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'app', 'streamlit', 'm1'}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, BlockUI())
import mcp_server as h
from pathlib import Path
from unittest.mock import patch
with patch.object(h.host, 'OpenAI', side_effect=AssertionError('API')), \\
     patch.object(h.t9, 'call_t9', side_effect=AssertionError('T9')), \\
     patch.object(h.t9.t8, 'call_t8', side_effect=AssertionError('T8')), \\
     patch.object(Path, 'write_bytes', side_effect=AssertionError('write')), \\
     patch.object(Path, 'write_text', side_effect=AssertionError('write')):
    prepared = h.hub_prepare_root_selection()
    with patch.object(h.host, 't7_retrieve', side_effect=AssertionError('body')):
        for control in prepared['controls']:
            offset = 0
            while True:
                chunk = h.hub_read_root_control(control['control_id'], offset)
                if not chunk['has_more']:
                    break
                offset = chunk['next_offset']
    h.hub_validate_root_selection(dict(task_scope='ordinary', selected_packages=[], unresolved_blockers=[]))
assert not {'app', 'streamlit', 'm1'} & set(sys.modules)
'''
        result = subprocess.run([sys.executable, "-c", code], cwd=REPO / "legacy",
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_stdio_prepare_validate_and_errors(self):
        async def inspect():
            params = StdioServerParameters(command=sys.executable, args=[str(REPO / "legacy" / "mcp_server.py")],
                                           cwd=tempfile.gettempdir())
            async with stdio_client(params) as (reader, writer):
                async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=20)) as session:
                    await session.initialize()
                    prepared = await session.call_tool("hub_prepare_root_selection", {})
                    self.assertFalse(prepared.isError)
                    self.assertEqual(prepared.structuredContent["result_schema"], hub.t9.ROUTE_SCHEMA)
                    for control in prepared.structuredContent["controls"]:
                        offset, chunks = 0, []
                        while True:
                            response = await session.call_tool("hub_read_root_control", {
                                "control_id": control["control_id"], "offset": offset})
                            self.assertFalse(response.isError)
                            chunk = response.structuredContent
                            self.assertEqual({k: chunk[k] for k in control}, control)
                            chunks.append(chunk["text"])
                            self.assertEqual(chunk["offset"], offset)
                            if not chunk["has_more"]:
                                break
                            self.assertGreater(chunk["next_offset"], offset)
                            offset = chunk["next_offset"]
                        self.assertEqual("".join(chunks), (REPO / control["path"]).read_bytes().decode("utf-8"))
                    for route in (record(), record("HUB-PKG-TECHNICAL"), record("HUB-PKG-IMAGET")):
                        result = await session.call_tool("hub_validate_root_selection", {"route_record": route})
                        self.assertFalse(result.isError)
                        self.assertEqual(result.structuredContent["route_record"], route)
                    for name, args in (("hub_prepare_root_selection", {"request": "x"}),
                                       ("hub_read_root_control", {}),
                                       ("hub_read_root_control", {"control_id": "wrong", "offset": 0}),
                                       ("hub_read_root_control", {"control_id": "hub_ci", "offset": -1}),
                                       ("hub_read_root_control", {"control_id": "hub_ci", "offset": 0, "max_chars": 4001}),
                                       ("hub_validate_root_selection", {}),
                                       ("hub_validate_root_selection", {"route_record": record(), "extra": True}),
                                       ("hub_validate_root_selection", {"route_record": {}})):
                        result = await session.call_tool(name, args)
                        self.assertTrue(result.isError)
        asyncio.run(inspect())


if __name__ == "__main__":
    unittest.main()
