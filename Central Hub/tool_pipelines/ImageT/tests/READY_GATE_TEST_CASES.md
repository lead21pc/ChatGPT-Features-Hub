# Active Ready Gate — required normative regression specification

STATUS: REQUIRED_REGRESSION_SPEC
ROLE: NON_RUNTIME_NORMATIVE_ORACLE
TARGET: READY_GATE 1.0
APPLIES_TO: READY_GATE_v1.0.md; IMAGE_CONTROLLER_v1.1 generation operations
READY_GATE_RUNTIME_STATUS: ACTIVE
ORIGINAL_IMAGET_LIVE_VALIDATION: CONFIRMED_BY_USER
CENTRAL_HUB_LIVE_VALIDATION: NOT_RUN

This is the required normative migration/regression oracle for READY_GATE_v1.0.md, delegated by the active subordinate ImageT controller. It is not a runtime Source, an optional test feature or a replacement for Hub instructions. It requires no candidate selection or replacement of Project instructions.

The user has confirmed that Ready Gate behavior was previously live-tested in the original ImageT Project. That user-confirmed project state is distinct from static migration preservation and from Central Hub integration, which has not yet been live-tested. The historical plan's NOT RUN metadata records its earlier evidence state; it does not override the user's later confirmation. Current sources do not provide the original live call trace or submitted payload, so this specification claims neither access to those records nor case-by-case live results.

## Purpose and runtime boundary

Ready Gate exists to expose the final tool-facing prompt and relevant execution inputs before the image generator call. The required order is source/authority resolution -> operation lock -> tool-facing prompt composition -> Prompt Gate -> Ready Gate -> image generator call -> visible-result verification.

- Prompt Gate verifies construction correctness against the resolved operation lock.
- Ready Gate presents the final prompt version, references, options and relevant execution inputs for user authorization.
- The image tool receives only that approved unchanged version, once.

The intended invariant is PROMPT SHOWN TO USER = PROMPT AUTHORIZED BY USER = PROMPT SENT TO IMAGE GENERATOR, to the extent observable/verifiable. ONE APPROVAL = ONE EXACT TOOL CALL. Displayed text alone does not establish backend equality. ANALYZE alone performs inspection without image generation or Ready Gate.

## Preparation and fixtures

Use the same simple CREATE request for all basic approval cases:

> Create one flat blue square on a white background, no text, no other objects.

For EDIT/CORRECT, use the same supplied image with two objects and change only the left object's color. VARIATION changes only that color. ANALYZE describes the image only, with no generation. Record exact references and tool options before approval.

Use the active Hub CI -> Hub Router -> subordinate ImageT controller architecture with the matching runtime sources. Do not install this oracle, archives or inactive preferences as runtime controls. Preference is not a prerequisite. Missing/inconsistent required sources block the dependent image operation normally. The test design itself grants no image-generation approval; a live acceptance run may generate only after the human tester clearly approves the relevant version.

## R01-R22 behavioral requirements

Every row is a normative acceptance requirement. The rows are not a claim that Central Hub has executed or passed these cases live.

| ID | Event or input | Required outcome |
| --- | --- | --- |
| R01 | Request reaches prompt gate with a required material field unresolved | Stop for the decision; no Ready Gate pass and no tool call. |
| R02 | Valid request, no reply after Ready Gate | Numbered PENDING_APPROVAL; all five user-visible categories and exact question; zero calls. |
| R03 | YES/CÓ/ĐỒNG Ý clearly approves the current version | APPROVED; freshness check; one call with unchanged displayed prompt and approved inputs; no second confirmation. |
| R04 | NO/KHÔNG without changes | PENDING_APPROVAL, still unapproved; ask what to change; zero calls. |
| R05 | "Có, nhưng đổi màu sang xanh lá." | REVISION_REQUIRED; never submit old version; preserve other constraints; new route/gate/version. |
| R06 | "Không, thực ra tôi muốn hai hình vuông." | New version changes only the authorized count; zero calls until new approval. |
| R07 | After R05, approve the new version | Submit exactly the new version once; old approval has no effect. |
| R08 | "Có lẽ", emoji, quoted YES or uncertain approval target | Clarify; no approval inferred; zero calls. |
| R09 | Request or tool-facing prompt/options/references changes after approval, before submit | STALE or REVISION_REQUIRED; reroute/gate/new version; old approval invalid. |
| R10 | New unrelated image request follows approval | Previous approval never authorizes it; new Ready Gate required. |
| R11 | Context no longer identifies exact pending prompt | STALE; reconstruct through route and prompt gate; new confirmation. |
| R12 | Effective source version changes or a required source cannot be read | No call; route/resolve again, new Ready Gate only after source requirements pass. |
| R13 | ANALYZE only | Analysis only; no Ready Gate or image generation. |
| R14 | EDIT/VARIATION/CORRECT | Gate before each call; preserve outside delta and non-open fields. Ready display cannot broaden operation. |
| R15 | Retry with changed prompt | Route/gate/new version; require new approval. |
| R16 | Submission already occurred; retry uses same prompt | Approval was consumed; require new version/approval for another call. |
| R17 | User asks what one sentence means without revising | Answer without tool call; same unchanged pending version remains identifiable. |
| R18 | User explicitly approves an older version while a newer one is pending | No call; clarify current version. |
| R19 | Submission result uncertain | Report uncertainty; no silent retry; any retry needs a new approval. |
| R20 | Gate-passed prompt is shown or approved | Compare composed, displayed and submitted prompt when observable; no Ready-stage rewrite or post-approval polish. |
| R21 | Preference absent throughout | Ready Gate still works; preference additions category says none; M2 is not a prerequisite. |
| R22 | Prompt says "not five fingers", exact count not set | No inference of four; baseline negative handling survives. |


## Required test topology

FRESH_CONVERSATIONS: R03-R08
MULTI_TURN_CASES: R09-R19

Repeat R03-R08 in separate fresh conversations. Run R09-R19 as multi-turn cases so approval, revisions, freshness, context loss and consumed approval are tested across turns. These case-specific groupings are required, not interchangeable with a generic fresh-chat/retry instruction.

## Evidence to record

For each run, record date/model/surface, exact active controller and module hashes/headers, original request, attachments and assigned reference roles, exact references, tool options and relevant execution inputs, operation lock snapshot, prompt-gate draft when observable, displayed prompt version, approval reply, state transition, tool-call count and submitted payload when observable. Preserve the correspondence among composed, displayed, approved and submitted versions; do not request private reasoning. Redact private data in shared records.

Keep user-confirmed prior live validation, static preservation checks, test-only specification simulations and observed Central Hub live results separate. Source comparisons and local oracles prove no model execution. Do not infer image quality improvements from this suite.

## Required acceptance invariants

- All no-approval branches require zero image tool calls.
- Every approved submission must use the exact approved prompt version and exact approved references, options and relevant execution inputs, with exactly one tool call, without a second confirmation. Submission consumes approval; it authorizes neither another call nor an unrelated request.
- Revisions invalidate previous approval and preserve unaffected constraints. This includes a yes-but reply; reroute, apply the authorized delta, recheck the prompt gate and show a new version requiring new approval.
- Changed request, prompt, sources, references, options, operation lock or relevant execution inputs invalidate approval; reroute/rebuild, show a new version and require new approval before submission. Lost or uncertain pending context is STALE; an unchanged clarification question does not authorize a call or invalidate the identifiable unchanged pending version.
- Report uncertain submission; never silently retry. Any retry requires a new version/approval, including a retry of the same prompt after a submission.
- Unobservable backend payload must be marked UNVERIFIABLE. A displayed prompt is not proof of backend payload. Claim equality only for the correspondence actually observed; lack of visibility is not PASS.

## X01 — cross-pipeline snapshot and scope regression

SPEC STATUS: REVIEWED_TEXT; CENTRAL HUB LIVE: NOT_RUN. This bounded fixture represents the user-reported stress-test breaks; it supplies no real-world historical claim or original live trace.

Required sequence: AIS -> BRAINSTORM -> TECHNICAL -> CREATIVE -> IMAGET -> READY GATE.

Input fixture: source S1 supports component A (archery); source S2 supports context B (mounted travel); neither supports their combination. The user requests a provisional fictional mechanism using these scoped facts, technical examination of that mechanism, an authorized creative design and then an image. A horse field is unspecified. S1/S2 are research sources, not generator image assets. No generation has been approved.

1. AIS returns the supported components separately, with scope and the relation gap. SUPPORTED COMPONENTS DO NOT AUTOMATICALLY SUPPORT THEIR COMBINATION; mounted-archery is not verified by these fixtures.
2. BRAINSTORM develops the requested provisional fictional branches. TECHNICAL examines their mechanism and distinguishes hypotheses from evidence. CREATIVE develops only the authorized design; the fictional mechanism stays fictional. No output silently becomes accepted design or historical fact.
3. IMAGET receives only task-assigned design attributes. AIS EVIDENCE SOURCE != IMAGE GENERATOR REFERENCE ASSET: S1/S2 may contribute scoped textual constraints but cannot be sent as image references. If no image assets are supplied, REFERENCES: NONE. In a paired variant with a user-supplied exact image asset F for palette only, resolve F before approval and fix its role to palette only; do not import identity, costume or pose.
4. At Prompt Gate, UNSPECIFIED != FORBIDDEN. The open horse field stays open/omitted; do not invent "no horse". Every actual negative requires user/source/logical authority. Freeze the resolved prompt and inputs before Ready Gate.
5. Ready Gate displays READY SNAPSHOT v1, STATE: PENDING_APPROVAL, the exact prompt, exact references plus roles or NONE, options, relevant inputs, constraints/completions and intentionally open fields. All references are resolved before approval; no later reference selection is promised. Zero image tool calls occur before approval.
6. A clear approval permits exactly one unchanged snapshot submission. Any change to asset, role, prompt, options, source basis, operation lock or relevant input invalidates approval and requires a new numbered snapshot. Unobservable payload is UNVERIFIABLE.

Acceptance: all six scoped handoffs and all boundaries above must hold. Record source support/relation gap, fictional claim status, design authorization, negative provenance, resolved assets/roles, numbered snapshot/state, reply, calls and payload when observable. Do not call this fixture run a model test merely because its contracts or local oracle pass.
