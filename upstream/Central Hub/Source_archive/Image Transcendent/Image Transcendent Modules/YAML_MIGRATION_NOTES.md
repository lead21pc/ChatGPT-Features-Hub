# Published YAML migration candidate

This migration is published as repository sources; it does not establish a new production release identity or deployment to a ChatGPT Project. `manifest.yaml` retains the baseline release ID and explicitly records `repository_published_candidate` with `published: true` and `publication_scope: repository_sources`. Its hashes describe these exact local bytes. Baseline CI remains the default; Ready Gate remains a candidate.

## Ownership

The manifest owns exact inventory, versions, hashes, active/candidate status, selectability, selection scope and compatibility version requirements. The router owns generic selection, source resolution, activation, conflicts, failures and operation routing. The router contains no CI filename or candidate ID. CI files retain instruction semantics and delegate source compatibility to the manifest.

The existing humanoid preference is inventoried but inactive and not selectable through source routing. Its existing explicit direct-input experiment contract is unchanged. The Ready Gate candidate still requires no preference and activates none. No preference routing milestone is implemented here.

## Local verification

From this modules directory run:

```powershell
python -B -m unittest discover -s tests -v
```

Requires PyYAML; the migration was checked with 6.0.3. No application runtime or image tool uses this test oracle. Static checks validate conservative YAML, hashes, headers, compatibility, character limits, preserved instruction bodies and archive provenance. Simulated cases validate the declared selection outcomes and Ready Gate pending state. Actual ChatGPT loading, prompt preparation, approval handling, submitted payload and image compliance are NOT TESTED.

Hash computation may be unavailable inside ChatGPT. The router then requires exact filenames and version headers and reports hash verification as unverified; it must not claim byte integrity. Local paths in the manifest are for local validation only and cannot satisfy a Project Sources load. The manifest excludes its own hash to avoid self-reference.

## Proposed isolated trial, not performed

1. Verify all manifest hashes locally. Provide only the manifest, router and required active modules as Project Sources; paste the chosen CI as Project instructions. Do not upload archives or dormant preference candidates.
2. Baseline trial: make no candidate selection; confirm the installed instructions match the manifest's active CI.
3. Candidate trial: explicitly select the candidate by its manifest ID, identify an isolated test Project and test session, and install the exact candidate instructions. Confirm compatibility and required sources before prompt preparation.
4. Run a simple CREATE request from the Ready Gate plan. Record selected sources, exact displayed prompt, pending state and absence of generation before approval. Separately check one-call approval, revisions, stale context and ANALYZE behavior.
5. End the test explicitly. Clear selection and restore baseline instructions before the next operation. Ending a test never edits active release state.

## Rollback evidence

The retired Markdown manifest and router are preserved byte-exact under the existing `source_archive/`; all prior archive entries remain in the YAML manifest with their original hashes. Archives are never runtime fallback sources. A deliberate rollback must restore a matching whole stack, including pre-migration CI references and compatibility headers, from the baseline Git snapshots:

- CI: `ea1884d38e32629a1e432a93e69591d5f51d219d`.
- Modules: `f5b7e6753f1df37916ff725b630367e4cc438137`.

Repository publication does not install Project instructions or Sources. No rollback, Project installation or live test was performed. Original source checkout history remains available separately.
