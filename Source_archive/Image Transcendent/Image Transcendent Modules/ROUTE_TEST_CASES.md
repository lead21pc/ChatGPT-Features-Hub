# Route and prompt-preservation cases

These are review cases, not evidence that a ChatGPT Project or image generator has passed. Keep the model, Project instructions, active Sources, and other conditions constant when running comparisons.

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

For each live case, record the original user prompt, active versions, tool-facing prompt when observable, result image, verified constraints, defects, and uncertainty. Do not interpret a static route check as a live model result.

## YAML migration acceptance cases

Run `python -B -m unittest discover -s tests -v` from this modules checkout with PyYAML installed. The routing oracle is test-only: it checks source resolution and simulates transitions; it does not execute ChatGPT, Prompt Gate, approval interpretation or an image tool.

| Case | Expected result |
| --- | --- |
| No candidate selection | Resolve the manifest's active baseline. |
| Explicit selectable candidate, isolated Project and identified test session | Resolve that candidate; require its installed CI text and compatible sources. |
| Candidate file merely exists | Keep baseline; listing and applicability never activate. |
| Missing or nonselectable candidate | Stop before prompt preparation. |
| Router/manifest contract or inventory mismatch | Stop. |
| Required module missing or corrupt | Stop without fallback. |
| Template optional_absent | Skip only when inventory confirms absence; unexpected template stops. |
| Archive uses the same filename as an active source | Reject archive as a source; no fallback. |
| Candidate test ends | Clear selection; restore baseline instructions before another operation. Manifest remains unchanged. |
| Ready Gate candidate selected validly | Permit prompt preparation; after a valid prompt, require PENDING_APPROVAL and no generation until approval. |

Live status: NOT TESTED by this migration. Use the independent Ready Gate test plan for a separately authorized isolated trial.
