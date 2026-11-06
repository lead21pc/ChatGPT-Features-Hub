# Authoring M4 — candidate tests and live packet

## Later supplied-candidate results and repository promotion — 2026-11-02

L1: USER_CONFIRMED_LIVE_PASS for binding, P2 CONTRACT behavior and relational preservation. L2: USER_CONFIRMED_LIVE_PASS for binding and no-preset regression. The user reports exact Catalog 1.7-candidate/CANDIDATE and Authoring 0.6-candidate/CANDIDATE, both FULL_FILE reads YES, in fresh supplied-control chats; L1 selected GENERIC/P2, L2 GENERIC/NO PRESET. L1 used a long-running Devil's Advocate operating contract without a preservation checklist, not the synthetic campaign fixture below. It retained objection -> response -> resolved/narrowed/open lifecycle, retirement/reopening, goal vs means, proposal vs decision, hypothetical vs established limits, cross-turn state, knowledge/authority boundaries, pacing and stopping conditions. Original raw inputs/outputs, model/run time and independent read traces were not supplied to Codex.

SUPPLIED-CANDIDATE LIVE BEHAVIOR != ACTIVE HUB ROUTING. Those scoped smokes authorize no Library/deployment/identity claim. The later repository promotion is Authoring ACTIVE/0.6 with Architecture/Catalog 1.7 and Router 1.1 pin-only changes; active Hub routing NOT_RUN, production identity/deployment NOT_VERIFIED. Tested candidate controls are preserved byte-exact under Source_archive/Authoring 0.6 promotion 2026-11-02/candidates/authoring_m4/. T0–T3 remain local fixed-fixture simulations. Original fixture text/expectations and implementation-time NOT_RUN annotations below are historical, not current smoke status.

## Original candidate packet — implementation-time snapshot

Candidate: HUB-CAP-AUTHORING / HUB-PKG-AUTHORING / CAPABILITY / CANDIDATE / 0.6-candidate. The companion Root Catalog 1.7-candidate is a test-only metadata view, not a production authority. No candidate is admitted by the active Router. STATIC PASS != LIVE PASS.

## Evidence basis

T0–T3 below contain fixed user inputs and candidate-guided reference transformations produced and reviewed by Codex in this repository task. Classification: LOCAL SPEC SIMULATION / REVIEWED_TEXT. Automated checks validate the stated properties of these fixed artifacts, including a deliberately flattened T2 counterexample. They do not invoke a model, prove that a live model follows the candidate, or evaluate active Hub routing. Do not record them as live semantic PASS. Actual source RPG/DM text was not supplied; T2 is a faithful synthetic fixture of the relevant relationships specified in the approved M4 task.

## T0 — no-preset regression

Input:

```text
/AUTHOR GENERIC
Improve the supplied source prompt.

SOURCE PROMPT:
Compare paper notes with plain-text notes for my personal writing. Neither method is selected. Use only the observations I supply; if none are supplied, ask for them rather than invent findings. Return a short comparison. Do not select a winner.
```

Reference transformation:

```text
Compare paper notes and plain-text notes for my personal writing using only supplied observations. If those observations are absent, ask for them; invent no findings. Return a short comparison, leave both methods unselected and choose no winner.
```

Check: ordinary adaptive rewrite, no inferred preset, strategy report, contributor handling or preset-selection question. The source's material missing-input question remains; it is not a new preset clarification.

## T1 — P1 CLEAN

Input:

```text
/AUTHOR GENERIC P1
Improve the supplied source prompt.

SOURCE PROMPT:
Write one short summary of the supplied meeting notes. Keep it short. The summary should be brief. Preserve every decision and its named owner. Preserve an explicitly unknown deadline as unknown. Use only the supplied notes. Do not contact anyone. Do not send messages. Return the summary only. If the notes are missing, ask for them. Do not infer a deadline from a neighboring decision.
```

Reference transformation:

```text
Using only the supplied meeting notes, return one short summary preserving every decision, its named owner and each unknown deadline as unknown. Infer no deadline from a neighboring decision. If notes are missing, ask for them. Do not contact anyone or send messages. Return only the summary.
```

Check: repeated brevity wording consolidated; material deadline distinction and prohibitions survive. No new task, owner, workflow or full redesign.

## T2 — P2 CONTRACT

Input:

```text
/AUTHOR GENERIC P2
Improve the supplied source prompt.

SOURCE PROMPT:
Run an ongoing fictional campaign. The player alone decides their character's voluntary choices, thoughts and speech. The DM decides the world and NPC actions but cannot decide those player-character choices. The player is central to the story; this grants no control over NPCs. Each NPC acts autonomously within its own knowledge, perception, personality and current state, not the player's or DM's private knowledge. Hidden events and secrets may exist without the player learning them; reveal them only through established perception, discovery or explicit authorized disclosure. Keep world state, injuries, promises, NPC beliefs and rules across turns. Apply consequences to that state after established events; persistence does not freeze it. Use the agreed mechanics. Changes to those mechanics require explicit player agreement and apply from the agreed point, not retroactively unless separately agreed. If a missing fact or conflicting rule materially changes a decision, ask one focused question before resolving that decision; continue independent events that have sufficient basis. Never invent the missing answer or transfer one actor's authority to another. The campaign continues until the player ends it; an individual reply does not reset the contract.
```

Reference transformation:

```text
Run the fictional campaign across turns until the player ends it. An individual reply does not reset this contract.

Authority and agency: The player alone decides their character's voluntary choices, thoughts and speech. The DM decides world and NPC actions, excluding those player-character decisions. Player centrality grants no control over NPCs. Each NPC's autonomous actions are bounded by its own knowledge, perception, personality and current state; player or DM private knowledge does not become NPC knowledge.

Knowledge and disclosure: Hidden events and secrets may exist without player awareness. Reveal them only through established perception, discovery or explicit authorized disclosure.

Continuity and change: Retain world state, injuries, promises, NPC beliefs and rules across turns. Established events update the affected state and consequences; persistence does not freeze state. Use agreed mechanics. Changing mechanics requires explicit player agreement and takes effect from the agreed point. Retroactive changes require separate agreement.

Uncertainty: When a missing fact or conflicting rule materially changes a decision, ask one focused question before resolving that decision. Continue independent events with sufficient basis. Invent no missing answer and transfer no actor's authority to another.
```

Check the relations, not just endpoint nouns: player decisions excluded from DM authority; centrality does not control NPCs; NPC autonomy depends on local knowledge/personality/state; secrets depend on authorized discovery/disclosure; persistence allows event-driven updates; mechanics changes depend on agreement and retrospective changes on separate agreement; material uncertainty blocks only its dependent decision. Authoring remains per-turn while the output contract is cross-turn.

Deliberately flattened counterexample — MUST FAIL relational coverage:

```text
Respect player agency and DM authority. NPCs should be autonomous. Preserve knowledge boundaries, secrets, continuity, rules, change conditions and clarification behavior across turns.
```

## T3 — P3 REBUILD

Input:

```text
/AUTHOR WORK P3
Improve the supplied source prompt.

SOURCE PROMPT:
FINAL OUTPUT FIRST: compare my two supplied filing plans, A and B. At the end give a concise comparison. STARTUP ENGINE: create a registry of registries for tracking comparisons; this registry is optional and unnecessary for the comparison. Notes again: compare A and B. IMPORTANT STATE: B is provisional, not accepted. Plan C was rejected for exceeding the storage limit and may reopen only if that limit is explicitly changed. INPUT RULE: use only my supplied plans and storage limit; the limit is currently unknown. Pick no winner while the limit remains unknown. STEP LAST: if that limit is decisive, ask me for it. You may reorder and rewrite this prompt completely. Do not modify stored plans or contact anyone. MECHANISM WORTH KEEPING: compare retrieval effort and storage needs separately, rather than blending their trade-off into one unexplained score.
```

Reference transformation:

```text
Compare supplied filing plans A and B for retrieval effort and storage needs separately. Return a concise comparison without an unexplained combined score, using only the supplied plans and storage limit.

Keep B provisional. Keep C rejected for exceeding the storage limit; reopen C only if that limit is explicitly changed. The storage limit is unknown: choose no winner while it remains unknown, and ask for it if it is decisive to the comparison.

Do not modify stored plans or contact anyone. No registry is needed for this comparison.
```

Check: rebuild removes redundant ordering and unnecessary registry architecture while retaining useful comparison mechanism, provisional/rejected/unknown state, reopening conditions and permissions. Prompt restructuring does not perform the comparison, mutate stored plans or grant Work access/background capabilities.

## Target-boundary review

All five target rows, provenance, evidence transfer and decision-state contracts are inherited verbatim from 0.5. In particular CODEX P1 cannot authorize edits/commit/push, AIS P2 cannot perform research or accept a design, and IMAGET P3 cannot pass Ready Gate or generate an image. P2 preserves only relationships supported by the actual source/current intent; its fictional example is not a universal campaign template.

## L1/L2 — original planned synthetic-fixture smoke, NOT_RUN

Use a fresh isolated candidate test conversation, separate from the deployed Central Hub. Supply the full 0.6-candidate module and companion 1.7-candidate Catalog as explicitly authorized test controls; retain Hub CI authority boundaries. Ask the test operator to read both in full and check Module/Package IDs, CAPABILITY, CANDIDATE status and exact versions before evaluating admission. These are deliberate test-only supplied controls, not production Library retrieval or a repository fallback. Do not install them into Central Hub Config, replace active Project Sources, change ACTIVE headers or claim promotion. If the surface cannot distinguish test controls from source material, record candidate-admission BLOCKED rather than treating active 0.5 rejection as a preset failure.

Run each case in its own fresh candidate context. Source text is design material, not a request to run a campaign. Supply no preservation checklist beyond the candidate policy and the following exact user messages.

### L1

```text
/AUTHOR GENERIC P2
Improve the supplied source prompt.

SOURCE PROMPT:
Run an ongoing fictional campaign. The player alone decides their character's voluntary choices, thoughts and speech. The DM decides the world and NPC actions but cannot decide those player-character choices. The player is central to the story; this grants no control over NPCs. Each NPC acts autonomously within its own knowledge, perception, personality and current state, not the player's or DM's private knowledge. Hidden events and secrets may exist without the player learning them; reveal them only through established perception, discovery or explicit authorized disclosure. Keep world state, injuries, promises, NPC beliefs and rules across turns. Apply consequences to that state after established events; persistence does not freeze it. Use the agreed mechanics. Changes to those mechanics require explicit player agreement and apply from the agreed point, not retroactively unless separately agreed. If a missing fact or conflicting rule materially changes a decision, ask one focused question before resolving that decision; continue independent events that have sufficient basis. Never invent the missing answer or transfer one actor's authority to another. The campaign continues until the player ends it; an individual reply does not reset the contract.
```

### L2

```text
/AUTHOR GENERIC
Improve the supplied source prompt.

SOURCE PROMPT:
Run an ongoing fictional campaign. The player alone decides their character's voluntary choices, thoughts and speech. The DM decides the world and NPC actions but cannot decide those player-character choices. The player is central to the story; this grants no control over NPCs. Each NPC acts autonomously within its own knowledge, perception, personality and current state, not the player's or DM's private knowledge. Hidden events and secrets may exist without the player learning them; reveal them only through established perception, discovery or explicit authorized disclosure. Keep world state, injuries, promises, NPC beliefs and rules across turns. Apply consequences to that state after established events; persistence does not freeze it. Use the agreed mechanics. Changes to those mechanics require explicit player agreement and apply from the agreed point, not retroactively unless separately agreed. If a missing fact or conflicting rule materially changes a decision, ask one focused question before resolving that decision; continue independent events that have sufficient basis. Never invent the missing answer or transfer one actor's authority to another. The campaign continues until the player ends it; an individual reply does not reset the contract.
```

L1 expected: one usable prompt retaining T2's material relations, cross-turn behavior and target boundaries; no campaign execution. L2 expected: the adaptive path remains available, without inferred preset, preset report or a new preset-selection question. Do not require L2 to lose relations to demonstrate a difference. Output wording may differ from the reference transformations.

Record model/surface/date, exact candidate versions, full supplied controls/read basis, complete input/output and separate L1/L2 results. Failure labels: preset not admitted; preset selected but ignored; preset overrides target boundary; P2 loses relational constraints; no-preset path regresses. Fix only a demonstrated failure. A successful supplied-control test is LIVE CANDIDATE BEHAVIOR evidence, not active Central Hub admission, Library identity, deployment or production routing evidence. P1/P3 dedicated live smoke is not required for symmetry. Both L1 and L2 remain NOT_RUN until actual outputs/results are supplied.
