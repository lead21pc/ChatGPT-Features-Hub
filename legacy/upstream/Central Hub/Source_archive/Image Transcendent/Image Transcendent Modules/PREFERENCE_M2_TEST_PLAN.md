# Preference candidate — M2 test plan

STATUS: CANDIDATE_TEST_PLAN
BASELINE: CI 1.0.0; Router 2.0.0; Anti-Prior 1.1.0; Config 2.0.0; Manifest 1.0.0
BASELINE_COMMIT: 3272b4e72cf1b4c449ee61e6cae38e4f8ccab1b3 (modules)
CI_BASELINE_COMMIT: f753230507c77a1b2caf907dcda29710403e6670
LIVE_RESULTS: NOT RUN

## Independent experiment

Use isolated fresh conversations with the same model, Project instructions, active sources, reference inputs and generation settings when exposed. Do not install the candidate into active Sources, change Router/Manifest, or use the Ready Gate candidate for this comparison. Copy the full preference text directly into B/C's current experiment message. A uses the baseline only. Selection applies to one operation and must be repeated explicitly for another operation. A missing/unreadable baseline source blocks every arm; the candidate is never a fallback.

Common wrapper for every arm:

> Prepare only the observable tool-facing prompt for the request below. Do not call an image tool or generate an image. Follow the baseline source route and operation lock. Preserve uncertainty rather than inventing a value. Show the final prepared prompt and material clarifications, if needed.

For B and C, append before the request:

> For this operation only, I explicitly select the following full-text CANDIDATE preference as soft guidance for components and design changes already authorized below. This is direct experimental input, not a Project source or an activation-rule change. Its restrictions and the baseline controls remain binding.

Then paste HUMANOID_CHARACTER_DESIGN_PREFERENCE.md verbatim. For C only, append:

> As an experimental check before returning the prompt, trace material details to USER-SPECIFIED, AUTHORIZED-PREFERENCE, VALID-DERIVATION, UNRESOLVED or UNAUTHORIZED. Remove unauthorized additions, retain open optional fields, and ask for material unresolved decisions. Judge small additions together. Return only the final prompt and material decisions, not private reasoning. This is a test treatment, not an implemented M4 validator.

## Fixed cases

Run each case in A/B/C. No expected output below is a claimed model result.

| ID | Exact request | Acceptance oracle |
| --- | --- | --- |
| P01 | Prepare a prompt for one humanoid character. I have not chosen clothing, color, materials, identity markers or setting. | Keep those fields open; ask only about choices materially needed. No invented costume or identity. |
| P02 | Design one clothed humanoid with exactly two arms and four visible fingers on each hand; exactly two garment layers, monochrome, no accessories. Refine the relationship between the two layers without adding components. | Exact counts, morphology, monochrome and accessory exclusion survive; relational specificity may improve. |
| P03 | One humanoid with a deliberately fragmented silhouette, uneven proportions, flat lighting and uniformly dense detail. Keep these choices. | No normalization to balance, realism or regional detail hierarchy. |
| P04 | Refine the line relationships of an existing soft coat and rigid shoulder panel on one humanoid. Their shapes and materials are fixed. Keep the current pose and palette. | May describe soft/rigid interaction; no new seams, fastening, material or pose decisions. |
| P05 | Keep deliberately conflicting line families: angular hair and flowing clothes, with no dominant style. | User choice wins; no compulsory single style system. |
| P06 | One humanoid wearing a coat. Do not choose its material or color. | No silk/leather/metal, accent color or lighting invented to satisfy drape/value preferences. |
| P07 | One plainly dressed humanoid, no new objects. Refine only existing contours. | Small guesses must not accumulate into jewelry, belts, trims or a new identity. |
| P08 | A landscape with three square towers in a flat two-color style. No characters. | Preference inapplicable even when explicitly supplied; exact tower count and style survive. |
| P09 | One humanoid with hands that are not five-fingered. Leave the exact digit count unresolved. | Retain negative; never infer exactly four. |
| P10 | Edit only the left sleeve color to blue in the supplied image. Preserve all other visible regions. | No layering, silhouette, face, accessories or composition redesign. Use the same image in all arms. |
| P11 | Use the supplied reference only for palette. One humanoid with a plain silhouette and no accessories. | Reference identity/costume/pose cannot leak. Use the same reference in all arms. |
| P12 | Variation: change only existing cloth fold rhythm. Preserve identity, anatomy, layer count, palette and pose. | Preference refines only opened fold relationships. |
| P13 | First prepare P02 under the arm's treatment (A without preference; B/C with it). Next request: prepare a landscape prompt, without selecting preference. | No carried-over activation. Use a separate matched two-turn conversation per arm. |

## Measurement and evidence

For each paired run, record case/arm/repetition, original message, model/date/settings, active source versions and hashes, supplied preference hash, attachments/roles, full visible prepared prompt, clarifications, and evidence type. Use three fresh repetitions per case, randomize A/B/C order, and score blinded to arm where feasible. Do not label the visible draft as the actual submitted payload when the latter is unobservable.

Record absolute counts, not prompt length: preserved hard constraints / applicable hard constraints; omissions; contradictions; unauthorized details; prior substitutions; out-of-domain influence; and authorized concrete relationships. A material decision must have an authorized basis. Record several small additions jointly if they create a new design. Record complexity as added instruction characters, extra clarifications and reviewer effort; record latency only when measured.

GO for a later routing trial requires no hard-constraint violation, unauthorized invention or domain leakage in B's reviewed runs, and repeatable useful authorized specificity beyond A in at least two applicable cases. Mixed results require preference revision and a rerun of affected pairs. C is optional: retain its treatment only if it detects a material error missed by B at justified cost. No improvement is proved until model runs exist; no finite suite guarantees universal compliance.

## Verification record — Phase 1

STATICALLY VERIFIED: candidate status and direct-only selection; source mapping covers P01-P21; active baseline and archives unchanged; forbidden-field authority and no activation carry-over are explicit; A/B/C treatments and 13 cases are specified.

SIMULATED: NOT RUN. No synthetic outputs are scored as model evidence.

LIVE TESTED: NOT RUN. No image tool was called; actual submitted payload is unobserved.

Handoff: M3 owns future activation; M4 owns any persistent provenance check; M6 owns integration and release. Ready Gate testing does not depend on these M2 results.
