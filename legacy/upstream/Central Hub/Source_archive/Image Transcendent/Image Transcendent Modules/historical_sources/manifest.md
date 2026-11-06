# Image Transcendent release manifest

MANIFEST_VERSION: 1.0.0
STATUS: ACTIVE
RELEASE_ID: image-transcendent-1.0.0

This manifest defines the intended ChatGPT Project inventory. During deployment, paste the `ImageT` file into Project Custom Instructions and upload the three active modules plus this manifest to Project Sources. Do not upload archived files. SHA-256 values verify local release bytes; the active version headers and exact filenames are the runtime identifiers when hash computation is unavailable.

| Role | Exact filename | Version | Status | SHA-256 |
| --- | --- | --- | --- | --- |
| Project Custom Instructions | `ImageT_v1.0.0.md` | 1.0.0 | ACTIVE | `41C9F56548C967CB1BC157E352EE11923CD82A9C68B933735B46EBB950D178F8` |
| Router | `IMAGE_SOURCE_ROUTER.md` | 2.0.0 | ACTIVE | `DE3DAF811C5B14E03EA24DC101655AA0D177153A29C6C6C7C768EE76B6732227` |
| Prior guard | `IMAGE_ANTI_PRIOR.md` | 1.1.0 | ACTIVE | `74636C2FFEC98E1A03D1D5EB96C463891C5C5993B7E8FB4EF02B47F3C2663FBA` |
| Anti-drift config | `config.md` | 2.0.0 | ACTIVE | `3DDF4DED0402ED0341A4F893331F17531E9206EBBABFF731B56DA1C981E247CF` |
| Optional visual template | `template.md` | none | OPTIONAL_ABSENT | none |

`OPTIONAL_ABSENT` records the verified local release state: no active `template.md` is supplied. It authorizes skipping only that module after the deployed Project inventory is checked against this manifest. If a template is later added, update this manifest, validate its declared scope and conflicts, and release a compatible new CI version before declaring it ACTIVE. If an active template unexpectedly appears or a declared active source cannot be read, treat the release as inconsistent and stop.

## Original source provenance

The old files below are byte-identical archives, not active Project Sources. Their SHA-256 values were checked against the loose originals before removal.

| Archive | Original SHA-256 |
| --- | --- |
| `../Image Transcendent CI/source_archive/CI.md` | `A2BCE4EF9275B99441AC420C4CEE36AD98D053278E9FD9519A7F7765CCDACEBC` |
| `source_archive/03-01-IMAGE_SOURCE_ROUTER-1-.md` | `AAC3D5326C663334332A5C95E9EBB41445E9DF61EA23311CADA316FB946B2ABC` |
| `source_archive/IMAGE_ANTI_PRIOR.md` | `3083B0A6DE6843845F50C5A23073864254DDDFEC651EF9D5EDE6D749DBC0033E` |
| `source_archive/02-02-config-1.md` | `1458EFF9790C02BF146CCA48232A7D352308A00F8FA1B684EBA5A32B94FF8FAA` |

## Release checks

Before a commit, confirm: exact active filenames and headers match this table; the CI contains at most 8,000 characters and is English; the route specifies required loads and template-absence behavior; the prompt-preservation rules cover the review cases; archives match the original hashes; and both Git staged diffs contain only task-owned files. Review the cases in `ROUTE_TEST_CASES.md`, then test representative prompts in the actual ChatGPT Project after deployment. Static validation does not establish model or image-generator compliance.
