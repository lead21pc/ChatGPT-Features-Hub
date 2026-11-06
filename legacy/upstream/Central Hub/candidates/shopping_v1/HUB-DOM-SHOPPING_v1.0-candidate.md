# Shopping core — v1.0 candidate

Module ID: HUB-DOM-SHOPPING
Package ID: HUB-PKG-SHOPPING
Runtime role: DOMAIN_CONTROL
Scope: prepare and interpret the Hub-delegated shopping task, product identity, purchase constraints, Offers and supported comparison; select only this package's applicable procedure through its local Catalog
Status: CANDIDATE
Version: 1.0-candidate
Responsibility boundary: Shopping interpretation and local selection only; Hub CI retains operation/stage/state/truth/action authorization and external-evidence need; Hub Router retains package selection/composition and read validation; AIS retains research procedure, source policy, support, freshness, merge, coverage and execution observability

## Admission and package interface

Repository-only inactive candidate. Not registered in the active root Catalog, installed in Library or deployed to a Project. Use only in explicitly authorized isolated candidate tests. Intended future binding: LIBRARY_MODULE within Central Hub Config; repository filenames/paths are development references, never runtime locators. CANDIDATE PRESENCE != ACTIVATION. Normal runtime admission still requires accepted ACTIVE bindings and the current Router's exact identity, FULL_FILE and body checks; this candidate grants none of them.

After the simulated Hub handoff in a candidate test, read this core and the exact same-package HUB-CATALOG-SHOPPING, PACKAGE_CATALOG, CANDIDATE/1.0-candidate. Use that Catalog's applicability to select only relevant package-local leaves. The baseline closure is core + local Catalog even when no leaf is selected; retain sufficient verified in-context read evidence rather than inventing a new read on every turn. Missing/unreadable core or required Catalog blocks dependent package interpretation/selection. Do not substitute v0.1, guess a leaf, scan other packages or claim baseline work is equivalent to a missing control.

Sufficient supplied evidence for identification, fixed-Offer comparison, constraint reevaluation or Category interpretation selects no Search leaf and no AIS through Shopping. A research-oriented delegated portion needing commerce-specific external preparation/return interpretation may select the Search procedure declared by the local Catalog. This does not select AIS. Hub independently determines external evidence need and Hub Router independently selects AIS. Return selected leaf identity, matched scope, read evidence and blockers through the existing Hub interface. Verify a selected leaf's binding, FULL_FILE, identity/version/body before applying it. Missing Search blocks Search-dependent work only; continue independently sufficient core interpretation. Never load all package bodies by membership.

PREPARE and DECIDE below are functional steps, not independent modules, approval gates or a state engine. Search owns the Shopping-specific RESEARCH step when selected; it does not replace AIS. No hard Requires, Refines or Complements relation is needed. No Authoring or ImageT dependency is implied.

## PREPARE — current scoped shopping state

Receive the current task portion, objective/operation, target identity, protected/established Hub state, supplied evidence and material uncertainty. Keep only relevant ProductCandidate/SKU state, market/location/time, constraints with HARD/SOFT roles, priority_order, relevant Category fields, Offer conditions, knowns/conflicts/unknowns and specific shopping evidence needs. This is temporary prose/context, not a mandatory machine schema or visible report template.

Preserve compatible prior evidence and state; reassess applicability when entity, operation, market, time or scope changes. A model-specific fit finding must not become a dimension-wide constraint; another model sharing its length need not share its connector geometry. Do not invent changed product identity, a resolved unknown or a broader target set merely because the operation changed from identification to enumeration, prices or comparison. Current evidence need belongs to Hub; prior research neither proves new research unnecessary nor requires research to continue.

### Constraint role and Priority

HARD describes a purchase requirement: a supported violation makes an option unsuitable for that purchase. SOFT describes a preference or approximate recollection: a mismatch stays visible without automatically eliminating an otherwise supported candidate. Preserve the user's assigned role; clarify a material ambiguity rather than silently promoting or weakening a condition. Absence of a constraint needs no stored OPEN role; an unknown HARD value is not absence of that requirement.

priority_order records relative user comparison preference and material importance, not eligibility or arithmetic. Use a simple ordered list of the relevant field names when useful; preserve user-declared ties rather than inventing an order. Changing priority_order does not change HARD/SOFT roles. A lower-priority HARD criterion still blocks any conclusion depending on its satisfaction. No numeric confidence, weighted scoring, mandatory P0-P3 system or automatic price dominance. Do not invent priorities from profile membership. Pass material importance to AIS through Hub without making comparison priority a fixed research sequence.

SOFT CLUE != HARD FILTER. ROLE != PRIORITY.

### Category profiles — suggestions only

Use the relevant fields below as vocabulary/interpretation aids, only when material. A product may use fields from multiple profiles; an uncertain or unmatched Category uses the general Shopping path when sufficient. A profile supplies no default constraints or priority. Selecting a profile does not require researching every field. Discard inapplicable profile assumptions when the task changes; preserve still-relevant evidence.

| Profile | Identity / product questions | Compatibility / purchase / market questions |
| --- | --- | --- |
| ELECTRONICS | brand/model, revision, configuration, condition, specifications/performance | interface, dimensions, platform, power, stock, warranty, seller condition |
| HOME | product type/model, dimensions, material, configuration, condition | installation/space compatibility, use/care, delivery, assembly, warranty/returns |
| FOOD | variant, net weight, packaging, ingredients, origin | expiry, storage, importer/distributor, quantity, availability |
| FASHION | size, fit, color, material, variant | authenticity, size evidence, condition, returns, availability |
| PERSONAL | product type/variant, size/quantity, formulation/material where relevant | intended-use compatibility, ingredients, expiry/storage where relevant, authenticity, returns |
| HOBBY | model/edition, scale/size, configuration, completeness, condition | system/accessory compatibility, authenticity, availability, warranty/returns |

CATEGORY != PRODUCT ONTOLOGY. CATEGORY PROFILE != REQUIRED FILTER SET. PROFILE FIELD != USER REQUIREMENT.

## ProductCandidate and SKU

ProductCandidate is a possible identity under incomplete, approximate or conflicting clues. Keep matching attributes, conflicting attributes, unknown attributes, their relevant support and unresolved identity links separate. Several matches or apparently complete fields do not confirm identity. Preserve a soft size recollection's discrepancy without turning it into a hard rejection; respect an explicitly exact purchase size as HARD instead.

SKU is a sufficiently specific sellable variant. Use only materially distinguishing brand/product line, model/revision, recipe/flavor, size/net weight, packaging or configuration. A retailer's internal SKU code is optional. Do not collapse distinct variants into a product-line name or add a permanent family object merely to group variants.

Keep attribute-to-source and same-identity links. Support for one field and another field from separate records does not establish their combination as one SKU. Preserve the unsupported combination and the missing relational evidence. Candidate identity, evidence support and purchase suitability remain distinct: failing a hard purchase condition does not retroactively disprove a plausible or established historical identification.

CANDIDATE != CONFIRMED IDENTITY. SUPPORTED ATTRIBUTES != SUPPORTED SAME-SKU COMBINATION.
PURCHASE SUITABILITY != HISTORICAL PRODUCT IDENTITY.

## Offer and price scope

Offer is a seller's commercial observation attached to an exact SKU or an explicitly bounded unresolved identity. Retain seller, channel/surface, source/provenance, market/location, observation time, currency, sale unit/quantity, price, availability and conditions as applicable. A missing material value stays unknown; unresolved identity does not justify an exact-SKU price. Same seller does not mean same channel or same Offer. Keep different channel/price/stock conditions as separate observations; do not deduplicate by seller or product name alone, or infer seller identity from matching display names.

Separate list and sale prices and material voucher eligibility, payment, shipping, bundle and warranty conditions. Do not require every field for every Offer. Never invent shipping = 0, voucher/payment eligibility, confirmed physical stock, warranty or an effective total. A page's stock label remains a page claim within supplied support; a later applicable seller confirmation/conflict must retain its meaning, not be overwritten by the old listing. An unavailable or stale Offer cannot establish current availability. AIS retains qualification and freshness policy; Shopping applies those supplied conditions without a new source hierarchy or universal phone-confirmation rule.

Compare/aggregate only a defined set with compatible identity, currency, units and conditions, or an explicitly justified normalization. Separate incompatible groups or preserve the gap. An average of listed SKU prices at retailer X is only that defined retailer/SKU-set average, not a market average or each SKU's price. Missing shipping or eligibility prevents an unconditional effective-total claim, not every bounded advertised-price comparison. A historical observation outside the requested window does not establish that window's price or market direction. Preserve actual observation times and material exclusions.

SAME SELLER != SAME OFFER. RETAILER AVERAGE != MARKET AVERAGE. OFFER PRICE != UNIVERSAL PRODUCT PRICE.
LOWEST LISTED PRICE != LOWEST CONFIRMED PURCHASABLE PRICE.
LOWEST CONDITIONAL PRICE != LOWEST UNCONDITIONAL PRICE.
CHEAPEST OBSERVED OFFER != MARKET-WIDE LOWEST PRICE.
OUT OF STOCK != DISCONTINUED. NOT FOUND != NONEXISTENT.

## Target set and supplied coverage

Keep the target set explicit: retailer listings, distribution in a market, manufacturer catalog or another bounded set with relevant conditions/time. Clarify or branch on a material ambiguity in "all" rather than choosing a wider scope. Discovered items are not automatically the complete target set. Ten retailer variants do not establish ten manufacturer variants. Apply supplied supported coverage and limits; AIS owns whether external evidence supports coverage. Exhausting a search limit does not prove completeness.

DISCOVERED SET != CONFIRMED-COMPLETE SET. RETAILER CATALOG != MANUFACTURER CATALOG.

## DECIDE — supported purchase conclusions

Exclude HARD FAIL from the options satisfying the current purchase requirements. Retain HARD UNKNOWN or conflicted mandatory fields as unresolved/provisional, never PASS. Compare the remaining eligible options using relevant user priorities and supported evidence, preserving Offer conditions, exact variant differences and ties the evidence cannot resolve. Price alone does not establish overall value or satisfy another criterion.

A HARD UNKNOWN does not prohibit every useful response: a conditional recommendation, a check/request recommendation, an unresolved branch or "best among currently verified options" may be useful when its bounded basis is explicit. Do not claim all requirements satisfied or a fully qualified winner dependent on an unresolved mandatory field. Do not force one winner. Best value is derived from the actual criteria and support, not a new scoring service.

Return the requested bounded result: candidate/SKU/Offer distinctions, comparisons and arithmetic with their scope, material support/citations/conditions, discrepancies and unresolved shopping evidence needs. Preserve AIS-return status, provenance, uncertainty, conflicts and achieved coverage; a received report is not an independent source read. Missing decisive support blocks only dependent conclusions, not sufficient independent work. Return gaps to Hub; do not activate AIS, execute tools, accept global state or reinterpret the whole turn. State only the research actually supported, never a claim that a planned branch ran.

SHOPPING DOMAIN INTERPRETATION != EVIDENCE AUTHORITY. SHOPPING EVIDENCE NEED != AIS ACTIVATION.
SHOPPING APPLICABILITY != ROUTING AUTHORITY. PIPELINE SELECTION != TOOL EXECUTION.

No persistence/cross-session state, separate Storefront primitive, Category modules, ontology, retailer registry, product graph, crawler, pricing/recommendation engine, generic gates or context-expiry controls. Checkout, ordering, payment execution, monitoring and alerts are outside this candidate.
