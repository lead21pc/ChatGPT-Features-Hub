# Prompt Authoring 0.3 — repository promotion and later deployment

Date: 2026-10-28 (Asia/Bangkok). Scope: local repository implementation only.

## Implemented repository topology

```text
Hub CI 1.1 (unchanged)
-> Hub Router 1.1 (algorithm unchanged; exact pins only)
-> Architecture 1.2 / root Catalog 1.2
   -> HUB-PKG-AUTHORING
      -> HUB-CAP-AUTHORING / CAPABILITY / ACTIVE / 0.3
```

The active repository artifact is `library_modules/HUB-CAP-AUTHORING_v0.3.md`. It is a root singleton intended for `ChatGPT Library / Central Hub Config`, with `local_catalog: null`, no hard `requires` and no declared `REFINES` or `COMPLEMENTS`. Target adaptation creates no target dependency.

The root Catalog permits selection only when the first non-empty user-authored line exactly equals one of the six case-sensitive `/AUTHOR <TARGET>` forms with one ASCII space and no surrounding whitespace or extra text. This is Catalog admission metadata, not a second module body or a new Router algorithm.

Repository status after this implementation:

```text
REPOSITORY IMPLEMENTED / STATICALLY VERIFIED
LIBRARY INSTALLATION NOT PERFORMED
LIBRARY BINDING NOT VERIFIED / UNRESOLVED
PROJECT DEPLOYMENT NOT PERFORMED
LIVE ROUTING NOT RUN
```

Prior Hanfu B/C and `/AUTHOR IMAGET` results remain candidate behavioral evidence only. They are not promoted-runtime evidence.

## Manual deployment sequence — not executed here

1. In `ChatGPT Library / Central Hub Config`, ensure no existing object can create an ambiguous `HUB-CAP-AUTHORING / HUB-PKG-AUTHORING / CAPABILITY / ACTIVE / 0.3` identity. Do not select by filename or apparent newest revision.
2. Install the exact full content of `library_modules/HUB-CAP-AUTHORING_v0.3.md` in that Library root. Do not place it in Project Sources.
3. Open the installed object and read `FULL_FILE`. Verify Module ID, Package ID, Runtime role, Status, Version and material body against the repository artifact. Complete sufficiently scoped listing/search coverage for plausible matches; multiple valid ACTIVE identities or incomplete coverage leaves the binding `UNRESOLVED`. Hidden internal IDs may remain null when the platform does not expose or require them. Do not fabricate `library_file_id`, `library_version_id` or a durable locator.
4. Preserve the currently working Project stack until step 3 succeeds. Then switch Project Sources as one compatible set to `HUB_ROUTER_v1.1.yaml`, `HUB_ARCHITECTURE_v1.2.md` and `HUB_PACKAGE_CATALOG_v1.2.yaml`. Keep `HUB_CI_v1.1.md` unchanged in Project Instructions. Replace the prior Architecture/Catalog authority; do not run both root Catalog revisions simultaneously.
5. Confirm Router pins resolve exactly Architecture 1.2 and Catalog 1.2. Confirm AIS, ImageT, TECHNICAL and Concept Development bindings remain unchanged.
6. Run only S1–S3 below in fresh controlled Central Hub turns. Record exact revisions, model/surface/date, actual Library read evidence, selection, output and blockers. A model claim that it read the module is not retrieval proof.
7. Only after the controlled switch and smoke results are acceptable should the prior deployed stack be retired from active authority. Keep recoverable rollback material, but never as automatic fallback.

## Later live smoke fixtures — NOT RUN

### S1 — positive GENERIC

Copy as one user message:

```text
/AUTHOR GENERIC
Write a concise downstream prompt that asks an assistant to compare two note-taking methods for a personal creative project. Preserve that no method has been selected yet. Return the prompt only; do not execute it.
```

Expected: Authoring is selected, returns a prompt artifact and does not execute it or select a method.

### S2 — positive IMAGET

Copy as one user message:

```text
/AUTHOR IMAGET
Create an image-facing prompt from this frozen concept state: an affluent late-Ming Jiangnan woman's autumn daytime clothing; proposal P remains provisional, option R remains rejected, and collar/combination details remain open unless the supplied evidence and decision authority both permit closure. Preserve open, provisional and rejected state. Do not create or pass a Ready Gate and do not generate an image.
```

Expected: Authoring is selected, preserves decision constraints and state, creates an image-facing prompt, and neither creates/approves a Ready Gate nor generates.

### S3 — negative semantic-intent control

Copy as one user message:

```text
Please help me write a prompt for another assistant that compares two note-taking methods. Do not execute the resulting prompt.
```

Expected: `HUB-PKG-AUTHORING` is not selected merely from prompt-writing intent; normal Hub behavior continues. `PROMPT-AUTHORING INTENT != AUTHORING ACTIVATION`.

## Deliberate rollback — not automatic fallback

If the new active stack fails after manual deployment:

1. Stop Authoring-dependent execution and preserve the failure evidence.
2. Explicitly restore the prior compatible Router snapshot, Architecture 1.1 and root Catalog 1.1 from `Source_archive/Authoring promotion 2026-10-28/` into Project Sources as one authority set; keep Hub CI 1.1 unchanged.
3. Remove or disable the promoted Authoring Library binding from the active deployment, or move it outside the active discovery root using a recoverable platform-supported action.
4. Reverify the restored exact stack and its prior bindings before dependent use.

Do not keep Catalog 1.1 and 1.2 as simultaneous authorities. Library resolution failure never triggers an automatic repository/Project Source/archive substitute.

`ROLLBACK != FALLBACK`

## Provenance

The predecessor Architecture 1.1, Catalog 1.1, pre-pin Router 1.1 snapshot and v0.3 candidate are preserved byte-exact under `Source_archive/Authoring promotion 2026-10-28/` after successor verification. Archived sources are historical/rollback evidence only, never runtime discovery or fallback.
