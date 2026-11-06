# Shopping Search — v1.0 candidate

Module ID: HUB-PROC-SHOPPING-SEARCH
Package ID: HUB-PKG-SHOPPING
Runtime role: DOMAIN_PROCEDURE
Scope: prepare commerce-specific research needs and interpret AIS returns for the delegated Shopping research portion
Status: CANDIDATE
Version: 1.0-candidate
Responsibility boundary: Shopping research preparation/interpretation only; Hub owns evidence need, pipeline selection and authorization; AIS owns research execution procedure, source policy, support, freshness, merge, depth, coverage and execution observability

## Admission and independent composition

Repository-only inactive candidate; intended future LIBRARY_MODULE binding within Central Hub Config, not an installed object or runtime locator. Use only in an explicitly authorized isolated candidate test after the Shopping core/local Catalog selects this procedure for its matched portion and its full content/identity is available. Candidate status does not permit normal active admission. Missing/mismatched/unreadable procedure blocks Search-dependent work, not independently sufficient core interpretation; no hidden predecessor fallback.

INDEPENDENT HUB COMPOSITION: Hub separately determines Shopping applicability and external evidence need; Hub Router independently selects AIS for the relevant portion. This procedure has no hard Requires AIS edge, calls no search/read tool, selects no pipeline or AIS mode and performs no research through an alternate mechanism. It can prepare a brief before AIS runs or consume a return afterward. If AIS is absent, unselected, not executed or incomplete, preserve the evidence need/incomplete research state and return it to Hub. A selection or dependency never proves execution or support.

HUB SELECTS PIPELINE. SHOPPING EVIDENCE NEED != AIS ACTIVATION.
PIPELINE SELECTION != TOOL EXECUTION.

## RESEARCH preparation — commerce-specific brief

Use the core's scoped objective/operation, target identity and SKU/revision needs, market/location/time, HARD/SOFT conditions, priority_order, relevant Category fields, Offer conditions and knowns/conflicts/gaps. Preserve protected state and constraint roles. Ask only material clarification through Hub; do not reconstruct absent sources or turn every suggested field into a requirement.

Form the smallest useful brief: what product/Offer question needs evidence, which identity/condition relations matter, what channel scope is relevant, what already-supported observations can be reused, and what unresolved fields limit the purchase conclusion. Include the bounded shopping completion question and any user/Hub-assigned limits. AIS constructs its existing search_contract, source policy, research_strategy and stop condition; this brief is not a second research lock/schema or a source-authority decision. Material importance is input to planning, not a fixed search order imposed by shopping priorities.

### Temporary strategies

| Strategy | Input emphasis | Intended Shopping output |
| --- | --- | --- |
| EXACT | incomplete target identity, SKU/revision or conflicting attributes | supported exact identity links or explicit unresolved alternatives; no lookalike revision as primary identity evidence |
| VALUE | specified purchase conditions, priorities and bounded market | broader relevant Offers/channels, conditional vs unconditional price and availability context for comparison |
| DISCOVER | needs/constraints rather than a fixed accepted product | alternative ProductCandidates with their supported attributes and unresolved requirements; discovery is not acceptance |

Infer a strategy only from an unambiguous delegated objective or explicit selection; otherwise describe the material need or clarify. No mandatory command syntax, enum field or default-strategy report is required. Strategies may serve successive parts of a task but supply no new goal, HARD condition, authority or persistent mode. Reassess them with the current task. Do not create BALANCED; multi-criterion balance belongs to DECIDE. AIS owns evidence depth; EXACT/VALUE/DISCOVER do not map to NORMAL/THOROUGH/EXTENSIVE.

SEARCH STRATEGY != AUTHORITY. SEARCH STRATEGY != HARD FILTER.
SEARCH STRATEGY != PERSISTENT MODE. SEARCH STRATEGY != AIS RESEARCH DEPTH.

### Store/channel breadth

For a broad purchase hunt, propose materially relevant coverage branches: major retailers, specialist retailers, smaller independent storefronts, marketplace storefronts and manufacturer/distributor/reseller channels when relevant. Category/objective determine which branches matter; these are coverage dimensions, not fixed tiers, named store rankings, a registry or a quota. Narrow exact verification need not survey all branches. A broad price-hunt brief must not collapse to familiar/high-ranked sellers or stop merely because one cheap Offer appeared.

Prefer web storefronts, retailer product pages, marketplaces and relevant manufacturer/distributor/reseller pages for commerce discovery. This is not Maps-first discovery and not a global tool ban: physical-store distance, directions or local availability may justify geographic/local-business evidence through Hub/AIS. Tool choice and actual access stay with their existing owners.

TOP SEARCH RESULTS != MARKET COVERAGE. CHEAP OFFER FOUND EARLY != PRICE HUNT COMPLETE.

## Interpret the research return

Consume the existing semantic AIS return through Hub: supported findings, actual source reads/citations, applicability, material inference, conflicts, decisive gaps, achieved coverage against locked needs, quality target, actual execution status/basis, observed executor, actions actually performed and material limits. Carry what affects the shopping conclusion. Receipt is not an independent source read; preserve supplied source/read limits and USER_REPORTED attribution. Do not invent a read, repair an inaccessible source or re-grade sources with a Shopping evidence system.

Keep ProductCandidate/SKU/Offer linkage tied to supported relations, not individually plausible attributes. Preserve seller/channel, identity applicability, actual observation time, units/currency, stock qualification and price conditions. Source read does not by itself establish a valid Offer. Conflicted or unknown mandatory attributes stay open for core DECIDE; cheaper price does not resolve them. Return supported domain inputs and specific gaps to core/Hub, never general accepted state.

Preserve each action/attempt's supplied EXECUTED, NOT_EXECUTED, UNKNOWN or CONFLICTED plus evidence basis and scope. AIS determines these statuses: direct execution evidence supports EXECUTED; direct non-execution/pre-submission block/unavailable executor supports NOT_EXECUTED; absent observability remains UNKNOWN; contradictory direct traces remain CONFLICTED. Do not classify absence of trace or model self-report as proof, erase earlier executed actions because a later tool failed, or count a search as a decisive source read.

PLANNED SEARCH != EXECUTED SEARCH. EXECUTED SEARCH != SOURCE READ.
SOURCE READ != CLAIM SUPPORT. SOURCE READ != VALID OFFER.
VALID OFFER != SHOPPING-SCOPE COMPLETION.

Apply AIS's achieved support/coverage to the purchase question without taking over AIS's coverage evaluation. Keep results inspected, unique Offers, unique sellers/channels and queries distinct when material; one metric cannot substitute for another. Report a winner only within its supported set/conditions. If major/specialist retailers are covered, smaller independents partial and marketplaces not executed, retain that partial scope; do not report the whole market searched or the market-wide lowest price. Limits exhausted or intended branch lists do not prove completeness. Execution UNKNOWN remains unknown even when an answer sounds complete.

Preserve independent supported branches on failure. Return remaining domain evidence needs to Hub within the existing scope/limits; do not force another research round, downgrade standards or silently switch mechanisms. No executor framework, persistent log/state, new AIS return schema, authoring/image adapter or commerce execution is part of this procedure.
