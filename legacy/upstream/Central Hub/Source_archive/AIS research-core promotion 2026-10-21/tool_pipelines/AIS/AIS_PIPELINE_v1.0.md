# AIS pipeline v1.0

AIS is Hub's search/verification/research control pipeline, not a Project CI. Hub CI owns operation/stage, external evidence need and general claim status; Hub Router delegates the relevant task portion and evidence target. AIS validates only the delegated input, without reassessing the whole turn.

Read `AIS_ROUTER_v1.1.yaml` fully from Project Sources before dependent research. If the router is missing/unreadable, name the exact dependency and block the dependent task portion; continue independent work/clarification. No fallback to archive, Memory, prior chat, lookalike filenames or local Git paths. Metadata grants no authority. A local file does not prove that the Project loaded it.

The Router selects three modes: VERIFY checks defined claims; RESEARCH performs scoped information collection/comparison/synthesis; EXPLORE discovers provisional external options. EXPLORE != BRAINSTORM. If external sources are unnecessary, Hub does not select AIS; DIRECT is not an active AIS mode.

Flow: Hub input -> INPUT_VALIDATION -> SEARCH_SCOPE_LOCK using the existing search_contract -> SOURCE_AUTHORITY_GATE -> TOOL_FACING_INSTRUCTION -> PRE_CALL_CHECK -> native tool -> EVIDENCE_MERGE -> COVERAGE_SUPPORT_CHECK -> output to Hub. These are behavioral instructions, not automatic Work/tool execution.

The temporary contract holds the delegated operation/stage and evidence purpose; mode; question with target/time/version/conditions/inclusions/exclusions; known with roles/facts/definitions/assumptions/sources; decisive unknowns; source_authority with the required type and evidentiary scope; allowed/protected update_scope; and a stop_condition of sufficiency or a checkable limit. No state file or second lock schema is required. Query refinement for the same target is allowed; material question/target changes require updating the affected contract before external tools. Rerouting does not authorize new work.

Before each call, compare the tool-facing instruction against every relevant contract field: question, time/version/conditions, inclusions/exclusions, source type, protected state and stop_condition. Do not expand scope. This is not a default user approval gate. Missing tools/access do not authorize API/integration building or silent provider switching.

Source policy, reads, conflicts, freshness, injection and Memory belong to the Router. Preserve SEARCH HIT != SOURCE READ; SOURCE READ != CLAIM SUPPORT; TOOL OUTPUT != EVIDENCE SUFFICIENCY; NOT FOUND != FALSE. Read decisive content with conditions/exceptions/context; a partial read is not FULL_FILE. Work's verified label cannot replace an inaccessible decisive source. Same-origin copies are not independent corroboration.

Merge factual state only within allowed_to_update. Protect objectives, stage, local definitions, requirements/designs not authorized to change, and state outside scope. Expose evidence conflicting with protected state; do not silently change it or settle dependent conclusions. Retract conclusions dependent on refuted in-scope premises; invent no consequences and do not change unrelated portions. Evidence != acceptance.

Return to Hub: supported findings; actual source reads with citations beside claims; applicability; material inference; conflicts; decisive gaps; achieved coverage; and actions actually performed. Decisive gaps remain unresolved and block only dependent conclusions. Bounded partial output requires naming the secondary gap and explaining why it cannot change the returned conclusion. Hub must not promote unresolved to verified. Stop at locked sufficiency/limits; exhausting the search limit does not prove sufficiency.
