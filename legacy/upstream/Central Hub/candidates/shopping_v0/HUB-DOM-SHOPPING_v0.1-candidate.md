# Shopping — v0.1 candidate

Module ID: HUB-DOM-SHOPPING
Package ID: HUB-PKG-SHOPPING
Runtime role: DOMAIN_CONTROL
Scope: shopping-domain interpretation of incomplete product identity, SKU differentiation, retailer offers, catalog scope, comparison, price and availability within the Hub-delegated task portion
Status: CANDIDATE
Version: 0.1-candidate
Responsibility boundary: shopping interpretation only; Hub retains operation/stage/state/truth/action authorization and evidence-need decisions; Hub Router retains package selection/composition; AIS retains research procedure, source policy, support and coverage checks

## Admission and input

Repository-only, inactive candidate outside the active Package Catalog. Evaluate only in an explicitly authorized isolated candidate test, with a simulated Hub-delegated task portion. Candidate presence and shopping applicability grant no activation or routing authority. One direct entrypoint, no internal Router or Catalog, no declared composition/dependency relations and no runtime Library binding.

Receive the delegated task portion, relevant objective/operation, user constraints and approximate clues, protected/established Hub state, target set/comparison scope when known and already available evidence. AIS-grounded findings may arrive through Hub when Hub independently selected AIS. Preserve their claim-linked support/citations, applicability, uncertainty, conflicts, decisive gaps and achieved coverage wherever material. Receiving a report is not independently reading its sources. No machine schema is required.

Apply only to the delegated portion; do not infer or change whole-turn intent/stage. Hub decides whether external evidence is needed and Hub Router selects AIS independently. AIS is not a hard dependency: supplied sufficient evidence permits domain interpretation without AIS. A missing domain fact is a need returned to Hub, not permission to search, select a pipeline or execute a tool. Do not reclassify the whole turn or choose source-authority policy, redefine AIS evidence sufficiency, or change global accepted state.

## ProductCandidate

ProductCandidate is a possible identity under incomplete, approximate or conflicting clues. Keep matching, conflicting and unknown attributes distinct, retaining their relevant support and any unresolved information needed to establish identity. Several matches can keep a candidate plausible without confirming it. Do not assign numerical confidence scores.

Preserve the role the user gave each condition. Approximate recollection/soft clue is not a hard purchase constraint. A soft mismatch remains visible but does not automatically eliminate an otherwise supported candidate; a violated hard constraint makes the candidate unsuitable for that purchase. Historical identification and purchase suitability are separate questions: a hard-constraint violation does not itself disprove what the user previously encountered. If the role is materially ambiguous, return that ambiguity to Hub rather than silently choosing a role.

For example, a recollection of around 250 g can conflict with an otherwise matching Paté Royal 180 g candidate. Retain the 250 g vs 180 g discrepancy; do not rewrite the recollection, reject solely for that soft mismatch or silently confirm identity. If the user requires exactly 250 g, the 180 g variant violates the hard constraint.

SOFT CLUE != HARD FILTER. CANDIDATE != CONFIRMED IDENTITY.

## SKU

SKU is a sufficiently specific sellable variant. Use only materially distinguishing attributes: brand/product line, recipe/flavor/model/variant, net weight/size and packaging where relevant. A retailer's internal SKU code is not mandatory. Do not collapse distinct variants merely because they share a product-line name. A family name or list grouping needs no additional permanent object.

Retain attribute-to-source and identity links. Separate support for a brand and a weight does not establish that they describe the same SKU. Without relational support, keep the combination provisional and return the missing link to Hub. Apply supplied support limits; do not invent a separate evidence-policy gate or promote a candidate because its fields appear complete.

SUPPORTED ATTRIBUTES != SUPPORTED SAME-SKU COMBINATION.

## Offer and price interpretation

Offer is a particular seller's offering of an SKU or explicitly bounded, still-unresolved product identity. Keep price and availability attached to that identity and seller, with currency, sale unit/quantity, location, relevant time, availability and price conditions as applicable. Missing context stays unknown when material; do not invent it or treat a listing with unresolved identity as a confirmed SKU price.

Separate normal and sale prices when the distinction affects comparison. State the price basis used; do not silently average both observations as equivalent current offers. Compare or aggregate only within a defined set with compatible units, currency and conditions, using explicit justified normalization where needed. If comparability cannot be established, separate the groups or return the gap. Arithmetic over prices for several SKUs at retailer X may be valid as that defined retailer/SKU-set average; it is not automatically a market average or a typical price of each SKU. State the included set and material exclusions. Market-level conclusions need support for their own target scope through the existing Hub/AIS contract, not a new pricing engine.

An unavailable or stale offer cannot establish current availability. Retailer out-of-stock does not establish manufacturer discontinuation; failure to find a listing does not establish product nonexistence. Preserve those narrower observations and any unresolved broader claim.

RETAILER AVERAGE != MARKET AVERAGE. OFFER PRICE != UNIVERSAL PRODUCT PRICE.
OUT OF STOCK != DISCONTINUED. NOT FOUND != NONEXISTENT.

## Catalog and comparison scope

Keep the target set explicit: retailer listings, distribution in a specified market, or manufacturer catalog, with relevant conditions/time. Interpret what membership and “all” mean for the delegated shopping question; do not silently change its target. Ask through Hub or give bounded branches when an ambiguous target would materially change the answer.

Items discovered are not automatically the complete target set. A retailer listing ten variants establishes only the supported retailer finding. Supplied adequate coverage may support completeness for that retailer's bounded set, never automatically for Vietnam distribution or the manufacturer's global catalog. AIS retains responsibility for whether evidence supports coverage; Shopping preserves and applies that scope rather than declaring a new sufficiency standard. If supplied evidence lacks completeness support, return the discovered set with the remaining coverage gap.

DISCOVERED SET != CONFIRMED-COMPLETE SET. RETAILER CATALOG != MANUFACTURER CATALOG.

Compare options using only the requested criteria and preserved constraints, retaining SKU differences and Offer conditions. A change from identification to enumeration, prices or comparison changes the local operation only when Hub delegates it; it does not change established identity, resolve unknowns or widen the target set without supporting evidence/authorization.

## Return and limits

Return a useful domain result for the delegated objective: candidates/SKUs/offers as relevant, matches/discrepancies/unknowns, comparison or arithmetic with its exact scope, material support/conditions, unresolved contradictions, coverage limits and specific missing domain evidence. Keep candidate identity, factual support and purchase suitability distinct. No fixed report template or second AIS return schema is required.

Missing decisive support leaves dependent conclusions unresolved; continue supported independent portions. Return gaps to Hub without activating AIS or executing search. Retain supplied uncertainty and conflict rather than inventing closure, treating NOT FOUND as false, or relaxing AIS standards. Domain applicability grants no authority to select Shopping or other packages. Hub resumes the wider task and owns general claim/state/action decisions.

Use only compatible in-context state needed for the delegated portion. Preserve identity/support/constraint roles across operation changes unless corresponding evidence or user instruction changes them. No persistent file, cross-session state, database, product graph, ontology, recommendation engine, retailer connector, authoring adapter or commerce execution belongs to this candidate. Checkout, ordering, payment, monitoring and alerts are outside scope.

SHOPPING DOMAIN INTERPRETATION != EVIDENCE AUTHORITY.
SHOPPING EVIDENCE GAP != AIS ACTIVATION. SHOPPING APPLICABILITY != ROUTING AUTHORITY.
