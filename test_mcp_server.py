"""M2-C1 contracts and real stdio protocol checks, with no model/API calls."""
import asyncio
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


REPO = Path(__file__).resolve().parent
EXPECTED = {
    "HUB-PKG-TECHNICAL": True, "HUB-PKG-CONCEPT-DEVELOPMENT": True,
    "HUB-PKG-AUTHORING": True, "HUB-PKG-AIS": True, "HUB-PKG-IMAGET": False,
}


class MCPServerTests(unittest.TestCase):
    def test_import_and_inspection_without_app_streamlit_or_execution(self):
        code = """
import sys
class BlockUI:
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'app', 'streamlit', 'm1'}:
            raise AssertionError('Forbidden import: ' + fullname)
sys.meta_path.insert(0, BlockUI())
import mcp_server as h
from unittest.mock import patch
with patch.object(h.host, 'OpenAI', side_effect=AssertionError('API execution')), \
     patch.object(h.t9.t8, 'call_t8', side_effect=AssertionError('T8 execution')), \
     patch.object(h.t9, 'call_t9', side_effect=AssertionError('AIS execution')):
    assert h.hub_status()['read_only']
    assert len(h.hub_runtime_inventory()['packages']) == 5
assert not {'app', 'streamlit', 'm1'} & set(sys.modules)
"""
        result = subprocess.run([sys.executable, "-c", code], cwd=REPO,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_exact_surface_annotations_and_capabilities(self):
        tools = asyncio.run(hub.list_tools())
        self.assertEqual({t.name for t in tools}, {"hub_status", "hub_runtime_inventory", "hub_prepare_root_selection", "hub_read_root_control", "hub_validate_root_selection", "hub_read_selected_package", "hub_read_selected_concept_interface", "hub_validate_concept_selection", "hub_read_selected_concept_leaf"})
        self.assertEqual(len(tools), 9)
        for tool in tools:
            self.assertTrue(tool.annotations.readOnlyHint)
            self.assertFalse(tool.annotations.destructiveHint)
            self.assertFalse(tool.annotations.openWorldHint)
            if tool.name == "hub_read_root_control":
                self.assertEqual(tool.inputSchema["properties"]["control_id"]["enum"], list(hub.ROOT_CONTROL_IDS))
                self.assertEqual(tool.inputSchema["required"], ["control_id", "offset"])
                self.assertFalse(tool.inputSchema["additionalProperties"])
                continue
            if tool.name in {"hub_read_selected_concept_interface", "hub_validate_concept_selection", "hub_read_selected_concept_leaf"}:
                required = {
                    "hub_read_selected_concept_interface": ["route_record", "component", "offset"],
                    "hub_validate_concept_selection": ["route_record", "leaf_record"],
                    "hub_read_selected_concept_leaf": ["route_record", "leaf_record", "module_id", "offset"],
                }[tool.name]
                self.assertEqual(tool.inputSchema["required"], required)
                self.assertEqual(tool.inputSchema["properties"]["route_record"], hub.t9.ROUTE_SCHEMA)
                if "leaf_record" in required:
                    self.assertEqual(tool.inputSchema["properties"]["leaf_record"], hub.host.LEAF_SCHEMA)
                else:
                    self.assertEqual(tool.inputSchema["properties"]["component"]["enum"], list(hub.CONCEPT_COMPONENTS))
                self.assertFalse(tool.inputSchema["additionalProperties"])
                continue
            if tool.name == "hub_read_selected_package":
                self.assertEqual(tool.inputSchema["required"], ["route_record", "package_id", "offset"])
                self.assertFalse(tool.inputSchema["additionalProperties"])
                continue
            if tool.name == "hub_validate_root_selection":
                self.assertEqual(tool.inputSchema["properties"], {"route_record": hub.t9.ROUTE_SCHEMA})
                self.assertEqual(tool.inputSchema["required"], ["route_record"])
                self.assertFalse(tool.inputSchema["additionalProperties"])
                continue
            self.assertEqual(tool.inputSchema,
                             {"type": "object", "properties": {}, "additionalProperties": False})
        capabilities = hub.server.create_initialization_options().capabilities
        self.assertIsNotNone(capabilities.tools)
        self.assertIsNone(capabilities.resources)
        self.assertIsNone(capabilities.prompts)
        for name in ("call_runtime", "call_model", "call_t8", "call_t9", "OpenAI"):
            self.assertFalse(hasattr(hub, name))
        for name in ("call_runtime", "call_model", "write_file", "call_t8", "call_t9"):
            with self.assertRaisesRegex(ValueError, "Unknown tool"):
                asyncio.run(hub.call_tool(name, {}))
        with self.assertRaises(ValueError):
            asyncio.run(hub.call_tool("hub_status", {"path": "anything"}))

    def test_truthful_status(self):
        status = hub.hub_status()
        self.assertEqual(status["runtime_mode"], hub.host.RUNTIME_MODE)
        self.assertEqual(status["transport"], "stdio")
        self.assertTrue(status["read_only"])
        self.assertFalse(status["write_enabled"])
        self.assertFalse(status["runtime_execution_enabled"])
        self.assertIn("no model or UI health check", status["status_scope"])
        self.assertEqual(status, hub.hub_status())

    def test_real_inventory_and_no_mutation(self):
        paths = [*REPO.joinpath("runtime").rglob("*"), hub.host.HUB_CATALOG_PATH]
        before = {p: p.read_bytes() for p in paths if p.is_file()}
        with patch.object(Path, "write_bytes", side_effect=AssertionError("write")), \
             patch.object(Path, "write_text", side_effect=AssertionError("write")), \
             patch.object(hub.host, "OpenAI", side_effect=AssertionError("API")):
            inventory = hub.hub_runtime_inventory()
        self.assertEqual({p["package_id"]: p["available"] for p in inventory["packages"]}, EXPECTED)
        self.assertEqual(inventory["binding_version"], "0.3")
        self.assertEqual(inventory["retrieval_authority"], "LOCAL_RUNTIME_FILE")
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_catalog_change_is_seen_next_call(self):
        original = hub.host.t7_read(hub.host.HUB_CATALOG_PATH)
        changed = original.replace("  version: '1.0'", "  version: '9.9'", 1)
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "catalog.yaml"
            catalog.write_text(changed, encoding="utf-8", newline="")
            with patch.object(hub.host, "HUB_CATALOG_PATH", catalog):
                packages = hub.hub_runtime_inventory()["packages"]
        technical = next(p for p in packages if p["package_id"] == "HUB-PKG-TECHNICAL")
        self.assertFalse(technical["available"])
        self.assertIn("mismatch", technical["reason"])
        self.assertTrue(hub.hub_runtime_inventory()["packages"][0]["available"])

    def test_bad_manifest_fails_closed(self):
        original = hub.host.t7_read(hub.t9.BINDINGS_PATH)
        changed = original.replace('"binding_version": "0.3"', '"binding_version": "9.9"')
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "bindings.json"
            manifest.write_text(changed, encoding="utf-8")
            with patch.object(hub.t9, "BINDINGS_PATH", manifest):
                with self.assertRaises(ValueError):
                    hub.hub_runtime_inventory()

    def test_corrupt_artifact_blocks_only_dependent_package(self):
        read_bytes = Path.read_bytes
        def corrupt(path):
            data = read_bytes(path)
            return data + b"changed" if path.name == "HUB-DOM-TECHNICAL_v1.0.md" else data
        with patch.object(Path, "read_bytes", corrupt):
            packages = hub.hub_runtime_inventory()["packages"]
        actual = {p["package_id"]: p["available"] for p in packages}
        self.assertEqual(actual, {**EXPECTED, "HUB-PKG-TECHNICAL": False})
        self.assertIn("SHA-256", packages[0]["reason"])

    def test_stdio_handshake_calls_errors_and_process_nonce(self):
        async def inspect_process():
            # Launch from outside the repo: all paths must be script-relative.
            parameters = StdioServerParameters(
                command=sys.executable, args=[str(REPO / "mcp_server.py")],
                cwd=tempfile.gettempdir())
            async with stdio_client(parameters) as (reader, writer):
                async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=20)) as session:
                    initialized = await session.initialize()
                    self.assertEqual(initialized.serverInfo.name, "central-hub")
                    tools = await session.list_tools()
                    self.assertEqual({t.name for t in tools.tools}, {"hub_status", "hub_runtime_inventory", "hub_prepare_root_selection", "hub_read_root_control", "hub_validate_root_selection", "hub_read_selected_package", "hub_read_selected_concept_interface", "hub_validate_concept_selection", "hub_read_selected_concept_leaf"})
                    status = await session.call_tool("hub_status", {})
                    self.assertFalse(status.isError)
                    inventory = await session.call_tool("hub_runtime_inventory", {})
                    self.assertFalse(inventory.isError)
                    self.assertEqual({p["package_id"]: p["available"]
                                      for p in inventory.structuredContent["packages"]}, EXPECTED)
                    for name, arguments in (("call_runtime", {}), ("hub_status", {"write": True})):
                        rejected = await session.call_tool(name, arguments)
                        self.assertTrue(rejected.isError)
                    repeated = await session.call_tool("hub_status", {})
                    self.assertEqual(status.structuredContent, repeated.structuredContent)
                    return status.structuredContent["process_nonce"]
        first = asyncio.run(inspect_process())
        second = asyncio.run(inspect_process())
        self.assertRegex(first, r"^[0-9a-f]{32}$")
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, hub.hub_status()["process_nonce"])


if __name__ == "__main__":
    unittest.main()
