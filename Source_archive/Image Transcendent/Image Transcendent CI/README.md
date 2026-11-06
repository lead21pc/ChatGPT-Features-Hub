# Image Transcendent CI release procedure

`ImageT_v<version>.md` is the English source for ChatGPT Project Custom Instructions. The 8,000-character limit applies to the file content, including whitespace. Keep a margin below that limit. The Git repository is a local release record; a commit does not update the ChatGPT Project.

For each release:

1. Record the repository branch, HEAD, status, and current active version.
2. Create a new immutable `ImageT_v<version>.md`. Do not overwrite an older released version.
3. Resolve the matching router, anti-prior, config, and optional template versions in the separate modules repository. Update its `manifest.yaml` and hashes.
4. Check the character count, exact filenames, load order, authority rules, template-absence behavior, and prompt-preservation cases. A static check does not prove model or image-tool behavior.
5. Copy any superseded source into `source_archive/` byte-for-byte, then verify its SHA-256 against the original before removing an imported loose copy.
6. Stage only task-owned paths. Inspect `git diff --cached --check`, `--stat`, and the full staged diff. Commit only after the relevant checks pass; verify status and latest commit.
7. Paste the active `ImageT` file into ChatGPT Project Custom Instructions and upload the matching active module files to Project Sources. Verify the deployed versions against `manifest.yaml`. Test representative prompts in that Project before claiming runtime improvement.

This repository has no remote configured. Pushing, tagging, and publishing require a separate request.
