# MCP Status

Date: 2026-11-06

Status: DORMANT

The existing MCP implementation and verification evidence are preserved unchanged.
MCP is not the current execution path and is not an acceptance dependency for the CLI-wrapper work.
No new MCP routing, orchestration, package surface, or host-entry behavior should be added while this status is active.

Current reason: ordinary Codex requests can bypass Central Hub MCP and use native host capabilities before entering Hub. Existing C1-C4 MCP evidence remains valid only for the previously verified host-driven/scripted scope.

Active direction: keep the verified M1 orchestration as the mandatory entry and test Codex CLI subscription as an alternative model transport before considering any MCP revival.

Reactivation requires an explicit later decision after the CLI-wrapper path has been evaluated.
