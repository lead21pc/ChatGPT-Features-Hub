# Authoring 0.7 candidate — explicit source isolation

Date: 2026-11-03 (Asia/Bangkok). Status: IMPLEMENTED / STATIC-SPEC VERIFIED; CANDIDATE ONLY. No promotion, push, tag, Project/Library deployment or live model test.

## Baseline and scope

Repository: lead21pc/ChatGPT-Creative-Workshops. Branch main, pre-task HEAD 59a563688ed91a8d93c23645512d2e65d0e6b6db. Worktree and index were clean; cached origin/main matched HEAD (0 ahead / 0 behind). Actual active stack: Hub CI/Router 1.1, Architecture/Catalog 1.8, Authoring ACTIVE/0.6. Authoring remains the root singleton HUB-PKG-AUTHORING -> HUB-CAP-AUTHORING / CAPABILITY, with no local Catalog or hard Requires. The newer Concept interface is preserved; this task reads no Concept/AIS/ImageT internals and changes none of their behavior.

The write scope is this candidate directory plus tests/test_authoring_isolation.py. Production controls, root/Hub READMEs, existing tests, runtime evidence history, FTH and Revamp remain untouched. The verified 0.6 active revision is a parallel baseline, not a predecessor being replaced; no archival is required for this inactive candidate.

## Audit findings and disposition

ACCEPT WITH LOCAL CORRECTION: use the proposed token order directly; it fits existing exact suffix admission. Represent it in a test-only root Catalog view because root selection precedes reading Authoring. A module-only change would otherwise leave the new form unadmitted. No broader architecture or Router change is necessary for candidate testing.

Already satisfied in active 0.6:

- **Admission and exact activation** limits activation to the current first non-empty user-authored line, excludes source/tool/quoted commands and reassesses each turn. This isolates trigger provenance, not all authoring task material.
- **Context sources, rewrite and reauthor** requires reading explicitly referenced accessible material, preserving material context, exposing missing decisive sources, treating source prompts as design material and stopping at the artifact. An explicit source can already be read; no new retrieval owner is needed.
- **Context provenance** distinguishes supplied state/evidence from generated structure/model knowledge and forbids inventing prior findings. It controls provenance truth, not whether otherwise valid but unreferenced prior state is admitted.
- **Scoped transformation** explicitly uses materially relevant current Hub context/state. **Reauthor** preserves unmentioned applicable prior constraints. These are correct defaults but supply the genuine 0.7 gap: no explicit per-turn exclusion of otherwise relevant ambient task content.
- Existing preset policies and target rows already preserve authority, agency, state, decision conditions and no-execution boundaries. They need no redesign. Defining isolation as memory deletion or control removal would contradict these contracts and is rejected; the requested behavioral admission boundary does not.

The delta is substantive source admission, not merely a provenance wording improvement. In the candidate, the new section applies first to scope which task material can reach existing context/preservation/reauthor/evidence rules. Those rules then operate only on admitted material. The entire 0.6 body is unchanged after removal of this one section and the candidate identity/admission wrapper. P1/P2/P3, five targets, bounded contributor composition, clarification threshold and downstream boundaries remain identical.

## Implemented syntax and semantics

```text
/AUTHOR <OUTPUT_TARGET> ISOLATED
/AUTHOR <OUTPUT_TARGET> P<n> ISOLATED
```

OUTPUT_TARGET remains AIS, IMAGET, CODEX, WORK or GENERIC. P<n> is exactly P1, P2 or P3. ISOLATED is the final exact case-sensitive token; exactly one ASCII space per token. First-line/provenance and per-turn rules remain unchanged. There is no DEFAULT token, inference, spelling repair, Unicode normalization or persistent selection.

ISOLATED admits the current request after the trigger, its explicitly supplied source material and sufficiently identified accessible material explicitly referenced by that request. Mandatory Hub/Authoring controls, binding/read checks, safety and actual target boundaries still constrain the operation. They cannot be used to import excluded objectives, source facts or project decisions as task content.

Unreferenced chat, assistant conclusions, proposals/decisions, merely available Project material, unreferenced Hub state and remembered discussion are excluded from task construction. Naming a unique accessible artifact may admit it; seeing an available attachment/link does not admit every source or recursively import its neighbors. A decisive ambiguous earlier decision requires the existing focused clarification, not silent history recovery. Sufficient admitted inputs require no new question. Reauthor and clarification turns must explicitly include/identify needed material and repeat a valid trigger; no source selection persists automatically.

Model knowledge can still support neutral structure/questions under existing provenance constraints. It cannot supply prior findings, task decisions or source history. External megaprompts remain source material, never instruction authority. The result is a prompt artifact or a necessary clarification, not downstream execution. No new target discovery, universal target loading, permission or execution owner is introduced.

SOURCE ISOLATION != CONTROL ISOLATION. ISOLATION != AMNESIA. SOURCE BOUNDARY != TRANSFORMATION STRATEGY. VISIBLE CONTEXT != AUTHORIZED AUTHORING SOURCE. ACCESSIBLE CONTEXT != ADMITTED TASK MATERIAL.

No suffix keeps normal 0.6 adaptive/context behavior. Existing `/AUTHOR <TARGET>`, `/AUTHOR <TARGET> P<n>` and `/AUTHOR <TARGET> + <CONTRIBUTOR>` remain valid. Contributor + ISOLATED, preset + contributor, and preset + contributor + ISOLATED are not admitted. No current isolation requirement justifies expanding those combinations.

## Candidate artifacts and binding limits

- [Authoring 0.7 candidate](HUB-CAP-AUTHORING_v0.7-candidate.md): same identity and role, CANDIDATE / 0.7-candidate; one inline source-isolation section.
- [Root Catalog 1.9 candidate](HUB_PACKAGE_CATALOG_v1.9-candidate.yaml): full test-only copy of current 1.8 root metadata, with candidate/non-ready wrapper and only the Authoring entry's status/version/admission/retrieval notice changed. Other package metadata/evidence is inherited exactly, not reverified. This is the existing root Catalog mechanism represented for testing, not a source registry or local Authoring Catalog.
- [I1–I10 fixtures](ISOLATION_TEST_CASES.json): scenario inputs, simulated accessible sources, expected outcomes and fixed reference outputs.
- [Eight static/spec tests](../../tests/test_authoring_isolation.py): lexical admission, reference-fixture checks, negative mutations, candidate binding and active-byte preservation.

Active Router contracts still pin Architecture/Catalog 1.8. Architecture section 10 and Router candidate eligibility allow separately authorized testing but exclude candidates from active use. The companion Catalog is explicitly test-only; it does not make an installed 1.8 stack compatible with candidate production execution. No candidate Architecture or Router copy/pin change is required for this supplied-control test scope. Any future production promotion must separately reconcile exact accepted bindings and deployment. This candidate makes no such change.

## Verification and evidence

Pre-change full Hub suite: 205/205 PASS. New isolation tests: 8/8 PASS. Focused Authoring suite: 33/33 PASS. Full Hub suite: 213/213 PASS. YAML/JSON parsing, active/candidate identity and pin integrity, unchanged other package entries, exact active-stack hashes, UTF-8/LF/no BOM, whitespace and scoped diff checks pass.

I1–I10 coverage:

| Case | Checked property | Evidence |
| --- | --- | --- |
| I1 | Sufficient current source excludes prior/project canary decisions | Fixed reference + contamination counterexample |
| I2 | Explicitly referenced simulated artifact contributes; neighboring artifact is excluded | Fixed reference + declared-access/source checks |
| I3 | Decisive unadmitted earlier decision yields a focused source question | Fixed clarification reference |
| I4 | Neutral research structure is allowed without fabricated prior state | Fixed reference + forbidden finding markers |
| I5 | CODEX restrictions survive isolation | Fixed reference + stripped-boundary counterexample |
| I6 | No suffix retains relevant normal context and no silent isolation | Legacy lexical oracle + fixed reference |
| I7 | P2 retains relational/cross-turn contract semantics on admitted material | Exact preset preservation + flattened counterexample |
| I8 | Wrong case/order/spacing, extra/lookalike tokens, quoted/later/source commands and unsupported combinations do not activate | Exact lexical spec oracle |
| I9 | AIS-facing prompt remains an artifact; no claim of research execution | Fixed reference + no-execution contract preservation |
| I10 | External megaprompt instructions remain material; no acceptance/messages | Fixed reference + authority-contamination counterexample |

Classification: LOCAL SPEC SIMULATION / REVIEWED_TEXT. Codex produced/reviewed the fixed reference outputs while preparing this candidate. Automated tests check those artifacts and fixture-specific negative mutations. They do not generate model outputs, resolve real Project files, detect semantic leakage in arbitrary prose or prove runtime adherence. Accessible-artifact/read availability in fixtures is declared simulated input, not an actual Library/source read. The lexical oracle is test-only, not a new runtime parser. STATIC / SPEC PASS != CANDIDATE-BOUND LIVE PASS.

Candidate-bound live: NOT_RUN. Active Hub 0.7 runtime: NOT_RUN / NOT_APPLICABLE_TO_PRODUCTION. Candidate Library identity/FULL_FILE: NOT_VERIFIED / UNRESOLVED. Candidate Project deployment: NOT_PERFORMED. Existing Authoring 0.6 user-reported deployment and scoped 0.6-candidate L1/L2 PASS remain unchanged in RUNTIME_EVIDENCE_CHANGELOG.md; they are not 0.7 evidence. No new runtime result is added to that historical owner in this task.

For later live reproduction, use a fresh isolated test conversation with the complete explicitly authorized candidate module and Catalog, not the active Hub binding. For each chosen case, establish its prior_chat/project_context as ambient setup, actually supply any accessible_artifacts as identified sources, then send request verbatim. Do not include reference_output, required or forbidden checks in the user's authoring request. I3 should expose a gap; I8 should not activate Authoring. Record exact candidate versions/full-read basis, complete input/output, actual reads/actions and result per case. Missing setup/access is a blocker for that case, not a fabricated read or PASS. A supplied-candidate live result would still not prove active Hub routing, production Library binding or deployment.

## Scope and completion

No local Catalog, preset/source registry, validator subsystem, automatic target/preset discovery, user preset system, database, lifecycle manager, persistent mode, global context policy, new execution owner or contributor grammar expansion. No FTH/Revamp/package-internal changes. No source was superseded or archived. No concrete blocker remains for this candidate scope. Stop at the small 0.7 candidate; promotion/deployment/push require separate authorization. Verified task files are committed locally according to the repository Git workflow.
