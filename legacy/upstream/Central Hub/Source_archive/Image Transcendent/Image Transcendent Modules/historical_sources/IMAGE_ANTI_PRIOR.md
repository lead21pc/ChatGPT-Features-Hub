# IMAGE ANTI-PRIOR

ANTI_PRIOR_VERSION: 1.0
STATUS: ACTIVE

## 1. FUNCTION

This file controls model-default substitution during image analysis, prompt composition, generation, editing, variation, and correction.

Project sources and the current explicit request define the target. Statistical familiarity, aesthetic preference, genre convention, and tool tendency never define it.

`MODEL PRIOR = FALLBACK MATERIAL, NOT AUTHORITY`

## 2. FORBIDDEN SUBSTITUTION

Do not replace the routed target with:

- the statistically typical form of the subject;
- contemporary human anatomy when stylized anatomy is specified;
- genre-standard costume, pose, palette, lighting, framing, expression, proportions, or setting;
- generic cinematic polish or concept-art treatment;
- automatic realism, beautification, sexualization, cuteness, grittiness, symmetry, or heroic exaggeration;
- familiar franchise traits not assigned by an active source;
- semantic associations inferred from a name, occupation, species, culture, era, object class, or style label;
- details inherited from a reference outside its assigned role;
- corrections that merely make an intentional design more conventional.

## 3. SPECIFIC OVERRIDES TYPICAL

An explicit, active instruction wins when it conflicts with a common visual convention, even when the requested result is unusual, sparse, asymmetrical, flat, disproportionate, awkward, or historically specific.

Do not normalize intentional:

- anatomy or digit structure;
- asymmetry;
- silhouette or proportion;
- limited or absent color;
- flat lighting or low detail;
- negative space;
- period-specific graphic language;
- unconventional attachment, layering, pose, or framing.

Unusual does not mean erroneous. Familiar does not mean authorized.

## 4. CONTROLLED GAP FILLING

For each genuinely unresolved field:

1. Prefer leaving it neutral or visually unobtrusive when possible.
2. Choose the lowest-impact value compatible with active sources.
3. Avoid choices that add semantics, alter silhouette, change topology, rebalance composition, or imply narrative.
4. Never use gap filling to bypass a negative constraint.
5. Never let several low-impact guesses accumulate into a new design direction.
6. Ask the user only when the alternatives would materially change the requested result.

Silence in one field does not authorize importing a whole convention bundle.

## 5. NEGATIVE CONSTRAINTS AS CONSTRUCTION

Keep every explicit negative binding, and also translate critical negatives into positive construction rules where possible.

Examples:

- `not five fingers` -> `exactly four visible digits, with no hidden, overlapping, or implied extra digit`;
- `not a modern human hand` -> `simplified vintage cartoon-glove anatomy with rounded segmented digits`;
- `no added color` -> `retain the declared monochrome or source palette only`;
- `no redesign` -> `preserve all non-target geometry, materials, and placement`.

The positive translation clarifies execution; it never deletes or weakens the original exclusion.

## 6. PRIOR-RISK CHECK

Before execution, identify only the priors relevant to the current task:

- What familiar default could replace the specified structure?
- What conventional beautification could alter identity or scope?
- Which reference might leak unassigned attributes?
- Which negative is likely to be ignored unless expressed as geometry?
- Which unresolved choice could introduce unintended meaning?

Convert each material risk into a prompt constraint or verification item. Do not expand the task with speculative risks unrelated to the active design boundary.

## 7. VERIFICATION

Fail the result when a visible model default has replaced or normalized an active requirement, even if the result appears polished.

Classify the defect by consequence:

- local prior leak: one bounded field can be corrected without changing the design;
- structural prior takeover: identity, anatomy, count, topology, silhouette, composition, or visual language has been replaced;
- unverifiable: the output hides the field needed to determine whether substitution occurred.

The generated image is evidence of tool behavior, not authority for future turns.

