# Shopping v0.1 — isolated candidate cases

## Baseline and evidence limits

M2 accepts the M1 thin-domain direction against the current local stack. Baseline: `main`, HEAD `28adb1adca4ccaae6b03bb547f0d1b63bf279ba3`, clean working tree, 107 existing tests PASS before edits. Current sources: Hub CI v1.1, Hub Router v1.1, Architecture v1.0, Package Catalog v1.0, official AIS pipeline v1.1/router v1.2. Existing singleton and scoped handoff contracts support this inactive candidate without active control changes.

The module is `HUB-DOM-SHOPPING_v0.1-candidate.md`, role DOMAIN_CONTROL, status CANDIDATE, package HUB-PKG-SHOPPING. It is not in the active Catalog. No activation, Library/Project configuration, active routing change or AIS modification is part of M2.

REVIEWED_TEXT: the module and expected behavior below.
STATIC VALIDATION: headers, boundary clauses, inactive admission and unchanged active-source hashes.
SPEC SIMULATION: small test-only Python oracles over declared facts, roles, identity links, support and coverage. They do not parse or execute the Markdown module, infer natural-language intent, select sources or determine actual evidence sufficiency. Support/coverage flags are supplied test premises, not Shopping-owned policies. Passing oracles prove consistency of these examples only.
LIVE CHATGPT / HUB ROUTING / LIBRARY / AIS-SHOPPING COMPOSITION: NOT RUN.

The pâté cases originate from the user's prior real-conversation observations (OBSERVED FAILURE / USER_REPORTED). Product attributes, counts and prices below are controlled test premises, not independently verified commercial facts. Neither a negative fixture nor a passing oracle reproduces a model failure. No earlier model/baseline is executed by these tests; REPRODUCED FAILURE is not claimed.

## Focused cases

| ID | Supplied input / evidence premise | Required domain result |
| --- | --- | --- |
| A01 | Country-style pâté, glass jar, metal lid, around 250 g, Ân Nam distribution, Annam Gourmet; linked evidence for Paté Royal 180 g supports the other properties; identity unresolved | Keep 180 g as a candidate, matching properties/support, explicit 250 g vs 180 g conflict and unknown identity link to the remembered item. No automatic rejection or confirmation. |
| A02 | Same evidence, but weight must be exactly 250 g | Flag hard-constraint violation and purchase unsuitability; this alone does not disprove historical identity. |
| A03 | All visible clues match; identity support still absent | Keep identity provisional. Matching fields alone grant no confirmation. |
| A04 | Explicit supplied support establishes identity within the delegated question | Permit established identity without manufacturing another universal approval gate. |
| B01 | Retailer X lists ten distinct variants; supplied coverage supports its complete listing set under stated conditions | “All ten variants listed by retailer X” is supported only for that target. |
| B02 | Same ten; requested set is manufacturer's global catalog, no matching coverage | Return ten discovered variants; manufacturer-complete claim unresolved. |
| B03 | Ten items found, no completeness support even for retailer X | Discovered set only; exhausting results does not establish “all.” |
| C01 | Two 180 g SKUs at X: normal prices 100000 and 120000 VND per jar, same declared time/location | Mean 110000 VND for this defined retailer/SKU set, not a market average or each SKU's price. |
| C02 | First SKU also has sale price 80000 VND with a stated member condition | Keep sale/normal bases and condition separate. An explicitly sale-only group can be computed; do not silently pool all three prices. |
| C03 | An offer is out of stock or its current applicability is not supported | Preserve price context; it cannot establish current availability. Out of stock is not discontinuation. |
| C04 | Empty search result; no evidence of product existence/nonexistence beyond that result | Preserve not-found observation and leave existence unresolved. |
| C05 | Prices differ in currency, sale unit, location or relevant time | No automatic pooled average; separate or require explicitly justified comparability. |
| D01 | Hub supplies all material inputs/support; no AIS report is supplied | Complete domain interpretation without requiring AIS. |
| D02 | Same-SKU relationship or other decisive input is missing | Return the exact gap to Hub; no self-selection or execution of AIS/search. |
| D03 | Source A supports brand; source B supports weight; no evidence links the records | Keep the proposed combined SKU unresolved; preserve both source links. |
| D04 | Hub successively delegates identify → enumerate → prices → compare with the same established product/SKU context | Different scoped outputs; unchanged identity, support and constraint roles absent new evidence. No persistence mechanism. |

## Negative cases

These are prohibited outcomes checked against the declared-fact oracles and the module's written guards, not observed outputs of the candidate in ChatGPT.

| ID | Prohibited escalation | Check |
| --- | --- | --- |
| N01 | Soft clue → hard rejection filter | A01 vs A02 preserves the supplied condition role. |
| N02 | Candidate → confirmed identity without support | A03 stays provisional; A04 needs explicit support plus linked attributes. |
| N03 | Retailer catalog → manufacturer catalog | B02 lacks matching target coverage. |
| N04 | Discovered set → exhaustive set | B03 retains the completeness gap. |
| N05 | One retailer average → market average | C01 labels only the defined retailer/SKU set. |
| N06 | Offer price → universal product price | C01/C02 keep seller, SKU and conditions in returned offers. |
| N07 | Out of stock → discontinued | C03 returns only local availability and unresolved discontinuation. |
| N08 | Not found → nonexistent | C04 leaves existence unresolved. |
| N09 | Shopping evidence gap → self-activation of AIS | D02 returns gaps to Hub; the test oracle performs no pipeline selection or tools. |
| N10 | Shopping applicability → Hub routing authority | Candidate excluded from active Catalog; module retains explicit Hub routing boundary. |

## Verification and smallest later behavioral test

From the Central Hub root:

```powershell
python -B -m unittest discover -s tests -p test_shopping_candidate.py -v
python -B -m unittest discover -s tests
git -c core.longpaths=true diff --check
```

New untracked files also need direct UTF-8/BOM, newline/EOF and trailing-whitespace checks because ordinary git diff does not include them. Existing active-package assertions remain unchanged.

After separate authorization, evaluate the full candidate text in an isolated model context with simulated Hub handoff and the fixed premises above; do not register/upload it as active. Start with the paired A01/A02 case, then B/C and boundary cases, including D04 as one conversation. Record exact candidate revision, prompt/evidence packet, model/surface/date, outputs and concrete PASS/FAIL/UNVERIFIABLE reasons. No actual search is needed for these supplied-evidence tests. A request to fill D02 must yield a gap for Hub rather than a tool call. Check observable output and calls, never private reasoning. These runs would test candidate behavior only, not live Hub routing or AIS integration. They have not been run in M2.

## M2 architecture audit

A–C are expressible with ProductCandidate, SKU and Offer plus ordinary distinctions for condition role and set completeness. No additional permanent primitive proved necessary; none of the three was eliminated. The oracles are test code only, not a product resolver, pricing service, Router or evidence engine. No concrete test requires changing Hub CI, Hub Router, Package Catalog, Architecture, AIS pipeline/router or Prompt Authoring for this isolated candidate.

Later activation is technically compatible with the existing package model but requires separately authorized Catalog admission/binding, reconciliation of Architecture's five-package/milestone descriptions and affected active-inventory tests. That is not implemented or verified here. There is no new architectural mechanism required by these fixtures.
