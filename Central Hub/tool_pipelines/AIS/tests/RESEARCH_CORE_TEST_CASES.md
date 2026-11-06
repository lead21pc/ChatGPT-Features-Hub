# AIS research core — guided research regression cases

STATUS: OFFICIAL_REGRESSION_SPEC / NON_RUNTIME
TARGET: AIS_PIPELINE_v1.1.md + AIS_ROUTER_v1.2.yaml, corrected in place after local promotion.
STATIC CONTRACT TEST: `python -B -m unittest discover -s tests -p test_ais_research_core.py -v` from Hub root.
SPEC SIMULATION: declared depth/coverage/trace fixtures only; no natural-language model interpretation, product launches or external calls.
INDEPENDENT LIVE: NOT_RUN. USER-REPORTED LIVE EVIDENCE: multi-round and broad Chat research, source comparison/counterexamples, workflow-heavy Chat without observed Work handoff, and execution audit distinguishing activity from retrospectively visible source support. These observations are not independent Codex reproduction or proof of deployment of this exact revision.

The original 28 acceptance cases in `ROUTE_TEST_CASES.md` remain unchanged by this correction. This specification supersedes the previous official 34-case research-core specification: automatic lane choice, Work transition/handoff, quota selection and executor-fallback cases no longer describe the accepted AIS architecture. Their removal follows the user's narrowed objective, not an attempt to satisfy old assertions. The remaining research, evidence and execution requirements are retained below. RC IDs here identify this corrected specification, not historical executor-selection fixtures.

| ID | Fixture | Required observable result |
| --- | --- | --- |
| RC01 | Direct search trace; retrospective model denial | Search EXECUTED with trace basis; self-report cannot erase direct execution evidence. |
| RC02 | No direct trace; model asserts executed or not executed | UNKNOWN, never invented NOT_EXECUTED or EXECUTED. |
| RC03 | Visible search, no decisive read; or read without relevant support | Execution, actual reads and claim support remain separate; dependent claim unresolved. |
| RC04 | Bounded delegated question | NORMAL; guided native Chat search/read loop within scope and stop condition. |
| RC05 | Explicit deep/thorough intent; adequate sources/access | At least THOROUGH using ordinary Chat search/read; evidence comparison/counterevidence where material. |
| RC06 | Materially broad question within authorized scope | EXTENSIVE may use repeated ordinary Chat search/read; no product escalation requirement. |
| RC07 | Deep intent expressed semantically, in any language | Raise evidence depth, source/support checks and stopping expectations; no literal trigger parser or answer-length proxy. |
| RC08 | Broad research task | No automatic Deep Research selection, nomination or launch machinery. |
| RC09 | Multi-step research within a larger workflow | No automatic Work selection or Chat-to-Work handoff. AIS researches the delegated portion only. |
| RC10 | Required evidence obtained with adequate support | Stop research and return findings/support/limits to Hub; no research for breadth alone. |
| RC11 | Checkable limit reached with material gaps | Stop and return honest partial coverage/gaps; limit exhaustion is not sufficiency. |
| RC12 | Supported A; decisive gap B | Preserve A, return B unresolved, block dependent conclusions only. |
| RC13 | Search/read tool directly unavailable before submission | Report NOT_EXECUTED for the blocked attempt, preserve evidence and gaps; no fabricated calls. |
| RC14 | Request submitted, then timeout; execution not observable | UNKNOWN; timeout/submission alone proves neither execution nor non-execution. |
| RC15 | Contradictory direct traces for one attempt | CONFLICTED and unresolved; assess different attempts separately. |
| RC16 | Direct non-execution, pre-submission block or unavailable executor | NOT_EXECUTED only for that directly evidenced action/attempt. |
| RC17 | User explicitly requests Deep Research or Work | Respect the explicit request through actual available authorized platform behavior; report limitations without invented launch/transfer or silent substitution. AIS owns no product-launch coordinator. |
| RC18 | Subscription entitlement or forum claim of capability | No claim of current tool availability or execution from those reports alone. |
| RC19 | Tool fails after completed A; B invalidated; C unresolved | Retain A with reads/conditions; re-plan B/C only, keep depth/evidence standard; do not reset valid research. |
| RC20 | Same-question synonym refinement | Retain scope; refine queries when justified; pre-call checks remain. |
| RC21 | Material target or scope expansion | INPUT_VALIDATION; rebuild affected contract/strategy and check Hub authorization before external work. |
| RC22 | Sources support A and B separately, not their relation | No automatic support for A+B; preserve material inference/gap. |
| RC23 | External source conflicts with protected state | Expose conflict; no silent protected-state rewrite or unauthorized update. |
| RC24 | Search/open/find traces remain but decisive readable response is absent; product says verified | Report observed execution; do not reassert inaccessible source contents or dependent claim support. |
| RC25 | Evidence task is part of FSP/IT/another stack activity | Hub selects AIS; AIS returns evidence and yields control. No whole-turn reassessment or unrelated-package orchestration. |
| RC26 | One material question remains, within the locked limit | Continue only for that evidence need; stop at sufficiency/limit and report unmet depth honestly. |

RESEARCH_STRATEGY remains narrowly useful: translate desired depth into evidence coverage after source authority is established. Keep only quality_target/coverage_expectations in research_strategy; use existing question/unknowns, source_authority and stop_condition rather than duplicate fields or a second engine.

For separately authorized live testing record: exact official pair actually loaded, date/model/surface, delegated question and protected state, depth/coverage expectations, actual searches/reads and trace basis, supported findings/conditions, conflicts/gaps, tool/access limits, stop reason, return to Hub and PASS / FAIL / UNVERIFIABLE. Missing observable evidence is UNVERIFIABLE, never a fabricated PASS. Do not request private reasoning. Explicit product requests are assessed against the exposed platform path; do not simulate a launch and report it as live execution.

Static contract tests and synthetic coverage fixtures do not prove guided model behavior, intent interpretation, tool availability or end-to-end stack integration. A prepared live path and a real-context stress test remain distinct evidence levels. Keep the previously resolved Hub routing result scoped; reopen only on new contradictory evidence.
