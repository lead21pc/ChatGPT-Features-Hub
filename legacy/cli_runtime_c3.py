"""C3 proof: natural request -> CLI root -> verified Technical retrieval -> CLI semantic answer."""
import json

import cli_model
import cli_root
import runtime_host as host
import t8
import t9
import m1


def call_c3(config, messages):
    """Run the bounded C3 Technical path entirely through Codex CLI subscription."""
    route = cli_root.select_root(config, messages)
    selected = route["selected_packages"]
    if [item["package_id"] for item in selected] != [t8.TECHNICAL]:
        raise ValueError("C3 CLI: test path requires Technical as the only selected package.")

    binding_text = host.t7_read(t9.BINDINGS_PATH)
    t9.load_bindings(binding_text)
    bindings = json.loads(binding_text)["packages"]
    technical = bindings[t8.TECHNICAL]["entrypoint"]
    body = host.t7_retrieve(technical)

    controls = [host.t7_read(p) for p in (
        host.HUB_CI_PATH, host.HUB_ROUTER_PATH,
        host.HUB_ARCHITECTURE_PATH, host.HUB_CATALOG_PATH,
    )]
    instructions = "\n\n".join([
        controls[0],
        m1.NOTE,
        "[C3 VERIFIED ROOT ROUTE]\n" + json.dumps(route, ensure_ascii=False),
        "[C3 VERIFIED TECHNICAL RETRIEVAL]\n" + json.dumps({
            key: technical[key] for key in ("module_id", "runtime_role", "version", "sha256")
        }, ensure_ascii=False),
        body,
        "Execute only the verified Technical application_scope for the original user request. "
        "Preserve competing hypotheses and uncertainty where evidence is missing. "
        "Return the final user-facing answer. Do not invoke other packages or claim tools ran.",
    ])

    answer = cli_model.call_codex_cli(
        instructions,
        messages,
        model=config.get("model", "gpt-6.1-sol"),
    )
    trace = {
        "root_selected_package_ids": [t8.TECHNICAL],
        "retrieved_module_ids": [technical["module_id"]],
        "retrieval_verified": True,
        "final_transport": "CODEX_CLI_SUBSCRIPTION",
    }
    return answer, trace
