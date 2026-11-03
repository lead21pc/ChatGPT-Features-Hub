# AIS research core — candidate regression cases

STATUS: CANDIDATE / NON_RUNTIME_SPEC
STATIC CONTRACT TEST: see `tests/test_ais_research_candidate.py` from Hub root.
SPEC SIMULATION: synthetic evidence/availability fixtures only; no model intent interpretation or external calls.
CONTROLLED LIVE: NOT_RUN. REAL-CONTEXT STRESS: NOT_RUN.

These extend, rather than replace, the unchanged 28 cases in `../../tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md`. AIS-22's exact missing-router case remains an active-baseline test; a candidate trial separately requires the exact candidate router. No older acceptance criteria are relaxed.

| ID | Fixture | Expected observable behavior |
| --- | --- | --- |
| RC01 | Direct UI/tool search trace; retrospective model says no search | EXECUTED for that search; preserve trace basis/attribution; self-report cannot erase it. |
| RC02 | Trace unavailable; model asserts executed or not executed | UNKNOWN; no inference from missing trace or self-report. |
| RC03 | Visible search; no decisive source read | Search EXECUTED; source read and claim support remain unestablished. |
| RC04 | Narrow bounded evidence task | NORMAL, CHAT_GUIDED with decisive read/support loop. |
| RC05 | Broad deep synthesis; observed usable Deep Research path and resources | EXTENSIVE; prefer DEEP_RESEARCH for material breadth benefit; selection proves no launch. |
| RC06 | Files/apps/browser plus dependent transformations and deliverable; Work available | Prefer WORK; retain source/support discipline. |
| RC07 | Unknown quota; bounded task | CHAT_GUIDED; quota remains UNKNOWN. |
| RC08 | Explicit deep request; material benefit; actual high-capacity path available | Raised quality target; eligible high-capacity lane, subject to authorization/native UX. |
| RC09 | Deep Research preferred/selected; no actual launch path | No fabricated call; distinguish preferred/feasible/observed executor; use allowed fallback or stop. |
| RC10 | Expensive lane fails after supported branch A; branch B unresolved | Retain A and its actual reads; re-plan B only; disclose coverage effect. |
| RC11 | Work only has same Project context plus separate-task launch path | Bounded handoff with all eight fields; no same-thread/full-history claim. |
| RC12 | Direct task-scoped Chat -> Work affordance on surface S | Permit that transition on S only; do not generalize to other surfaces/history transfer. |
| RC13 | Forum report alone says Work/Deep Research is available | No runtime availability/launch-path claim; UNKNOWN; bounded fallback. |
| RC14 | User requests quota conservation | Prefer CHAT_GUIDED while preserving raised quality target and disclosing unmet breadth. |
| RC15 | Work/Deep Research says verified; decisive readable evidence missing | Dependent claim remains unresolved regardless of label. |
| RC16 | Pure broad research; both lanes available | Prefer DEEP_RESEARCH, not WORK merely for being agentic. |
| RC17 | Workflow-heavy research; both lanes available | Prefer WORK, not DEEP_RESEARCH merely for specialization. |
| RC18 | Resources exhausted with supported branch A already complete | Exclude exhausted lane; preserve A; reduce achievable breadth, never evidence standard. |
| RC19 | Synonym refinement within unchanged question/conditions/target | Retain scope lock; refine query; pre-call checks still apply. |
| RC20 | Material target expansion or replacement | INPUT_VALIDATION; rebuild affected contract/strategy and check Hub authorization before external work. |
| RC21 | Conflicting direct executed/non-executed traces for the same attempt | CONFLICTED, unresolved; preserve both. Different attempts must be assessed separately. |
| RC22 | Direct non-execution, pre-submission block or unavailable executor | NOT_EXECUTED only for the directly evidenced attempt; earlier searches unaffected. |
| RC23 | Submitted request times out; no execution trace | UNKNOWN; submission/timeout proves neither execution nor non-execution. |
| RC24 | Named executor unavailable; fallback forbidden | Stop dependent work with explicit limitation; no silent executor substitution. |
| RC25 | Explicit depth + actual path but quota UNKNOWN / LOW | UNKNOWN stays unknown; LOW permits only justified bounded attempt with fallback. No plan-entitlement inference. |
| RC26 | CHAT_GUIDED also unavailable; preferred expensive lane unusable | No fabricated fallback call; stop unresolved dependent branches; retain supported work. |

Controlled live testing requires separate authorization and an isolated compatible test stack, with explicit candidate admission for this pair. Do not edit/upload/promote the active Hub stack as part of local tests. Keep all 28 baseline cases as regression obligations; prepared fixtures do not prove real-context behavior.

For each authorized live case record: case ID, date/model/surface/Project, exact candidate pair actually read, task portion and protected state, quality target/reason, preferred/selected executor, observed availability/resource evidence, actual launch/transition evidence, per-action EXECUTED / NOT_EXECUTED / UNKNOWN / CONFLICTED and basis, actual decisive reads/citations/support, completed/unresolved branches, fallback and material coverage effect, result PASS / FAIL / UNVERIFIABLE. Missing observable evidence is UNVERIFIABLE, never an invented PASS. Do not request private reasoning.

First controlled group: RC01–RC03/RC21–RC23 for execution evidence; RC04–RC09/RC13–RC17 for strategy; RC10–RC12/RC18–RC20 for evidence retention and transitions. Inject unavailable/exhausted states as declared fixtures when no safe actual failure path exists, and label those SPEC SIMULATION rather than live platform verification. Test unexposed lanes as UNKNOWN/UNAVAILABLE, not as launched.

Stable-enough criteria: static contract checks pass with unchanged active baselines; then authorized controlled cases satisfy observable criteria or explicitly retain unavailable-path limits; then a real-context conversation tests discussion -> research -> discussion plus fallback/reporting under accumulated context. Passing a prepared path alone does not establish real-context stability. Keep the resolved Hub routing rerun as user-reported prior evidence; reopen only on new contradictory routing evidence.
