"""Read-only Central Hub controls/retrieval over MCP; semantic execution is host-owned."""
import asyncio
import copy
import hashlib
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


ROOT_TASK = (
    "Perform semantic TASK_SCOPE and ROOT_PACKAGE_SELECTION only for the current user request "
    "and relevant history, after reading every listed control fully with hub_read_root_control "
    "from offset 0 until has_more=false, checking consistent sha256 and total_length. "
    "Offsets and lengths count Unicode code points; sha256 hashes the full UTF-8 file bytes. "
    "Each call reads the current file, not a retained snapshot. The host model makes the selection; "
    "Python does not interpret applicability. Return the supplied t9 root contract with exact Catalog "
    "identities, version and declared_source_path (empty string when absent). Empty selection is valid. "
    "Do not inspect leaf inventories. Do not suppress applicable packages due to local unavailability. "
    "Pending post-selection retrieval is not an unresolved blocker. Report only genuine unresolved "
    "conditions. Stop after root selection: selection != retrieval != execution. No fallback or retry."
)
LOCAL_ROOT_BOUNDARY = (
    "LOCAL_RUNTIME_FILE v0.3 supplies the existing Technical, Concept, Authoring and AIS storage "
    "bindings only; historical Library/Project storage metadata does not block these local bindings. "
    "All non-storage semantics remain unchanged. ImageT has no local binding; select it if applicable "
    "and expose unavailability. Availability never activates a package. This milestone executes no "
    "package, resolves no leaves and grants no tool execution or state promotion."
)
ROOT_CONTROL_IDS = ("hub_ci", "hub_router", "hub_architecture", "hub_catalog")
ROOT_CONTROL_DEFAULT_CHARS = 2000
ROOT_CONTROL_MAX_CHARS = 4000


def _root_control_paths():
    return (host.HUB_CI_PATH, host.HUB_ROUTER_PATH,
            host.HUB_ARCHITECTURE_PATH, host.HUB_CATALOG_PATH)


def _control_identity(control_id, path, text):
    return {"control_id": control_id, "path": str(path), "total_length": len(text),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def hub_read_root_control(control_id, offset, max_chars=ROOT_CONTROL_DEFAULT_CHARS):
    """Return an exact slice from one fresh full-file UTF-8 read; retain no snapshot."""
    if not isinstance(control_id, str) or control_id not in ROOT_CONTROL_IDS:
        raise ValueError("Invalid root control_id")
    if type(offset) is not int or offset < 0:
        raise ValueError("offset must be an integer >= 0")
    if type(max_chars) is not int or not 1 <= max_chars <= ROOT_CONTROL_MAX_CHARS:
        raise ValueError("max_chars must be an integer from 1 to 4000")
    path = _root_control_paths()[ROOT_CONTROL_IDS.index(control_id)]
    text = host.t7_read(path)
    if offset > len(text):
        raise ValueError("offset exceeds current total_length")
    chunk = text[offset:offset + max_chars]
    next_offset = offset + len(chunk)
    return {**_control_identity(control_id, path, text), "text": chunk,
            "offset": offset, "next_offset": next_offset, "has_more": next_offset < len(text)}


def _root_context():
    paths = _root_control_paths()
    texts = [host.t7_read(path) for path in paths]
    if any(not text.strip() or "\x00" in text for text in texts):
        raise ValueError("Root control is empty or contains NUL; no fallback/retry")
    catalog = host.t7_catalog_identities(texts[3], "packages", "package_id")
    sources = t9.catalog_sources(texts[3])
    binding_text = host.t7_read(t9.BINDINGS_PATH)
    ais = t9.load_bindings(binding_text)
    packages = json.loads(binding_text, object_pairs_hook=t9.unique_object)["packages"]
    if set(packages) - set(catalog):
        raise ValueError("Local binding package absent from root Catalog")
    return paths, texts, catalog, sources, packages, ais


def hub_prepare_root_selection():
    """Supply authoritative root inputs, never semantic decisions or leaf inventories."""
    paths, texts, catalog, _, packages, _ = _root_context()
    return {
        "semantic_task": ROOT_TASK,
        "local_binding_boundary": LOCAL_ROOT_BOUNDARY,
        "controls": [_control_identity(cid, path, text)
                     for cid, path, text in zip(ROOT_CONTROL_IDS, paths, texts)],
        "result_schema": copy.deepcopy(t9.ROUTE_SCHEMA),
        "local_binding_context": [
            {"package_id": pid, "binding_declared": pid in packages} for pid in catalog],
        "availability_scope": "Binding declarations only; package artifacts have not been read or verified",
    }


def hub_validate_root_selection(route_record):
    """Check a host decision against current sources; do not judge semantic applicability."""
    _, texts, catalog, sources, packages, ais = _root_context()
    route = copy.deepcopy(route_record)
    if (not isinstance(route, dict) or set(route) != set(t9.ROUTE_SCHEMA["required"])
        or not isinstance(route["task_scope"], str)
        or not isinstance(route["selected_packages"], list)
        or not isinstance(route["unresolved_blockers"], list)
        or not all(isinstance(v, str) for v in route["unresolved_blockers"])):
        raise ValueError("Invalid root structured record; no fallback/retry")
    selected_ids = []
    # Validate the complete record before any selected-artifact reads.
    for selection in route["selected_packages"]:
        if (not isinstance(selection, dict) or set(selection) != set(t9.ROOT_FIELDS["required"])
            or not all(isinstance(v, str) for v in selection.values())):
            raise ValueError("Invalid root selected identity")
        pid = selection["package_id"]
        identity = catalog.get(pid)
        if (identity is None or pid in selected_ids
            or any(selection[k] != identity[k] for k in ("entrypoint_module_id", "runtime_role", "version"))
            or selection["declared_source_path"] != sources.get(pid, "")):
            raise ValueError("Root identity/version/source mismatch or duplicate selection")
        selected_ids.append(pid)
    availability = []
    blockers = list(route["unresolved_blockers"])
    for pid in selected_ids:
        item = {"package_id": pid, "available": False}
        try:
            if pid not in packages:
                raise ValueError("local-runtime unavailable; no local binding; no fallback/emulation")
            if pid == t9.AIS:
                t9.validate_ais_catalog(texts[3], catalog[pid], sources.get(pid))
                t9.retrieve_pair(ais)
            else:
                entry = packages[pid]["entrypoint"]
                identity = catalog[pid]
                if identity["status"] != "ACTIVE" or any(
                    entry[k] != identity[root_key] for k, root_key in (
                        ("module_id", "entrypoint_module_id"), ("runtime_role", "runtime_role"),
                        ("version", "version"))
                ):
                    raise ValueError("Local binding/Catalog identity mismatch")
                host.t7_retrieve(entry)
            item.update(available=True, reason="Selected entrypoint (AIS pair if selected) read and SHA-256 verified")
        except (ValueError, KeyError, IndexError) as exc:
            item["reason"] = str(exc)
            blockers.append(f"{pid}: {exc}")
        availability.append(item)
    return {
        "record_valid": True,
        "validation_scope": "Shape and current Catalog identity/binding only; semantic applicability is host-owned",
        "route_record": route,
        "selected_package_ids": selected_ids,
        "selected_package_availability": availability,
        "unresolved_blockers": blockers,
        "availability_scope": "Selected root entrypoints only; no local catalogs/leaves, closure or execution verified",
        "runtime_execution_enabled": False,
    }


def _selected_binding(route_record, package_id, allowed=(t9.t8.TECHNICAL,)):
    # Revalidate explicit host identity on every call; no saved selection or bearer receipt.
    receipt = hub_validate_root_selection(route_record)
    if package_id not in receipt["selected_package_ids"]:
        raise ValueError("Package was not selected in the supplied root record")
    if receipt["unresolved_blockers"]:
        raise ValueError("Root selection blocked: " + "; ".join(receipt["unresolved_blockers"]))
    if package_id not in allowed:
        raise ValueError("Package retrieval outside the bounded MCP proof")
    _, _, catalog, sources, packages, _ = _root_context()
    selection = next(s for s in route_record["selected_packages"] if s["package_id"] == package_id)
    identity = catalog.get(package_id)
    entry = packages[package_id]["entrypoint"]
    if (identity is None or identity["status"] != "ACTIVE"
        or selection["declared_source_path"] != sources.get(package_id, "")
        or any(selection[k] != identity[k] for k in ("entrypoint_module_id", "runtime_role", "version"))
        or any(entry[k] != identity[root_key] for k, root_key in (
            ("module_id", "entrypoint_module_id"), ("runtime_role", "runtime_role"), ("version", "version")))):
        raise ValueError("Current selected binding/Catalog identity mismatch")
    return packages[package_id]


def _artifact_chunk(binding, offset, max_chars):
    if type(offset) is not int or offset < 0:
        raise ValueError("offset must be an integer >= 0")
    if type(max_chars) is not int or not 1 <= max_chars <= ROOT_CONTROL_MAX_CHARS:
        raise ValueError("max_chars must be an integer from 1 to 4000")
    body = host.t7_retrieve(binding)
    if offset > len(body):
        raise ValueError("offset exceeds current total_length")
    text = body[offset:offset + max_chars]
    return {**binding, "verified": True, "total_length": len(body), "text": text,
            "offset": offset, "next_offset": offset + len(text),
            "has_more": offset + len(text) < len(body),
            "validation_scope": "Current identity/binding and full UTF-8 SHA-256 retrieval only; "
                                "not proof of host reading, semantic applicability or answer quality"}


def hub_read_selected_package(route_record, package_id, offset, max_chars=ROOT_CONTROL_DEFAULT_CHARS):
    """Expose only a selected, current, verified Technical entrypoint; never execute it."""
    package = _selected_binding(route_record, package_id)
    return _artifact_chunk(package["entrypoint"], offset, max_chars)


CONCEPT_COMPONENTS = ("entrypoint", "local_catalog")
CONCEPT_TASK = (
    "Read both Concept entrypoint and local_catalog completely from offset 0 through has_more=false, "
    "checking consistent SHA-256 and total_length. Select leaves yourself using the exact core and "
    "Catalog semantics for the current request/history; Python never infers activation/applicability. "
    "Return result_schema; empty selection is valid. Preserve unresolved blockers. "
    "Selection != retrieval != execution; no Authoring/AIS/provider execution."
)


def _concept_interface(route_record):
    package = _selected_binding(route_record, t9.t8.CONCEPT, allowed=(t9.t8.CONCEPT,))
    catalog_text = host.t7_read(host.HUB_CATALOG_PATH)
    local_id = package["local_catalog"]
    try:
        block = catalog_text.split("- package_id: " + t9.t8.CONCEPT + "\n", 1)[1].split("\n- package_id:", 1)[0]
        block = block.split("  local_catalog:\n", 1)[1].split("    location:", 1)[0]
        for key in ("module_id", "package_id", "runtime_role", "status", "version"):
            scalar = f"    {key}: "
            values = [line[len(scalar):].strip("'\"") for line in block.splitlines() if line.startswith(scalar)]
            if values != [{**local_id, "package_id": t9.t8.CONCEPT, "status": "ACTIVE"}[key]]:
                raise ValueError("Concept local Catalog interface identity mismatch")
    except IndexError:
        raise ValueError("Concept local Catalog interface identity mismatch") from None
    host.t7_retrieve(package["entrypoint"])
    local = host.t7_retrieve(local_id)
    identities = host.t7_catalog_identities(local, "entries", "module_id")
    return package, identities


def hub_read_selected_concept_interface(route_record, component, offset, max_chars=ROOT_CONTROL_DEFAULT_CHARS):
    """Read only the selected Concept core or local Catalog, never choose leaves."""
    if not isinstance(component, str) or component not in CONCEPT_COMPONENTS:
        raise ValueError("Invalid Concept component")
    package, _ = _concept_interface(route_record)
    return {**_artifact_chunk(package[component], offset, max_chars),
            "component": component, "semantic_task": CONCEPT_TASK,
            "result_schema": copy.deepcopy(host.LEAF_SCHEMA)}


def _validated_concept_selection(route_record, leaf_record):
    record = copy.deepcopy(leaf_record)
    if (not isinstance(record, dict) or set(record) != set(host.LEAF_SCHEMA["required"])
        or not isinstance(record["selected_leaves"], list)
        or not isinstance(record["unresolved_blockers"], list)
        or not all(isinstance(v, str) for v in record["unresolved_blockers"])
        or not all(isinstance(item, dict) and set(item) == set(host.LEAF_FIELDS)
                   and all(isinstance(v, str) for v in item.values()) for item in record["selected_leaves"])):
        raise ValueError("Invalid Concept leaf structured record")
    package, identities = _concept_interface(route_record)
    selected = {}
    for leaf in record["selected_leaves"]:
        mid = leaf["module_id"]
        identity = identities.get(mid)
        bound = next((a for a in package["leaves"] if a["module_id"] == mid), None)
        if (mid in selected or identity is None or bound is None or identity["status"] != "ACTIVE"
            or leaf["runtime_role"] != identity["runtime_role"]
            or any(bound[k] != identity[k] for k in ("module_id", "runtime_role", "version"))):
            raise ValueError("Concept leaf identity/status/role/version mismatch or duplicate selection")
        selected[mid] = bound
    return record, selected


def hub_validate_concept_selection(route_record, leaf_record):
    """Validate current identities without reading any leaf body or deciding applicability."""
    record, selected = _validated_concept_selection(route_record, leaf_record)
    return {"record_valid": True, "leaf_record": record, "selected_module_ids": list(selected),
            "unresolved_blockers": list(record["unresolved_blockers"]),
            "validation_scope": "Shape and current verified Concept Catalog/binding only; semantic selection is host-owned",
            "runtime_execution_enabled": False}


def hub_read_selected_concept_leaf(route_record, leaf_record, module_id, offset, max_chars=ROOT_CONTROL_DEFAULT_CHARS):
    """Revalidate supplied decisions, then read only an explicitly selected bound leaf."""
    record, selected = _validated_concept_selection(route_record, leaf_record)
    if not isinstance(module_id, str) or module_id not in selected:
        raise ValueError("Concept leaf was not selected in the supplied leaf record")
    if record["unresolved_blockers"]:
        raise ValueError("Concept selection blocked: " + "; ".join(record["unresolved_blockers"]))
    return _artifact_chunk(selected[module_id], offset, max_chars)


@server.list_tools()
async def list_tools():
    tools = [types.Tool(
        name=name, description=description,
        inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
        annotations=types.ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False),
    ) for name, description in (
        ("hub_status", "Inspect local Central Hub runtime mode and read-only MCP process status."),
        ("hub_runtime_inventory", "Inspect current local package availability; never activate or execute packages."),
    )]
    tools.extend(types.Tool(
        name=name, description=description, inputSchema=schema,
        annotations=types.ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False),
    ) for name, description, schema in (
        ("hub_prepare_root_selection", "Get current root control manifest and t9 contract; read all controls via hub_read_root_control before selecting.",
         {"type": "object", "properties": {}, "additionalProperties": False}),
        ("hub_read_root_control", "Read an exact current UTF-8 root control chunk. Repeat from next_offset until has_more=false; compare full-file sha256/length. No retained snapshot.",
         {"type": "object", "properties": {
             "control_id": {"type": "string", "enum": list(ROOT_CONTROL_IDS)},
             "offset": {"type": "integer", "minimum": 0},
             "max_chars": {"type": "integer", "minimum": 1, "maximum": ROOT_CONTROL_MAX_CHARS,
                           "default": ROOT_CONTROL_DEFAULT_CHARS}},
          "required": ["control_id", "offset"], "additionalProperties": False}),
        ("hub_validate_root_selection", "Validate a host-produced root record and selected local bindings; no execution.",
         {"type": "object", "properties": {"route_record": copy.deepcopy(t9.ROUTE_SCHEMA)},
          "required": ["route_record"], "additionalProperties": False}),
        ("hub_read_selected_package", "Read the exact SHA-256 verified selected Technical body in chunks. Supply the host root record each call; no model execution. Read through has_more=false before use.",
         {"type": "object", "properties": {
             "route_record": copy.deepcopy(t9.ROUTE_SCHEMA), "package_id": {"type": "string"},
             "offset": {"type": "integer", "minimum": 0},
             "max_chars": {"type": "integer", "minimum": 1, "maximum": ROOT_CONTROL_MAX_CHARS}},
          "required": ["route_record", "package_id", "offset"], "additionalProperties": False}),
    ))
    for name, description, fields, required in (
        ("hub_read_selected_concept_interface", CONCEPT_TASK,
         {"component": {"type": "string", "enum": list(CONCEPT_COMPONENTS)},
          "offset": {"type": "integer", "minimum": 0},
          "max_chars": {"type": "integer", "minimum": 1, "maximum": ROOT_CONTROL_MAX_CHARS}},
         ["route_record", "component", "offset"]),
        ("hub_validate_concept_selection", "Validate a host-produced Concept leaf record against the current verified interface; no leaf body reads or semantic selection.",
         {"leaf_record": copy.deepcopy(host.LEAF_SCHEMA)}, ["route_record", "leaf_record"]),
        ("hub_read_selected_concept_leaf", "Read only a selected Concept leaf after current root/leaf revalidation, with exact SHA-256 verified chunks. Read through has_more=false before use; no execution.",
         {"leaf_record": copy.deepcopy(host.LEAF_SCHEMA), "module_id": {"type": "string"},
          "offset": {"type": "integer", "minimum": 0},
          "max_chars": {"type": "integer", "minimum": 1, "maximum": ROOT_CONTROL_MAX_CHARS}},
         ["route_record", "leaf_record", "module_id", "offset"]),
    ):
        tools.append(types.Tool(name=name, description=description,
            inputSchema={"type": "object", "properties": {"route_record": copy.deepcopy(t9.ROUTE_SCHEMA), **fields},
                         "required": required, "additionalProperties": False},
            annotations=types.ToolAnnotations(
                readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)))
    return tools


@server.call_tool()
async def call_tool(name, arguments):
    concept_calls = {
        "hub_read_selected_concept_interface": (hub_read_selected_concept_interface, {"route_record", "component", "offset"}, {"max_chars"}),
        "hub_validate_concept_selection": (hub_validate_concept_selection, {"route_record", "leaf_record"}, set()),
        "hub_read_selected_concept_leaf": (hub_read_selected_concept_leaf, {"route_record", "leaf_record", "module_id", "offset"}, {"max_chars"}),
    }
    if name in concept_calls:
        function, required, optional = concept_calls[name]
        if not isinstance(arguments, dict) or not required <= set(arguments) or set(arguments) - required - optional:
            raise ValueError("Invalid Concept tool arguments")
        return function(**arguments)
    if name == "hub_read_selected_package":
        if (not isinstance(arguments, dict) or not {"route_record", "package_id", "offset"} <= set(arguments)
            or set(arguments) - {"route_record", "package_id", "offset", "max_chars"}):
            raise ValueError("Expected route_record, package_id, offset and optional max_chars")
        return hub_read_selected_package(**arguments)
    if name == "hub_read_root_control":
        if (not isinstance(arguments, dict) or not {"control_id", "offset"} <= set(arguments)
            or set(arguments) - {"control_id", "offset", "max_chars"}):
            raise ValueError("Expected control_id, offset and optional max_chars")
        return hub_read_root_control(**arguments)
    if name == "hub_validate_root_selection":
        if not isinstance(arguments, dict) or set(arguments) != {"route_record"}:
            raise ValueError("Expected exactly route_record")
        return hub_validate_root_selection(arguments["route_record"])
    if arguments:
        raise ValueError("These read-only tools accept no arguments")
    if name == "hub_status":
        return hub_status()
    if name == "hub_runtime_inventory":
        return hub_runtime_inventory()
    if name == "hub_prepare_root_selection":
        return hub_prepare_root_selection()
    raise ValueError("Unknown tool")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
