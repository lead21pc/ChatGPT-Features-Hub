"""Read-only Central Hub inspection over MCP stdio; no package execution."""
import asyncio
import json
import secrets

from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

import runtime_host as host
import t9


server = Server("central-hub")
_PROCESS_NONCE = secrets.token_hex(16)


def hub_status():
    """Describe this inspection process, not a running model or UI session."""
    return {
        "runtime_mode": host.RUNTIME_MODE,
        "transport": "stdio",
        "read_only": True,
        "write_enabled": False,
        "runtime_execution_enabled": False,
        "status_scope": "MCP inspection process; no model or UI health check",
        "process_nonce": _PROCESS_NONCE,
    }


def hub_runtime_inventory():
    """Reread current bindings/catalog and verify local artifacts without activation."""
    binding_text = host.t7_read(t9.BINDINGS_PATH)
    ais = t9.load_bindings(binding_text)
    manifest = json.loads(binding_text, object_pairs_hook=t9.unique_object)
    packages = manifest["packages"]
    catalog_text = host.t7_read(host.HUB_CATALOG_PATH)
    catalog = host.t7_catalog_identities(catalog_text, "packages", "package_id")
    if set(packages) - set(catalog):
        raise ValueError("Local binding package absent from root Catalog")
    sources = t9.catalog_sources(catalog_text)
    inventory = []
    for pid, identity in catalog.items():
        item = {**identity, "available": False, "reason": "No local runtime binding"}
        if pid in packages:
            try:
                package = packages[pid]
                if pid == t9.AIS:
                    t9.validate_ais_catalog(catalog_text, identity, sources.get(pid))
                    t9.retrieve_pair(ais)
                else:
                    entry = package["entrypoint"]
                    if identity["status"] != "ACTIVE" or any(
                        entry[key] != identity[root_key] for key, root_key in (
                            ("module_id", "entrypoint_module_id"),
                            ("runtime_role", "runtime_role"), ("version", "version"))
                    ):
                        raise ValueError("Local binding/Catalog identity mismatch")
                    host.t7_retrieve(entry)
                    if "local_catalog" in package:
                        local_id = package["local_catalog"]
                        block = catalog_text.split("- package_id: " + pid + "\n", 1)[1].split("\n- package_id:", 1)[0]
                        block = block.split("  local_catalog:\n", 1)[1].split("    location:", 1)[0]
                        for key in ("module_id", "package_id", "runtime_role", "status", "version"):
                            scalar = f"    {key}: "
                            values = [line[len(scalar):].strip("'\"")
                                      for line in block.splitlines() if line.startswith(scalar)]
                            if values != [{**local_id, "package_id": pid, "status": "ACTIVE"}[key]]:
                                raise ValueError("Local Concept Catalog interface identity mismatch")
                        local = host.t7_retrieve(local_id)
                        leaves = host.t7_catalog_identities(local, "entries", "module_id")
                        for leaf in package["leaves"]:
                            leaf_id = leaves.get(leaf["module_id"])
                            if leaf_id is None or leaf_id["status"] != "ACTIVE" or any(
                                leaf[key] != leaf_id[key]
                                for key in ("module_id", "runtime_role", "version")
                            ):
                                raise ValueError("Local leaf binding/Catalog identity mismatch")
                            host.t7_retrieve(leaf)
                item.update(available=True, reason="Local artifacts read and SHA-256 verified")
            except (ValueError, IndexError, KeyError) as exc:
                item["reason"] = str(exc)
        inventory.append(item)
    return {
        "runtime_mode": host.RUNTIME_MODE,
        "binding_version": manifest["binding_version"],
        "retrieval_authority": manifest["retrieval_authority"],
        "bindings_path": str(t9.BINDINGS_PATH),
        "catalog_path": str(host.HUB_CATALOG_PATH),
        "availability_scope": "Local retrieval only; no activation, execution or deployment proof",
        "packages": inventory,
    }


@server.list_tools()
async def list_tools():
    return [types.Tool(
        name=name, description=description,
        inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
        annotations=types.ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False),
    ) for name, description in (
        ("hub_status", "Inspect local Central Hub runtime mode and read-only MCP process status."),
        ("hub_runtime_inventory", "Inspect current local package availability; never activate or execute packages."),
    )]


@server.call_tool()
async def call_tool(name, arguments):
    if arguments:
        raise ValueError("These read-only tools accept no arguments")
    if name == "hub_status":
        return hub_status()
    if name == "hub_runtime_inventory":
        return hub_runtime_inventory()
    raise ValueError("Unknown tool")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
