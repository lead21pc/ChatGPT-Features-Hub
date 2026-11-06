# Authoring M4 — preset strategy candidate

## Current closure — 2026-11-02

M4 COMPLETE. AUTHORING 0.6 REPOSITORY BASELINE STABLE. Current production artifacts: library_modules/HUB-CAP-AUTHORING_v0.6.md, HUB_PACKAGE_CATALOG_v1.7.yaml and HUB_ARCHITECTURE_v1.7.md, with Router 1.1 exact pins only updated and CI 1.1 unchanged. Preset policies are unchanged from the tested candidate. No-preset and bounded composition remain intact; no additional preset mechanism or M5.

The candidate was originally ca70b28 on the FTH branch and published independently as equivalent f363546. With explicit approval main was fast-forwarded to f363546; FTH's private branch was not rewritten or merged. Architecture 1.6 sections 6/8 and Router contracts require exact 1.6 Catalog/stack bindings; the user approved the minimum 1.7 successor/pin changes after this concrete constraint was reported. This is not version symmetry or an algorithm redesign.

L1 and L2 now have USER_CONFIRMED_LIVE_PASS / SUPPLIED-CANDIDATE LIVE BEHAVIOR with user-reported exact candidate identities and FULL_FILE receipts. L1 used a Devil's Advocate operating contract and passed P2 relational preservation; L2 passed without a preset. See AUTHORING_M4_TESTS.md and ../../RUNTIME_EVIDENCE_CHANGELOG.md for scope/provenance. The original campaign fixture was not claimed run. Active 0.6 Hub routing NOT_RUN; production Library identity/deployment NOT_VERIFIED. REPOSITORY BASELINE STABLE != ACTIVE CENTRAL HUB RUNTIME VERIFIED.

The verified controls and 0.5 predecessor/compatible stack are archived byte-exact under ../../Source_archive/Authoring 0.6 promotion 2026-11-02/. The original candidate implementation snapshot below retains its old status statements as history. Post-promotion static verification is recorded after execution in AUTHORING_PROMOTION.md and the runtime evidence log. No push, deployment, tag or CURRENT handoff edit.

## Original candidate implementation snapshot

Status: M4 CANDIDATE READY FOR LIVE SMOKE. Date: 2026-11-02 (Asia/Bangkok). This is an explicitly reopened workstream after M1 CLOSED / M2 CLOSED / M3 COMPLETE, not unfinished baseline work.

## Verified baseline and gap

Repository: lead21pc/ChatGPT-Creative-Workshops. Branch: fth/router-6.0-lock. Pre-M4 HEAD: 1e2e041af21a4ad08033b1317ee24b5e6ba442ab. Worktree and index were clean. Cached origin/main and read-only remote refs/heads/main both resolved to 6db0291d350a336774b31bd5ed1793e40684dc25. The current branch was ahead by one existing FTH commit; that commit is unrelated to M4 and is not republished or rewritten here. Keep the shared checkout.

Production baseline remains Hub CI 1.1 / Router 1.1 / Architecture 1.6 / Root Catalog 1.6 / Authoring ACTIVE 0.5. The source confirms source-prompt rewrite/reauthor, context/provenance/decision preservation, target adaptation and bounded composition, but no explicit preset selection. Strategies can already be expressed in user instructions; M4 supplies bounded user-selected strategies without requiring the user to articulate every preservation dimension. No reproduced 0.5 failure or reopening of its closed evidence is implied.

## Candidate implementation and admission ownership

- [Authoring 0.6 candidate](<../../Source_archive/Authoring 0.6 promotion 2026-11-02/candidates/authoring_m4/HUB-CAP-AUTHORING_v0.6-candidate.md>): same singleton identity/role, CANDIDATE / 0.6-candidate. Adds only the inline optional preset-strategy section, plus candidate header/admission wrapper. All existing behavior after the admission wrapper is inherited exactly when that new section is removed.
- [Root Catalog 1.7 candidate](<../../Source_archive/Authoring 0.6 promotion 2026-11-02/candidates/authoring_m4/HUB_PACKAGE_CATALOG_v1.7-candidate.yaml>): full test-only copy of the current root metadata, with CANDIDATE/non-ready wrapper and only Authoring's applicability/version/status/retrieval notice changed. Other package entries and their historical evidence are inherited unchanged; they are not fresh verification results.
- [T0–T3 and exact L1/L2 packet](AUTHORING_M4_TESTS.md): local reference transformations, relational counterexample and later live instructions.
- [Focused static/spec tests](../../tests/test_authoring_m4.py): eight tests, no runtime parser or model invocation.

Disposition: ACCEPT WITH LOCAL CORRECTION. Root selection precedes the Authoring body, so changing only the module would leave presets unadmitted. Represent the expanded syntax in this isolated candidate Catalog view. Do not expand the ACTIVE 1.6 Catalog to admit a candidate or add a second production entrypoint. Existing Router eligibility explicitly permits test-only metadata simulation and excludes candidates from normal runtime; Architecture already permits separately authorized candidate testing. This needs no Architecture successor, pin change or Router copy/algorithm modification for candidate testing. Separate future production promotion would require a compatible accepted Catalog/Architecture and exact Router pin update; this task performs none of them.

This Catalog is the existing root selection mechanism represented for testing, not a Preset Catalog or new package-local catalog. Production pins remain exactly 1.6, and ACTIVE 0.5 remains the single known-safe production revision. No predecessor is superseded, removed or archived: a parallel candidate does not trigger predecessor archival. Existing archive byte checks remain in the full suite.

## Preset contract

Exact optional syntax: `/AUTHOR <OUTPUT_TARGET> P<n>`, where the five existing targets remain AIS, IMAGET, CODEX, WORK and GENERIC, and the suffix is exactly P1, P2 or P3. Keep case, one ASCII space, first non-empty user-authored line, source provenance and per-turn activation rules. Existing singles and `/AUTHOR <OUTPUT_TARGET> + <CONTRIBUTOR>` remain unchanged. Any preset + contributor form is non-activating.

- P1 — CLEAN: improve a fundamentally correct source prompt through local wording/organization cleanup and true redundancy removal, preserving material behavior, state, constraints and authority. Cleanup does not authorize redesign.
- P2 — CONTRACT: preserve long-running operating semantics, authority/agency/knowledge/state/change boundaries and material relations between constraints. Retaining each endpoint is insufficient if their relation is lost. Per-turn Authoring can produce a cross-turn downstream contract; persistence is not immutability.
- P3 — REBUILD: allow substantial restructuring of a poorly organized source while retaining supported intent, useful mechanisms, material constraints/state and authority. Full rewrite permission does not authorize intent replacement or project-state changes.

PRESET != TARGET. PRESET != CONTRIBUTOR. PRESET != AUTHORITY. PRESET != PERSISTENT MODE. TARGET BOUNDARY > PRESET STRATEGY. No suffix retains adaptive 0.5 behavior: no inferred preset, preset report or preset-selection question. Definitions and policies are English-only and reside directly in Authoring.

No Preset Catalog, Preset Registry, Preset Router, new package, persistent mode, dynamic discovery, user storage, preset recommendation, preset inheritance, N-way composition or preset + contributor support was added. Hub CI, Router, Architecture, all active modules/pipelines and other projects remain unchanged.

## Verification and limits

Baseline full Hub suite: 183/183 PASS. M4 syntax/identity/pins/integrity and T0–T3 fixed-fixture checks: 8/8 PASS. Focused Authoring suite: 22/22 PASS. Full Hub static suite: 191/191 PASS. YAML parsing, candidate/active binding separation, one active production Authoring revision, byte-exact active stack, inherited behavior/target rows, existing predecessor/archive checks, UTF-8/LF/no BOM, whitespace and scoped git diff checks pass.

T0: no-preset local reference regression checked. T1: CLEAN local reference checked. T2: CONTRACT reference preserves source relationships; flattened and single-relation-loss counterexamples are rejected by focused fixture assertions. T3: REBUILD reference preserves useful mechanism, state and permission boundaries while removing unnecessary structure. These are LOCAL SPEC SIMULATION / REVIEWED_TEXT with automated checks on fixed artifacts, not observed model compliance. The relation checks are specific to this fixture and do not evaluate arbitrary paraphrases or prove general semantic preservation.

L1/L2: NOT_RUN. The exact minimal messages and test-only setup are in AUTHORING_M4_TESTS.md. They compare GENERIC P2 with GENERIC on equivalent operating-contract input, without adding a preservation checklist to the request. No P1/P3 live smoke is required for symmetry. Supplied-control candidate live evidence must not be labeled active Central Hub routing or Library identity verification. Authoring 0.5 user-confirmed scoped live PASS and deployment report remain unchanged in the canonical runtime evidence changelog.

## Git and stop boundary

Only M4-owned paths are staged and committed locally after verification. No push, deployment or promotion is authorized. The branch's pre-existing FTH commit remains outside this task's ownership. Stop at M4 CANDIDATE READY FOR LIVE SMOKE; no additional milestone or preset infrastructure is proposed.
