# M2 MCP Completion

Date: 2026-11-06

## Scope

M2 proves the minimum host-driven MCP boundary on the current Codex ChatGPT-authenticated host. It does not claim that every Central Hub package lifecycle is portable.

Completed sequence:
- C1: Codex discovers and calls the read-only Central Hub MCP server and reads real local state.
- C2: Codex reads authoritative root controls, performs TASK_SCOPE + ROOT_PACKAGE_SELECTION itself, and Central Hub validates the route.
- C3: after a valid Technical root selection, Central Hub exposes only the selected SHA-256-verified Technical body; Codex reads the whole body and performs semantic reasoning.
- C4: after a valid Concept root selection, Central Hub exposes the verified Concept core and local Catalog; Codex selects leaves from those semantics, Central Hub validates the leaf record, and only validated selected leaf bodies can be read.

MCP remains transport/access only. Python does not parse natural-language applicability and does not call the model on this host-driven path.

## C3 Technical live verification

Outer-host preflight:
- codex.cmd login status: Logged in using ChatGPT.
- OPENAI_API_KEY and CODEX_API_KEY: unset.
- Codex model: gpt-6.1-sol.
- Central Hub transport: local MCP stdio.

Live result:
- Codex read all four root controls and checked manifest identity, SHA-256, total length, and contiguous offsets.
- Root selection: HUB-PKG-TECHNICAL.
- Root blockers: none.
- Complete verified body: HUB-DOM-TECHNICAL, version 1.0, 1867 characters.
- SHA-256: fb42257b74597d5b680e5334cf1a132f04f17eb708a507444da0f3fe4a9f73d4.
- Codex produced the bounded diagnosis only after reading the complete body.
- Central Hub validated identity/retrieval, not prose quality.

C3: LIVE PASS.

## C4 Concept positive live verification

The test request contained an explicit valid /BRAINSTORM ... # control span.

Live result:
- Root selection: HUB-PKG-CONCEPT-DEVELOPMENT.
- Verified Concept core: HUB-DOM-CONCEPT-DEVELOPMENT v1.1, SHA-256 b93c4b3045c5ce980fdc3157d01728f3bd650e0cc4e908c8f89fda3f8346a4b0.
- Verified local Catalog: HUB-CATALOG-CONCEPT-DEVELOPMENT v1.1, SHA-256 eaf480160e055ac7afc12ee4f8d511d09b6828abd14063d85ca571f5e6f03c07.
- Codex itself selected HUB-CAP-BRAINSTORM.
- Central Hub validated the leaf selection against current Catalog/binding identity.
- Selected leaf read completely: HUB-CAP-BRAINSTORM v1.1, SHA-256 3758bf748ab11886656f0ea2a73472323301d14e7bf93bca5767079fea824843.
- Blockers: none.
- Codex produced Concept output only after reading the selected leaf body.

C4 positive: LIVE PASS.

## C4 negative leaf control

A separate session used the same Concept premise with the ordinary phrase "Brainstorm three..." but no valid /BRAINSTORM ... # control span.

Live result:
- Root selection: HUB-PKG-CONCEPT-DEVELOPMENT.
- Codex read the complete Concept core and local Catalog.
- Leaf selection: empty.
- Central Hub accepted the empty leaf record.
- No Concept leaf reader was called and no leaf body was retrieved.
- Blockers: none.
- Codex continued under Concept core/interface semantics only.

C4 negative: LIVE PASS.

## Static verification

Before C3/C4, the full suite had 138 tests.

After C3/C4:
- focused MCP suite: 32/32 PASS
- full repository suite: 152/152 PASS
- py_compile: PASS
- git diff --check: PASS
- no diff in app.py, runtime_host.py, m1.py, t8.py, t9.py, requirements.txt, runtime/, or upstream/.

## Boundary proven by M2

Codex host model
-> Central Hub MCP authoritative controls
-> Codex semantic root selection
-> Central Hub route validation
-> verified selected package/interface retrieval
-> Codex semantic package/leaf selection and execution
-> Central Hub identity/retrieval validation

No new session engine, phase engine, provider registry, automatic fallback, or Python model executor was introduced.

## Explicitly outside M2

Not established by this milestone:
- Authoring admission/contributor lifecycle through MCP
- AIS research/tool lifecycle through MCP
- Anthropic/Claude Code compatibility
- Moonshot/Kimi Code compatibility
- provider-neutral compatibility beyond the current Codex proof
- UI Quick Connect/provider settings
- write-capable MCP tools
- full-system portability claim

Those require separate evidence. M3/provider expansion has not started.
