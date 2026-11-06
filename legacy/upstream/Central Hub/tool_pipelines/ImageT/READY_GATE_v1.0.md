# ImageT Ready Gate v1.0

READY_GATE_VERSION: 1.0
STATUS: ACTIVE
ROLE: EXECUTION_SNAPSHOT_AUTHORIZATION
COMPATIBILITY_SOURCE: manifest.yaml
ORIGINAL_PROTOCOL_SHA256: c1360811a98e27b6ddabbf008d9b82ffd54610b0bf5a8948c8f37092340fd322

## Ownership and entry

This required ImageT runtime control authorizes one exact execution snapshot after the controller's Prompt Gate passes. It owns snapshot construction/identity, PENDING_APPROVAL, APPROVED, REVISION_REQUIRED, STALE, approval interpretation/consumption, one-call authorization, approval-relevant freshness and uncertain submission. It owns no image operation selection, source resolution, field authority, operation-lock construction, prompt composition, visible-result verification, Hub stage or truth state. It is not an approval gate for AIS or other tools. On revision, the preserved protocol's apply-delta/rebuild instructions are performed by the controller; Ready Gate does not compose or rewrite the prompt.

The ImageT router resolves this exact active required artifact from manifest.yaml, including version/hash/compatibility. Missing/unreadable/corrupt/wrong-version/incompatible control stops only dependent generation: name the exact dependency, make no image tool call and continue independent work. No archive or embedded-controller fallback. ANALYZE alone generates nothing and bypasses Ready Gate; CREATE, EDIT, VARIATION, CORRECT and each generation retry require it.

## Versioned execution snapshot

After Prompt Gate, freeze the composed prompt; Ready Gate must not rewrite, improve or silently patch it. Construct READY SNAPSHOT vN, STATE: PENDING_APPROVAL. The numbered prompt version in the preserved protocol below identifies this same snapshot, not a separate approval object. Retain in temporary context: state; exact final tool-facing prompt; exact reference assets and reference roles; exact tool options; relevant execution inputs/attachments; operation-lock identity and protected constraints; authorized interpretations/completions and preference additions; intentionally open fields; explicit exclusions/negatives; and effective source versions/hash verification status as the freshness basis. This is prose instruction, not a persistent schema or state engine.

Before PENDING_APPROVAL, the controller must already have resolved every generator reference to an exact available asset plus its exact role. Research evidence may supply scoped textual facts but is not an image asset: AIS EVIDENCE SOURCE != IMAGE GENERATOR REFERENCE ASSET. Do not promise to choose references after approval. With no image reference asset, explicitly display REFERENCES: NONE; if a required asset/role is unresolved, return to the controller without a call.

Display the snapshot version and PENDING_APPROVAL, retained constraints, authorized interpretations/completions, authorized preference additions (none when absent), intentionally open fields, excluded/forbidden fields, exact final prompt, exact references plus roles or NONE, exact relevant tool options and relevant execution inputs. Open fields remain open: UNSPECIFIED != FORBIDDEN; OMITTED != PROHIBITED; OPEN FIELD != NEGATIVE CONSTRAINT. The controller's Prompt Gate owns negative-authority checks; Ready Gate does not add prohibitions. Show decisions, not private reasoning, and end with the preserved protocol's official approval question for this version.

## Preserved approval protocol

After the prompt gate passes, before each CREATE, EDIT, VARIATION, CORRECT or retry call, set PENDING_APPROVAL for a numbered prompt version. ANALYZE alone never enters this gate or generates. No approval means no image generation.

Show retained constraints, meaningful interpretations/completions, authorized preference additions (none here), unfilled/excluded fields, exact prompt, references and tool options. End with: "Thế này đã đủ ổn theo yêu cầu của bạn chưa?" Wait. Show decisions, not private reasoning.

Keep prompt, lock, references/options and source versions in temporary context. Clear YES/CÓ/ĐỒNG Ý to this version sets APPROVED for one call. Recheck sources and this snapshot before submission. If unchanged, send the exact displayed prompt and approved inputs; no rewrite, embellishment or second confirmation. Submission consumes approval; it covers no other call or future request.

NO/KHÔNG keeps PENDING_APPROVAL, unapproved; ask what to adjust if unspecified. Any revision, including "yes, but...", sets REVISION_REQUIRED and invalidates approval. Preserve compatible constraints, apply the delta, rerun route and prompt gate, then show a new version. Ambiguous replies never approve; clarify, retaining the unchanged pending version.

Changed effective sources, request, references/options or lost/uncertain pending context sets STALE. Stop, reroute, recheck the prompt gate and show a new version for approval. A question alone preserves an unchanged pending version. Report uncertain submission; never silently retry. This guidance provides no durable state or proof of backend payload.

## Exact submission and invalidation

PROMPT SHOWN TO USER = PROMPT AUTHORIZED BY USER = PROMPT SENT TO IMAGE GENERATOR. APPROVED SNAPSHOT = EXACT PROMPT + EXACT REFERENCES + EXACT REFERENCE ROLES + EXACT TOOL OPTIONS + EXACT RELEVANT INPUTS + EXACT OPERATION CONSTRAINT STATE, within observable evidence. ONE APPROVAL = ONE EXACT TOOL CALL. Immediately before submit, recheck this full snapshot and its effective source freshness basis; submit unchanged approved prompt/assets/roles/options/inputs once, with no post-approval rewrite or second confirmation. Submission consumes approval (CONSUMED); it never authorizes a retry, future request, second image/variation/call or changed input/source basis.

Any change that can affect the generator call invalidates approval: effective sources, current request, tool-facing prompt, operation lock/protected constraints, references, reference roles, tool options, attachments or relevant execution inputs. Set STALE, make no call, send affected dependencies back through router/controller resolution and Prompt Gate, then display a new snapshot version requiring new approval. A user revision, including YES BUT/CÓ NHƯNG, is REVISION_REQUIRED and also invalidates approval; preserve unaffected constraints while the controller rebuilds. No silent patch to an approved snapshot.

Clear YES/CÓ/ĐỒNG Ý applies only to the exact current version. NO/KHÔNG remains unapproved; ask what to change if unspecified. Emoji, quoted yes, tentative language, unrelated agreement or ambiguous replies never approve. Approval of an older version makes no call; clarify the current version. A question alone preserves an identifiable unchanged pending snapshot; lost/uncertain pending context is STALE.

Report uncertain submission and never silently retry; any retry requires a new snapshot and approval. An unobservable backend payload is UNVERIFIABLE, not proof of equality or PASS. Displayed prompt != proof of backend payload; report only observed correspondence. The controller owns visible-result verification after actual execution. Original ImageT behavior was previously live-tested per user-confirmed project state; Central Hub versioned integration has not yet been live-tested.
