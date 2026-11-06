# IMAGE SOURCE ROUTER

ROUTER_VERSION: 1.2
STATUS: ACTIVE

## 0. PRE-REQUEST CONFIGURATION LOAD

At Project or image-workflow initialization, load `config.md` before accepting, interpreting, classifying, or composing any image request.

- `config.md` is a pre-request dependency, not a source loaded after an operation has already been inferred.
- Do not analyze the image request, select an operation, inspect references, compose a prompt, or call an image tool until this load succeeds.
- The loaded configuration establishes the active aesthetic vocabulary, applicable exclusions, and permitted aesthetic defaults against which the later request is resolved. It does not authorize invention of subject-specific fields declared `UNSET_BY_THIS_FILE`.
- A request may override `config.md` only through an explicit current instruction and only for the fields it actually releases or changes.
- If `config.md` is missing, unreadable, ambiguous, stale by its own rule, or internally unresolved, stop before processing the image request and identify that exact dependency.
- Conversation memory, a prior load from another Project, or a visually similar earlier request never satisfies this gate.

## 1. REQUIRED CONTROL FILES

- FILE: `IMAGE_GENERATION_CI.md`
  STATUS: REQUIRED
  AUTHORITY: execution route, operation lock, anti-drift, prompt composition, and verification

- FILE: `IMAGE_ANTI_PRIOR.md`
  STATUS: REQUIRED
  AUTHORITY: prior suppression, controlled gap filling, and prior-failure verification

## 2. DEFAULT ACTIVE CONFIGURATION

- FILE: `config.md`
  STATUS: REQUIRED
  AUTHORITY: aesthetic base, visual-language constraints, applicable palette and material rules, exclusions, known failure modes, and the interface used to derive an operation lock
  NON_AUTHORITY: subject identity, exact counts, anatomy, topology, attachment, reference roles, operation-specific composition, and operation stop condition unless explicitly assigned by a higher-authority current source
  LOAD_PHASE: PRE_REQUEST

## 3. OPERATION ROUTES

### ANALYZE

- REQUIRED: `config.md`, `IMAGE_ANTI_PRIOR.md`
- OPTIONAL: `[files or NONE]`
- FORBIDDEN: `[files or NONE]`
- OUTPUT_BOUNDARY: Analysis only; do not generate or edit.

### CREATE

- REQUIRED: `config.md`, `IMAGE_ANTI_PRIOR.md`
- OPTIONAL: `[files or NONE]`
- FORBIDDEN: `[files or NONE]`

### EDIT

- REQUIRED: `config.md`, `IMAGE_ANTI_PRIOR.md`
- OPTIONAL: `[files or NONE]`
- FORBIDDEN: `[files or NONE]`
- PRESERVATION_RULE: Preserve every property and region outside the explicit edit delta as far as the tool permits.

### VARIATION

- REQUIRED: `config.md`, `IMAGE_ANTI_PRIOR.md`
- OPTIONAL: `[files or NONE]`
- FORBIDDEN: `[files or NONE]`
- VARIABLE_FIELDS: `[exact fields allowed to vary]`
- PRESERVED_FIELDS: `[exact fields that remain invariant]`

### CORRECT

- REQUIRED: `config.md`, `IMAGE_ANTI_PRIOR.md`
- OPTIONAL: `[files or NONE]`
- FORBIDDEN: `[files or NONE]`
- CORRECTION_RULE: Reopen only failed fields; preserve all other verified fields.

## 4. SOURCE STATUS

Allowed status values:

- `ACTIVE`: binding for the current operation.
- `CANDIDATE`: evaluable but not binding by default.
- `LEGACY`: historical context only.
- `RETIRED`: inactive until explicit reactivation.
- `REFERENCE_ONLY`: limited to the assigned reference role.
- `UNKNOWN`: unresolved and non-authorizing.

The router must not promote a source based on similarity, repetition, usefulness, familiarity, or apparent completeness.

## 5. REFERENCE-ROLE MAP

Assign each reference only the attributes it may supply.

- `[reference filename]`: `[identity | structure | anatomy | pose | composition | palette | material | lighting | style | detail]`

Unassigned attributes have no authority. If a reference serves several roles, list them explicitly. If its role is unresolved, generation is blocked when that ambiguity can change a hard constraint.

## 6. AUTHORITY AND CONFLICT ORDER

Declare the exact Project-specific order:

1. `[highest-authority active configuration]`
2. `[operation-specific source or overlay]`
3. `[base configuration]`
4. `[reference-only evidence]`

The user's current explicit request remains above Project files unless it conflicts with platform safety or tool constraints.

Do not average incompatible sources. Preserve explicit negatives. Block execution when an unresolved conflict changes identity, count, anatomy, topology, composition, coverage, reference role, or another invariant.

## 7. FRESHNESS AND REUSE

- RELOAD_WHEN: `[every operation, or exact observable conditions]`
- REUSE_ALLOWED_WHEN: `[exact conditions or NEVER]`
- STALE_WHEN: `[version mismatch, changed request, changed source, or other conditions]`

Conversation memory does not satisfy a file-load requirement.

## 8. MISSING-SOURCE RULE

Any missing, unreadable, ambiguous, stale, or unresolved `REQUIRED` source blocks execution.

When blocked:

1. identify the exact dependency;
2. do not reconstruct it from memory or convention;
3. request only the minimum information needed to restore the route.

`UNKNOWN != PERMISSION TO INVENT`

## 9. PROJECT CONFIGURATION CONTRACT

Every routed visual configuration should declare at minimum:

- stable identifier, version, and status;
- its role, scope, authority, non-authority, and applicability conditions;
- subject identity and defining silhouette, or an explicit declaration that the file does not own those fields;
- exact counts, anatomy, topology, and attachment rules, or an explicit declaration that they remain unset by that file;
- composition, viewpoint, pose, spatial relationships, and required visibility, or the authorized source from which they must be derived;
- visual language, line behavior, shape language, and detail density;
- palette, lighting, background, materials, and surface treatment;
- invariants, allowed variables, negative constraints, and known failure modes;
- reference assignments or an explicit declaration that they remain unset;
- its own completion boundary and the source of the operation-specific stop condition.

An explicit unset declaration is non-authorizing. It requires resolution from the current request or another routed source and must never be treated as permission to fill the field from model prior.

The configuration may use any filename, but the exact filename and authority must be declared above.
