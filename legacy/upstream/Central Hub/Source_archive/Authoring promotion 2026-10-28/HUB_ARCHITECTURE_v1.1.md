# Central Hub — shared infrastructure integration architecture v1.1

Module ID: HUB-CORE-ARCH
Runtime role: CORE_ARCHITECTURE
Scope: shared Central Hub topology, module/package identity, Library resolution, composition and common failure behavior
Status: ACTIVE
Version: 1.1
Responsibility boundary: shared technical architecture only; no global behavior, domain, pipeline or tool authorization ownership

## 1. Status and ownership

This v1.1 runtime contract is ACTIVE in the repository; Project deployment is not verified by this local operation. It takes effect only after manual installation of the exact compatible CI/Router/Architecture/Catalog stack; file presence does not activate it. Hub CI retains action authorization. Normal core activation does not promote other candidate packages. The preceding singleton stack is preserved byte-exact for explicit rollback; it is not an automatic runtime fallback.

This document defines only the shared technical architecture. Hub CI retains operation/stage/state/truth/action, verification need, general authorization and explanation. Hub Router retains scoped selection/composition. Packages/modules retain specialized behavior; pipelines retain internal procedures. This document owns no domain knowledge, AIS methods, ImageT generation mechanics, tool authorization internals, canon/semantic truth or shared subject ontology.

The contract is not an executable program, resolver service or state engine. Add no registry, graph engine, scoring, ranking or package manager.

Runtime control language: English only for Hub CI, Router, Architecture, Package Catalogs, selectable control modules and pipeline control/config artifacts. This rule does not apply to user-authored content, quoted evidence, source/domain or worldbuilding material, historical artifacts, or non-runtime human notes.

## 2. Runtime topology

| Location | Target contents |
| --- | --- |
| Project Instructions | Hub CI only |
| Project Sources | Hub Router, shared architecture, root package Catalog, AIS core, ImageT core |
| ChatGPT Library / Central Hub Config | TECHNICAL ACTIVE/1.0; concept-development entrypoint/catalog ACTIVE/1.0; CREATIVE/BRAINSTORM ACTIVE/1.1 under HUB-PKG-CONCEPT-DEVELOPMENT. The four concept objects were observed in a root-scoped listing and verified by FULL_FILE identity/content plus byte-exact repository comparison. A later integrated runtime smoke was user-confirmed PASS; individual internal retrieval traces were not independently verified |
| Repository only | Tests, candidate development, migration reports, archives |

AIS core includes its pipeline/router and internally owned dependencies. ImageT core continues to include controller/router/manifest, anti-prior/config and required Ready Gate; do not relocate them by inference from this topology. The current preference remains candidate/inactive/direct-input-only; no promotion or activation-contract change.

TECHNICAL retains its Library-only ACTIVE/1.0 binding. HUB-PKG-CONCEPT-DEVELOPMENT is a growing Library-only package: one DOMAIN_CONTROL entrypoint, one PACKAGE_CATALOG and two independently selectable leaves. CREATIVE retains DOMAIN_CONTROL and BRAINSTORM retains CAPABILITY; both keep their canonical Module IDs and bind Version 1.1 under the new Package ID. After the migration commit, a ChatGPT-observed/user-provided smoke inspection found the four new objects in Central Hub Config, completed their FULL_FILE reads, matched their identities/content and verified byte-exact equality with the repository artifacts; no duplicate for those identities was observed in the inspected root-scoped listing. Codex did not independently reproduce that Library inspection. A later user-confirmed integrated Central Hub runtime smoke exercised exact Hub/AIS/TECHNICAL/Concept/Brainstorm/Creative revisions and passed for that scoped path. It does not prove every internal retrieval event, all C01-C12 cases, unrelated paths or a global Hub pass. Old BRAINSTORM/1.0 UI evidence remains old-package/revision evidence and is not reused for 1.1. AIS/ImageT retain their Project Sources. ONE PACKAGE = ONE RUNTIME BINDING. MIXED STORAGE != DUAL FALLBACK. No standalone Creative/Brainstorm package remains in the current root Catalog; old stack artifacts are explicit rollback/history only.

## 3. One canonical module identity and package context

MODULE ID != VERSION. FILENAME != IDENTITY. SEARCH HIT != VERIFIED MODULE. HEADER MATCH != ACTIVATION.

In the target architecture, each runtime artifact has exactly one canonical Module ID, stable across renames, path changes, versions and relocation within Central Hub Config. Runtime role distinguishes behavior type; do not create competing Domain/Capability/Pipeline ID systems. A prefix alone establishes no scope, role or authority.

Package ID is the stable technical ownership and resolution context of a package that may grow; it is not a second artifact identity. MODULE ID = concrete runtime artifact identity. PACKAGE ID = technical ownership / resolution context. A package may have only one entrypoint. A local catalog artifact also has its own Module ID and its owning Package ID.

PACKAGE MEMBERSHIP != SEMANTIC CONTAINMENT. PACKAGE MEMBERSHIP != AUTOMATIC LOAD. PACKAGE MEMBERSHIP != ONTOLOGICAL PARENTAGE. Directories, co-occurrence and cross-references create no dependency.

Existing ImageT manifest internal slot keys do not change in this milestone; they are not an alternative identity system for modules exposed later. Do not force a retrofit of all current controls through this contract.

## 4. Headers and runtime roles

A selectable Library module must have exactly one nonempty value for each field: Module ID, Package ID, Runtime role, Scope, Status, Version. Only explicitly declared core infrastructure may omit Package ID. Scope describes the task portion; Version is the bound revision, not priority. YAML Library catalogs use the equivalent module_id, package_id, runtime_role, scope, status and version keys for these same identity/header checks; full-read and body verification are unchanged.

Responsibility boundary is needed when overlap/interfaces could merge authority; it is required for refinements/procedures with material interfaces. Refines, Complements, Requires appear only for actual relations. Add no metadata without a corresponding runtime decision.

| Initial runtime role | Responsibility |
| --- | --- |
| CORE_ARCHITECTURE | Define the shared technical contract |
| PACKAGE_CATALOG | Root or package technical inventory; does not execute module behavior |
| DOMAIN_CONTROL | Execution discipline for a selected product/domain; concept-development core and Creative have this role |
| REASONING_PROFILE | Cross-subject mechanism reasoning, diagnosis and change verification; Technical |
| CAPABILITY | Techniques usable across domains; Brainstorm |
| DOMAIN_PROCEDURE | Scoped procedure within a package; does not independently call pipelines |
| PREFERENCE | Soft guidance under its owner's authority/activation contract |
| TOOL_PIPELINE | Entry into a mediation pipeline; AIS or ImageT |

DOMAIN_SPECIALIZATION is not yet needed as a separate role: REFINES expresses specialization. REASONING_PROFILE was established by inspecting TECHNICAL's body: it governs HOW reasoning proceeds, not WHAT subject the task belongs to. It connects mechanisms, retains competing hypotheses, chooses distinguishing tests and checks bounded changes across subjects; it owns no domain knowledge or Hub CI truth/state policy. BRAINSTORM remains a CAPABILITY for premise-expansion techniques, not part of this profile. NEW ROLE requires a concrete runtime distinction not representable by an existing role. Pipeline-internal roles remain pipeline-owned; this table does not redesign them.

TECHNICAL retains canonical Module ID HUB-DOM-TECHNICAL. DOM is part of the identifier, not a role assertion; inferring role from a prefix is forbidden. Retain the ID because no identity/resolution failure requires a rename, not because a directory or old candidate determines role. Package ID HUB-PKG-TECHNICAL remains technical ownership context. Trial 0.1-trial and real migration candidate 1.0-candidate share identity/role but differ in revision and permitted use; do not select newest or retain a trial as fallback. ARCHITECTURE IS NOT ONTOLOGY. CURRENT DIRECTORY != ROLE.

## 5. Technical composition relations

Only REFINES, COMPLEMENTS, REQUIRES. Add no parent/child/inherits/weight/rank/priority/supersedes.

REFINES declares a target Module ID and the matched responsibility/scope being refined. A target ID alone is insufficient when the responsibility portion is unclear. REFINES != REPLACES. REFINES != REQUIRES. The relation neither autoloads the target nor creates a hard dependency. Router must preserve base responsibilities that still apply outside the matched scope; if target reading is necessary to establish task coverage/boundaries, read it for that composition need, not through a general autoload rule.

SPECIALIZATION REFINES MATCHED SCOPE; IT DOES NOT ERASE UNCOVERED BASE RESPONSIBILITIES. MORE SPECIFIC != EXCLUSIVE. OVERLAP != REPLACEMENT.

COMPLEMENTS declares a target and scope where needed to express independent contributions to the same task portion. Neither module automatically wins or replaces the other. COMPLEMENTS != REQUIRES; relation alone does not autoload the counterpart.

REQUIRES is a hard technical dependency by Module ID; expand transitively only through explicitly declared and accepted edges. Missing dependencies or hard cycles block dependent work. A module that needs a target for correct execution must declare Requires separately, even if it declares Refines/Complements. Infer no edges from mentions, package membership or proposals in retrieved content.

ROUTING RELATION != ONTOLOGY. Load order is not authority priority. When modules give incompatible instructions for the same decision, consider complete scopes/boundaries and separate independent portions where possible; expose and block any remaining material conflict. Do not default to specificity winning or silently merge instructions.

## 6. Root package Catalog

ROOT CATALOG != GLOBAL LEAF-MODULE REGISTRY. Root registers only major package/interface entrypoints: Package ID, Entrypoint Module ID, role, status, version binding, short applicability, location/binding and local catalog if present. Declare cross-package Requires only when genuinely hard; do not copy all leaf relations into root.

The runtime Catalog has Module ID HUB-CORE-PACKAGE-CATALOG, role PACKAGE_CATALOG, status ACTIVE, version 1.1. Exactly four root entries: Technical, Concept Development, AIS and ImageT. Root knows the concept entrypoint and local-catalog interface, not its leaf inventory or trigger details. Internal concept leaves are declared only in the package-local catalog. AIS/ImageT LEGACY_EXISTING bindings preserve their current exact sources; this topology change does not modify pipeline behavior.

Root helps Hub select relevant packages and resolve entrypoints/local catalogs. It contains no module behavior bodies, leaf-selection algorithm or priority scores. Root-entry existence grants no activation; a Catalog does not itself verify headers, reads or runtime location.

LIBRARY_MODULE binding: Technical and Concept Development, root Central Hub Config and each selected artifact's exact catalog-bound Version; no Project Source fallback. Prefer verified internal object/revision identity when available; otherwise require the root-scoped object resolution defined in section 8 and Hub Router. Null internal IDs/locators do not alone prohibit that resolution, but dependent execution remains blocked until one identity path is verified. Update metadata only from actual observations, never filename equality. LEGACY_PROJECT_SOURCE binding: only unmigrated AIS/ImageT, exact declared_source_path/source_name in Project Sources, full reads and existing title/version/responsibility-boundary checks. Catalog Module IDs are routing aliases, not installed source headers. Missing or ambiguous sources block dependent work; no Library discovery. This is transitional compatibility, not a relaxation of the Library contract. Pipelines retain internal ownership. Migration must remove the legacy binding in the same deployment.

## 7. Local catalogs and package growth

Singleton packages use root entry -> direct entrypoint. Add a package-local catalog only when multiple independently selectable modules exist and the direct entrypoint is insufficient; do not create an empty catalog for the future.

A local catalog has its own Module ID, Package ID, PACKAGE_CATALOG role and status/version; entries contain Module ID, role, status, version, short applicability, a locator within Central Hub Config and scoped Refines/Complements/Requires. Catalogs are selection data; only an authorized entrypoint/procedure performs local selection within Hub's delegated scope. CATALOG ENTRY != MODULE CONTENT; CATALOG MATCH != MODULE READ; CATALOG MEMBERSHIP != ACTIVATION.

A package selects only its own modules. A cross-package edge must explicitly declare target Module ID plus Package ID for owner resolution, then return to Hub Router for scoped composition/dependency handling; do not scan other packages or invent edges. Use one Module ID namespace; Package ID does not replace target identity. A dependency not admitted by the catalog does not admit itself because a retrieved body demands it.

A local catalog does not override Hub CI, replace Hub Router, activate AIS/ImageT independently or grant semantic authority. Root retains only the local-catalog interface and necessary bindings; changing leaves does not require changing root or Router core. Pipelines retain their internal inventory/router and need not convert manifests into shared catalogs.

## 8. Resolution and read contract

CENTRAL HUB CONFIG = SOLE LIBRARY DISCOVERY ROOT.

Central Hub Config is the only Library root. The user provided ACTIVE TECHNICAL/1.0 evidence: library_file_id=libfile_bab7d55cd85c819198291acf135099fd, Library version_id=1; observed file_id=file_000000006da88211aa3412146f6c016c is surface evidence only. FULL_FILE 19/19, has_more=false; V01/V02 PASS, no fallback or identity ambiguity. USER_REPORTED, not reproduced by Codex. User-reported live integration: I01–I07/I09–I10 PASS; I08 UNVERIFIABLE. LIVE INTEGRATION PARTIAL: success paths verified, actual failure path unverified. Do not interpret PARTIAL as a functional integration failure. Library version_id=1 != artifact Version=1.0.

Two identity paths serve one LIBRARY_MODULE binding: verified direct internal identity when exposed and usable, or root-scoped Library object resolution when it is not. Both require FULL_FILE, exact Module ID / Package ID / Runtime role / Status ACTIVE / bound artifact Version and material body/responsibility verification. For root-scoped resolution, open the specific candidate and establish one acceptable ACTIVE identity through sufficient observable listing/search coverage inside Central Hub Config, completing relevant pagination/loading and inspecting all plausible matches, including differently named candidates. Incomplete coverage or unread plausible candidates remain UNRESOLVED; multiple valid matches block. Seeing one filename on one screen is insufficient. Report the scoped evidence and its limits; no mathematical whole-Library uniqueness claim is required. Direct-ID mismatch is not permission to switch paths and evade rejection. Direct-fetch capability remains UNVERIFIED; invent no API.

Integration flow: task portion -> Hub Router -> root package Catalog -> select relevant packages -> resolve entrypoint/local catalog -> select module set and hard Requires closure -> dispatch by binding. LIBRARY_MODULE: retrieve exact artifact in Central Hub Config -> FULL_FILE -> verify Module ID / Package ID / role / status / version and object identity. LEGACY_PROJECT_SOURCE: full-read the exact declared source and check its existing contract; require neither new headers nor Library lookup. Compose and apply within scope only after verification.

Read entrypoints/catalogs fully and verify identity/binding before using their content to select leaves. Metadata dependencies are only a read plan until every artifact passes FULL_FILE and comparison. Material header/body/Catalog discrepancies in bindings, dependencies or responsibility boundaries block dependent work; do not silently repair the Catalog or select a newer revision.

Library locators must be relative to Central Hub Config or explicitly bounded by Central Hub Config through verified actual identity. Do not use local/repository paths, absolute filesystem paths, another folder, lookalikes or newest-version guesses. If the tool cannot establish the exact root, stop discovery; do not search the whole Library to guess its folder. Do not substitute Project Sources, repository, Memory, prior chat or archives for a Library-bound module.

A missing file does not permit broader search. A null locator leaves identity unresolved until a valid Library identity path succeeds; it never authorizes repository_path or another storage source. Filename/display name helps discovery, not identity confirmation. Hidden internal IDs may remain null even after sufficient root-scoped verification. Never derive Library revision from artifact Version or "current version"; record a stable object URL only when stability/usefulness is demonstrated, not merely because a viewer URL exists. Snippets, hits, headers, summaries and metadata do not prove FULL_FILE. NAME MATCH != IDENTITY; SEARCH RESULT != MODULE READ; HEADER MATCH != ACTIVATION; PARTIAL READ != FULL_FILE; NOT FOUND != FALSE.

Only ACTIVE Library artifacts in accepted bindings become eligible after selection/read. Legacy sources use the explicitly declared compatibility branch. Core runtime requires the exact installed v1.1 stack and CI delegation. Self-declared headers grant no admission; do not activate other candidate packages or expand action authorization.

Do not traverse the whole Library/package. Read only the selected module set, declared hard closure and owner context materially required for composition. REFINES/COMPLEMENTS prompt relevant scope consideration, not recursive autoload. Stop at delegated sufficiency; valid broad scope may require a broad closure. This is no claim about ChatGPT backend complexity or performance.

## 9. Pipeline and state boundaries

HUB SELECTS PIPELINE. PIPELINE RESOLVES INTERNAL DEPENDENCIES. Root knows AIS/ImageT entrypoints, not an enumeration of Ready Gate, anti-prior, internal source modules, research stages/source policy or future deep-research gates.

Domain modules return scoped input/needs to Hub. Requires or package-local selection does not grant tool-call authorization or bypass pipeline gates. For a newly needed pipeline, Hub CI evaluates need/authorization and Hub Router selects the corresponding portion. RESEARCH EVIDENCE != DESIGN AUTHORIZATION. PIPELINE SELECTION != TOOL EXECUTION. PIPELINE OUTPUT != GLOBAL STATE UPDATE.

Do not create a shared AIS/ImageT Ready Gate merely because both use gates. ImageT retains its one-call approval snapshot and visible verification; AIS retains its research lock/source/evidence/coverage and its own protocol when designed later.

Router reassesses each turn/scope change; retain context/read evidence only while sufficient, not persistent modes. PREVIOUS ACTIVATION != CURRENT ACTIVATION. Packages/modules do not activate each other. Material scope changes require affected reselection/rebuilding and rereads if context/read evidence is no longer sufficient; pipelines handle internal refresh under their own contracts.

## 10. Failure behavior

| Situation | Required result |
| --- | --- |
| Root Catalog missing/unreadable | Block catalog-dependent selection; no arbitrary control discovery. Continue sufficient independent baseline work |
| Package entry missing | Do not infer a package from filename; report unresolved package |
| Required package-local catalog missing | Block dependent selection; do not load the whole package instead |
| Selected Library module missing | Block dependent work; do not broaden beyond Central Hub Config |
| Library unavailable or neither identity path can resolve one object | Retain UNRESOLVED / NOT VERIFIED; fabricate no read or repository substitute |
| Module ID mismatch or duplicate/ambiguous identity | Reject mismatched artifact/ambiguous selection; do not select by search rank |
| Package ID mismatch | Do not apply a module under the wrong owner; block dependent work |
| Wrong runtime role | Do not use the body as the expected role |
| Wrong version binding | Do not choose newest; report binding mismatch |
| Candidate/inactive selected accidentally | Do not auto-activate; only test separately within authorized scope |
| Hard Requires dependency missing | Block module and dependent work; continue independent portions |
| Requires cycle | Block the affected closure; no infinite retrieval loop |
| Partial specialization overlap | Keep uncovered base responsibilities; refine only matched scope |
| Applicable module conflict | Consider boundaries/separation; expose unresolved material conflict |
| Scope materially changes | Reselect and refresh affected portions before continuing |
| Lookalike filename but wrong ID | Not the requested module; no fallback |
| Only snippet/header retrieved | Not FULL_FILE; do not execute the module |
| Large Library, small selected closure | Do not traverse unrelated content or claim package/global completeness |

Block only dependent work where possible; continue independent baseline work Hub CI can sufficiently perform. Do not relabel a missing decisive dependency as a secondary gap to bypass it. The failure contract applies with the correct v1.1 installation; I08 actual Library failure remains UNVERIFIABLE. Do not modify repository Router v1.0.

## 11. Integration milestone limits

The concept migration uses the existing growing-package/local-catalog mechanism for two independently selectable leaves. It adds no role, registry, resolver, graph/state engine or routing algorithm. Keep other packages/pipelines unchanged and preserve selected-closure loading and ownership boundaries.

## 12. Migration and required evidence

This runtime stack is ACTIVE in the repository, not automatic proof of Project deployment. At migration-commit time, Library installation and exact FULL_FILE/identity verification for the concept entrypoint/catalog and Creative/Brainstorm 1.1 were NOT_PERFORMED / NOT_VERIFIED. The later ChatGPT-observed/user-provided smoke inspection verifies that the four exact objects are present in Central Hub Config and that their FULL_FILE identity/content and repository byte matches pass. `library_version_id` and durable `locator` remain unknown; artifact Version must not be treated as a Library revision. On 2026-10-27, the user confirmed PASS for one integrated Central Hub runtime smoke across the exact Hub/AIS/TECHNICAL/Concept/Brainstorm/Creative revisions recorded in RUNTIME_EVIDENCE_CHANGELOG.md. Hub runtime retrieval traces remain NOT_VERIFIED; all C01-C12 live cases remain NOT_RUN; the scoped PASS is not a global Central Hub PASS. Prior Technical evidence remains user-reported and prior Brainstorm 1.0 UI evidence remains old-revision-only. CONCEPT_DEVELOPMENT_MIGRATION.md records provenance, retirement, the safe manual switch/rollback sequence, current post-smoke evidence and C01-C12 smoke/spec cases. Historical migration/result records remain historical; do not install them as controls or use them as runtime fallbacks.

Preserve Hub/AIS/ImageT regressions: baseline NONE, no self-activation, research does not become acceptance, required one-call Ready Gate and no silent retry. Rollback must explicitly restore a compatible previous CI/Router/source stack; Library failure does not trigger automatic rollback. ROLLBACK != FALLBACK.
