"""C2 proof: run M1 root selection through Codex CLI subscription."""
import json

import cli_model
import runtime_host as host
import t9
import m1


def select_root(config, messages):
    """Return a validated M1 root route using Codex CLI instead of Responses API."""
    controls = [host.t7_read(p) for p in (
        host.HUB_CI_PATH, host.HUB_ROUTER_PATH,
        host.HUB_ARCHITECTURE_PATH, host.HUB_CATALOG_PATH,
    )]
    if any(not text.strip() or "\x00" in text for text in controls):
        raise ValueError("C2 CLI: Control rỗng hoặc chứa NUL.")

    binding_text = host.t7_read(t9.BINDINGS_PATH)
    t9.load_bindings(binding_text)
    bindings = json.loads(binding_text)["packages"]
    catalog = host.t7_catalog_identities(controls[3], "packages", "package_id")
    sources = t9.catalog_sources(controls[3])

    instructions = "\n\n".join(controls + [m1.NOTE,
        "Perform semantic TASK_SCOPE and ROOT_PACKAGE_SELECTION only for the current request "
        "and relevant history. Return exact Catalog identities, version and declared_source_path "
        "(empty string when absent). Empty selection is valid. Do not inspect leaf inventories "
        "or suppress applicable packages because their bodies are not yet retrieved. "
        "Expected pending post-selection retrieval of selected package bodies and local catalogs "
        "is not an unresolved blocker. The host retrieves them after root selection. "
        "Report unresolved_blockers only for genuine unresolved conditions, not this normal next retrieval stage."
    ])

    raw = cli_model.call_codex_cli(
        instructions,
        messages,
        model=config.get("model", "gpt-6.1-sol"),
        output_schema=t9.ROUTE_SCHEMA,
    )
    try:
        route = json.loads(raw, object_pairs_hook=t9.unique_object)
    except (ValueError, TypeError):
        raise ValueError("C2 CLI: Root structured không phải JSON hợp lệ.") from None

    if (not isinstance(route, dict) or set(route) != set(t9.ROUTE_SCHEMA["required"])
        or not isinstance(route["task_scope"], str)
        or not isinstance(route["selected_packages"], list)
        or not isinstance(route["unresolved_blockers"], list)
        or not all(isinstance(v, str) for v in route["unresolved_blockers"])):
        raise ValueError("C2 CLI: Root structured không hợp lệ.")

    selected_ids = []
    for selection in route["selected_packages"]:
        if (not isinstance(selection, dict)
            or set(selection) != set(t9.ROOT_FIELDS["required"])
            or not all(isinstance(v, str) for v in selection.values())):
            raise ValueError("C2 CLI: Root selected identity không hợp lệ.")
        pid = selection["package_id"]
        identity = catalog.get(pid)
        if (identity is None or pid in selected_ids
            or any(selection[k] != identity[k] for k in ("entrypoint_module_id", "runtime_role", "version"))
            or selection["declared_source_path"] != sources.get(pid, "")):
            raise ValueError("C2 CLI: Root identity/version/source không khớp Catalog.")
        selected_ids.append(pid)
        if pid not in bindings:
            raise ValueError(f"C2 CLI: {pid} local-runtime unavailable.")

    if route["unresolved_blockers"]:
        raise ValueError("C2 CLI: Root có blocker: " + "; ".join(route["unresolved_blockers"]))

    return route
