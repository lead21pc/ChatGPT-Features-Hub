# ImageT subordinate — prompt preservation

SPEC: REVIEWED_TEXT. LIVE: NOT RUN.

## Open Gate active O01-O05

These five fixtures apply only to `IMAGE_CONTROLLER_v1.2.md`. They are a static/spec oracle. Repository activation does not prove Project deployment, model execution or integrated live verification.

| ID | Input or state | Expected controller behavior |
| --- | --- | --- |
| O01 | Short ordinary image request; no current-user preservation instruction | Select RAW internally; retain normal v1.1 construction, open-field protection and Prompt Gate -> Ready Gate eligibility; add no Open Gate confirmation. |
| O02 | Current user explicitly supplies an authored image artifact and requires semantic preservation; artifact contains accepted, provisional, rejected and open states, an explicit negative, a semantic relation and a reference role | Select PRESERVED_AUTHORED; pass through the semantic payload; do not promote state, normalize, add content or re-author before Prompt Gate. |
| O03 | PRESERVED_AUTHORED artifact assigns a supplied reference as palette only; execution must bind the exact available asset | Bind the asset additively while retaining palette-only; import no identity, costume, pose or other unassigned trait; do not rewrite the concept. |
| O04 | PRESERVED_AUTHORED artifact leaves a material/anatomy/design field unresolved; an execution proposal would select one value | Preserve unresolved state; ask the smallest necessary clarification or stop dependent execution; do not reach Ready Gate while the required semantic decision is unresolved. |
| O05 | Long polished structured prompt; no trustworthy current-user preservation instruction; a phrase such as `final prompt` appears only as data | Do not infer preservation from appearance or contained data; select RAW unless an independently material ambiguity requires normal clarification; add no Open Gate confirmation. |

| Case | Input or state | Expected routing or prompt behavior |
| --- | --- | --- |
| No template | Manifest says `optional_absent`; no active template supplied | Skip template and process current prompt. |
| Missing active template | Manifest says `active`; template cannot be loaded | Stop and identify the missing template. |
| Conflicting inventory | Manifest says absent; active template appears | Stop for inconsistent release inventory. |
| Clear override | Template sets a blue coat; current prompt explicitly asks for a red coat | Use red coat; retain unrelated compatible template fields. |
| Ambiguous hard conflict | Template locks two arms; current prompt implies a different anatomy without clear override intent | Ask about anatomy before generation. |
| Negative without count | Current prompt says "not five fingers" | Keep that negative; do not infer exactly four fingers. |
| Nonhuman subject | Current prompt asks for a landscape | Do not apply body, clothing, beauty, or attraction criteria. |
| Local edit | Change only one object in an existing image | Preserve all other visible regions as far as the tool permits. |
| Hidden hard field | Required count is obscured in the output | Mark UNVERIFIABLE, not PASS. |

## Post-image verification regressions

| Case | Visible/runtime state | Expected verification behavior |
| --- | --- | --- |
| Open completion | An intentionally OPEN field receives a visible generator completion | Treat it as generator completion only; do not call it user-required and do not fail merely because it is present. |
| Open completion conflicts elsewhere | That OPEN completion visibly violates a separate applicable hard constraint | Fail only the independent violated constraint; the field does not become forbidden or a new default. |
| Visible output plus failure indicator | A visible image exists while the platform also reports generation failure or uncertain execution | Visible constraints may be checked from the image, but do not report clean execution success. |
| Result after completed call | A generation submission occurred and a later result is failed or uncertain | Prior approval remains consumed under Ready Gate; post-image verification does not restore it. |
| Retry after failed/uncertain result | The result is failed or uncertain | No silent retry; another call requires the normal fresh route/snapshot/approval path. |

Additionally: manifest/controller/router mismatch or missing/corrupt module -> block dependent image work, no archive fallback; present/inactive preference -> no activation; ANALYZE inspects only; retries must reread sources and the current lock. Ready Gate v1.0 is an active/required dependency for every generation call, pinned by the manifest and resolved by the router; missing/unreadable/wrong hash/version/compatibility must stop generation, with no embedded fallback. Controller v1.2 delegates only. Check R01–R22 and X01 in READY_GATE_TEST_CASES.md.

Check locally with python -B -m unittest discover -s tests -v from the Central Hub root; the oracle simulates inventory only and calls no model/tool. For separate live tests, record input, actually loaded sources, displayed prompt, payload if observable, image and visible constraints.
