# IMAGE SOURCE ROUTER

ROUTER_VERSION: 2.0.0
STATUS: ACTIVE
COMPATIBLE_CI: ImageT_v1.0.0.md

## 1. Release inventory

`manifest.md` is the authoritative inventory of the release uploaded to ChatGPT Project Sources. It names the active CI version and exact module filenames. The CI is Project Custom Instructions, not a Project source file. Archived files, lookalike names, prior chats, and local Git paths cannot satisfy a source load. If the manifest or this router is missing, unreadable, or inconsistent, stop before image execution.

The release maintainer verifies the manifest against uploaded Sources. At runtime, use its template state as the published existence check. If an unexpected template is available, or an active file cannot be loaded, treat the inventory as inconsistent and stop. Do not silently skip a damaged or missing active file.

## 2. Load order

After this router and the manifest are used for source resolution, process visual instructions in this order:

1. Active `ImageT_v1.0.0.md` Project Custom Instructions.
2. Required `IMAGE_ANTI_PRIOR.md`.
3. Required `config.md`.
4. Optional `template.md` only when the manifest declares it ACTIVE.
5. The user's current prompt and request-specific references.

This is processing order, not priority of visual content. The user's explicit current request defines the target. Project files may constrain interpretation, provide compatible template fields, or permit minimal neutral completion; they may not overwrite an explicit user field. Platform safety and tool limits remain binding.

## 3. Exact sources

- `IMAGE_ANTI_PRIOR.md`: required; prevent unauthorized model-prior substitution and invalid expansion of negatives.
- `config.md`: required; generic anti-drift and minimal-gap policy, not a visual specification.
- `template.md`: optional; no active template in this release. `OPTIONAL_ABSENT` in the manifest means skip it and continue to the current prompt. An ACTIVE entry requires a readable valid file.

Never use an archived or candidate version as a fallback for a missing required source. Re-read the active sources for every CREATE, EDIT, VARIATION, CORRECT, ANALYZE, or retry operation. Do not use memory as a file-load substitute.

## 4. Template contract and conflict check

When a future template is active, it must declare an identifier, version, status, scope or applicability, fields it owns, fields it does not own, and its override conditions. Treat an empty, malformed, or internally contradictory active template as unresolved and stop.

Compare each template field to the user's current prompt. Keep compatible fields. A clear explicit user change wins for only the field it changes; it does not release unrelated template constraints. When an apparent conflict affects identity, exact count, anatomy, topology, attachment, reference role, protected region, or another hard invariant and override intent is unclear, stop for the smallest clarification. Never average conflicts or replace a user requirement silently. The template cannot authorize content outside its declared scope.

If the user explicitly asks to use a template but the release declares `OPTIONAL_ABSENT`, request that template or a revised release; do not invent it.

## 5. Operation routes

- ANALYZE: inspect or discuss only. Do not generate or edit.
- CREATE: compose a new image instruction from the resolved current request.
- EDIT: preserve the input image outside the explicit edit delta as far as the tool permits.
- VARIATION: vary only fields explicitly opened by the current request or an active applicable template.
- CORRECT: reopen only failed fields when a bounded correction is possible; structural failures require a fresh creation attempt from the resolved lock.

For every operation, load the two required modules and any active template before interpreting visual details. If no image tool is being called, do not pretend the execute or verify stages happened.

## 6. References, uncertainty, and freshness

Assign each reference image only the attributes stated by the current request or an active template: for example identity, anatomy, pose, composition, palette, material, lighting, or style. Unassigned attributes are non-authorizing. Ask when an unresolved role could change a hard constraint.

`UNKNOWN` is not permission to invent. Leave optional fields unspecified where possible. A missing detail that materially changes the outcome requires clarification. A mismatch between manifest version, active file header, or current request and a reused operation lock makes the lock stale; derive a new one.
