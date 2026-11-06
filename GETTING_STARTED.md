# Getting started with Central Hub

Central Hub coordinates specialized capabilities in a ChatGPT Project. Hub CI governs the conversation, including what actions are authorized and what claims are supported. The Router selects packages for the parts of the current request that need them. Architecture defines how the pieces fit together, and the Package Catalog identifies each package and where its entrypoint must be read. AIS and ImageT manage their own tool procedures. For everyday chat, writing, or a simple explanation, the Hub can respond using its baseline without selecting a package.

## What you need

- ChatGPT on the web with a Project that supports Project Instructions and Project Sources.
- A Library surface where you can place the required modules in `Central Hub Config`. The Project's runtime must also be able to resolve and fully read the exact Library objects in that root. This access depends on the capabilities your account exposes. The repository does not establish a universal folder-creation, direct-ID lookup, or full-file retrieval workflow.
- Search and source-reading tools for live AIS research. Image analysis or generation capability for the ImageT operation you request.

The files in this repository are sufficient for the installation map below. A separate Creative Workshops checkout is unnecessary. For general product navigation, see [ChatGPT on the web](https://learn.chatgpt.com/docs/web).

## 1. Create a Project and add the core files

Use **Hub CI 1.1 and Router 1.1 with Architecture 1.10 and Root Package Catalog 1.10** as one compatible set. All paths below are relative to this repository's root.

1. Create a new Project in ChatGPT on the web.
2. Open **Project Instructions** and paste the full text of [HUB_CI_v1.1.md](HUB_CI_v1.1.md). This is the only file whose contents go in Project Instructions.
3. Add the following three files to **Project Sources**. Keep their exact filenames.
4. For live research or image work, add the corresponding Project Sources from the [pipeline section](#3-add-the-tool-pipelines).
5. Set up the [Library modules](#2-place-the-library-modules) and check that the Project can resolve them. Then open a new chat inside the Project and try the [sanity checks](#quick-sanity-checks).

| Project Sources | Purpose |
| --- | --- |
| [HUB_ROUTER_v1.1.yaml](HUB_ROUTER_v1.1.yaml) | Selects packages and checks reads and dependencies. |
| [HUB_ARCHITECTURE_v1.10.md](HUB_ARCHITECTURE_v1.10.md) | Defines the shared topology and how sources are resolved. |
| [HUB_PACKAGE_CATALOG_v1.10.yaml](HUB_PACKAGE_CATALOG_v1.10.yaml) | Lists the six root packages and their bindings. |

If you are replacing an earlier setup, remove earlier competing core sources from the Project. The Router is pinned to the exact 1.10 Architecture and Catalog.

## 2. Place the Library modules

Use **ChatGPT Library → `Central Hub Config`**, the only discovery root for these bindings. If your Library surface supports creating or selecting that root and saving files there, place the files below in that root. Keep the content and filenames intact. The package names in the table explain how the files are used. They do not require separate Library subfolders.

| Package | Role | File to place in `Central Hub Config` |
| --- | --- | --- |
| Technical | Entrypoint, reasoning profile 1.0 | [HUB-DOM-TECHNICAL_v1.0.md](candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md) |
| Concept Development | Core entrypoint 1.1 | [HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md](library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md) |
| Concept Development | Local Catalog 1.1 | [HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml](library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml) |
| Concept Development | Creative leaf 1.1 | [HUB-DOM-CREATIVE_v1.1.md](library_modules/HUB-DOM-CREATIVE_v1.1.md) |
| Concept Development | Brainstorm leaf 1.1 | [HUB-CAP-BRAINSTORM_v1.1.md](library_modules/HUB-CAP-BRAINSTORM_v1.1.md) |
| Concept Development | Debate leaf 1.0 | [HUB-CAP-DEBATE_v1.0.md](library_modules/HUB-CAP-DEBATE_v1.0.md) |
| Authoring | Single entrypoint 0.7 | [HUB-CAP-AUTHORING_v0.7.md](library_modules/HUB-CAP-AUTHORING_v0.7.md) |
| Shopping | Core entrypoint 1.0 | [HUB-DOM-SHOPPING_v1.0.md](library_modules/HUB-DOM-SHOPPING_v1.0.md) |
| Shopping | Local Catalog 1.0 | [HUB-CATALOG-SHOPPING_v1.0.yaml](library_modules/HUB-CATALOG-SHOPPING_v1.0.yaml) |
| Shopping | Search procedure 1.0 | [HUB-PROC-SHOPPING-SEARCH_v1.0.md](library_modules/HUB-PROC-SHOPPING-SEARCH_v1.0.md) |

Technical's listed file declares `ACTIVE` and Version `1.0` despite its directory name. Use that exact artifact. The default Library setup excludes archived and candidate versions, tests, and Concept's inactive experimental anti-drift entries. Keep the two local catalogs with their Library packages. The Root Package Catalog stays in Project Sources.

Before relying on a Library package, check that its required objects can be resolved and read in full from the Project. Use verified internal object and revision identity when exposed and usable. Otherwise, check within `Central Hub Config` with sufficient listing or search coverage, including plausible matches with different filenames. Open each specific object and verify the complete contents (`FULL_FILE`), exact Module ID, Package ID, runtime role, `ACTIVE` status, artifact version, and material body. Resolve duplicates or ambiguity before using the package. A filename, search hit, or partial read is insufficient. An object ID recorded from an earlier installation may be unavailable in yours.

If you cannot create or access the required root, or the Project cannot demonstrate an exact full read, treat the affected Library binding as unresolved. Report what you could observe and continue only with independent work that has sufficient sources. The contract provides no fallback through Project Sources, chat attachments, or repository files.

## 3. Add the tool pipelines

Hub Router selects a pipeline's entrypoint for the relevant task portion. The pipeline resolves its own controls and mediates tool use. Add the required files to **Project Sources**, preserving the exact filenames. Each pipeline requires the appropriate tool capability before it can execute an operation.

| Pipeline | Entrypoint | Required internal Project Sources |
| --- | --- | --- |
| AIS | [AIS_PIPELINE_v1.1.md](tool_pipelines/AIS/AIS_PIPELINE_v1.1.md) | [AIS_ROUTER_v1.2.yaml](tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml) |
| ImageT | [IMAGE_CONTROLLER_v1.2.md](tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2.md) | [IMAGE_SOURCE_ROUTER.yaml](tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml), [manifest.yaml](tool_pipelines/ImageT/manifest.yaml), [IMAGE_ANTI_PRIOR.md](tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md), [config.md](tool_pipelines/ImageT/config.md), [READY_GATE_v1.0.md](tool_pipelines/ImageT/READY_GATE_v1.0.md) |

**AIS** handles scoped verification, research, and discovery. It checks its search scope, available tools, source authority, and evidence coverage, then returns supported findings and gaps to the Hub. Its output does not itself change the Hub's task, decisions, or protected state.

**ImageT** distinguishes three steps for generation work:

1. **Open Gate** establishes whether the current input may be transformed as raw material or must be preserved as an authored prompt. To preserve a supplied prompt's semantics, state that explicitly in your current request for image execution.
2. **Prompt Gate** checks the tool-facing prompt against the operation, authorized constraints, and reference roles.
3. **Ready Gate** presents a numbered snapshot for approval. Approve the exact current snapshot before the generation call. Approval covers one call. Changes or a retry require a fresh approval. Analysis alone does not generate an image and bypasses Ready Gate.

Leave the humanoid preference out of the default setup. The manifest lists it as inactive and available only for direct-input experiments. The visual template is declared optional and absent. Creating a prompt or showing a pending snapshot establishes neither tool execution nor an image result.

## Quick sanity checks

Start with a fresh chat inside the configured Project. Try the first row, then one path you installed. Each row is a separate request. Type command examples as plain user instructions.

| Path | Try this | What to look for |
| --- | --- | --- |
| Baseline | `Write a one-sentence thank-you note for a neighbor.` | A usable answer can come from the baseline without a package. |
| Technical | `My laptop slows down after 20 minutes under load. Give two plausible causes and one test that distinguishes them.` | Technical may contribute mechanism reasoning and a distinguishing test. |
| Concept Development | `/BRAINSTORM Give two ways to remove a bookstore's dependence on book sales, and trace one consequence of each. #` | The core and local Catalog resolve the Brainstorm leaf for this span if the binding is verified. |
| Authoring | First line `/AUTHOR CODEX`. Next line `Draft a prompt to investigate a slow file import.` | A prompt is returned for handoff. Codex is not invoked by Authoring. |
| AIS | `Search the web to verify Python 3.14's release date using official Python sources. Cite the relevant source.` | If search and retrieval are available, look for sources actually read and evidence that supports the date. |
| ImageT | `Generate an image of one blue square on white. Show me the snapshot and wait for my approval before calling the tool.` | With required sources available, look for the numbered pending snapshot before any generation call. |
| Shopping | `Offer A is 500 g for $8 and Offer B is 750 g for $11. Compare unit prices and keep stock status unknown.` | A bounded comparison can use the supplied offers without requiring AIS. |

**EXPECTED ROUTING != PROOF OF FULL LIVE VERIFICATION.** A plausible answer alone does not establish a Library read, package execution, search, or image call. Check available read and tool evidence. If a decisive dependency is unavailable, expect a specific blocker for the affected part. The repository records earlier evidence by revision. It does not establish a fresh 1.10 deployment for your account. See the [runtime evidence changelog](RUNTIME_EVIDENCE_CHANGELOG.md).

## Everyday use

Ask normally. The Hub evaluates the current task and selects specialization only when materially needed. You do not need to call the Router manually. A technical topic alone does not require Technical, and an ordinary request for ideas can use baseline or the Concept core. For specialized Concept leaves, put an exact opener and a standalone closing `#` around nonempty user instructions: `/CREATIVE <content> #`, `/BRAINSTORM <content> #`, or `/DEBATE <content> #`. Type these as directives in the current message. A quoted example or an earlier invocation does not activate a leaf. See the [Concept core](library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md).

### Authoring commands

Put the command on the first nonempty line you write, outside quotes or code fences, using exact case, one ASCII space between tokens, and no surrounding whitespace or extra text. Put the task on the following lines. The five base commands are:

```text
/AUTHOR AIS
/AUTHOR IMAGET
/AUTHOR CODEX
/AUTHOR WORK
/AUTHOR GENERIC
```

| Additional form | Example |
| --- | --- |
| `/AUTHOR <OUTPUT_TARGET> + <CONTRIBUTOR>` | `/AUTHOR GENERIC + BRAINSTORM` |
| `/AUTHOR <OUTPUT_TARGET> P<n>` | `/AUTHOR CODEX P2` |
| `/AUTHOR <OUTPUT_TARGET> ISOLATED` | `/AUTHOR CODEX ISOLATED` |
| `/AUTHOR <OUTPUT_TARGET> P<n> ISOLATED` | `/AUTHOR CODEX P2 ISOLATED` |

Presets are `P1`, `P2`, or `P3`. `ISOLATED` goes last and limits the source material admitted for this turn. Contributors are `CREATIVE` or `BRAINSTORM`. Use a corresponding valid Concept span in the request body when asking that leaf to contribute. The contributor name alone does not activate it. Contributor forms cannot include a preset or `ISOLATED`. Repeat the command on a new Authoring turn, including when replying to a clarification. Authoring returns a prompt or asks a necessary clarification. Target execution requires a separate request and its own permissions. See [Authoring 0.7](library_modules/HUB-CAP-AUTHORING_v0.7.md).

## How packages work together

Bring your current task to the Hub. The Router can choose zero, one, or several packages, including different packages for different parts of a request. Each package contributes within its own scope. The next turn can use a different combination, or invoke the same capability again if the new request calls for it.

| Request | One possible composition |
| --- | --- |
| Write a brief thank-you note. | Hub baseline alone. |
| Diagnose a slowdown from symptoms and logs already supplied. | Technical compares mechanisms and proposes a distinguishing test. |
| Verify a documented hardware limit, then assess whether it explains the slowdown. | AIS checks the external evidence. The Hub can use the supported findings in the scoped Technical analysis. |
| Review an idea for consistency, or explore alternate premises. | Concept core can handle a review alone. A valid `/BRAINSTORM … #` span can add premise exploration. A `/CREATIVE … #` span can develop a chosen premise separately. |
| Create or edit an image from a clear request. | ImageT can handle it directly, with the applicable gates before a generation call. |
| Turn an existing diagnosis into a task for Codex. | `/AUTHOR CODEX` produces the requested handoff prompt and stops. |

AIS returns supported evidence and gaps to the Hub. The Hub may use that evidence in a direct answer, Technical analysis, Concept development, an Authoring handoff, or an ImageT task that needs factual constraints. An evidence source is not automatically an image reference asset. Creative and Brainstorm have independent scopes. Neither needs to run merely because the other was selected. A declared refinement or complementary relation describes how scoped contributions relate. Refinement and complementarity alone add no hard dependency. Required reads follow the applicable contract and any declared hard dependencies. See [Architecture](HUB_ARCHITECTURE_v1.10.md).

## Full walkthrough example — not required order

This optional walkthrough illustrates how to turn research into an image of a historical spacecraft. Use a Project with the core files, the applicable Library modules, both pipeline file sets, and working tools. Send each quoted prompt as a separate turn in the same Project chat. Continue dependent steps only when the previous step supplied the evidence or material they need.

1. **Check the baseline.** Ask “Write a one-sentence thank-you note for a neighbor.” No specialized package is needed for this example.
2. **Ask for research.** Try “Search official NASA sources for the visible landing-gear features of the Apollo 11 Lunar Module. Cite the sources you actually read and flag any details they do not establish.” Use supported findings as constraints. Keep unresolved details open.
3. **Develop one visual premise.** Try `/CREATIVE Develop a single museum illustration concept from the supported findings above. Keep the verified landing-gear features, and keep unsupported details open. #`. If you instead want to explore different premises, use a valid Brainstorm span in a separate request and choose which premise to carry forward.
4. **Prepare a handoff prompt.** Use `/AUTHOR IMAGET` on the first line. On the next line ask for a self-contained image prompt from the chosen concept and supported findings. Review the returned prompt. This turn ends at the prompt.
5. **Request the image.** Supply the prompt and say “Generate the image from this final authored prompt. Preserve its semantic content. Show me the snapshot and wait for my approval before calling the tool.” Your current instruction supplies the preservation authority for Open Gate. ImageT resolves its sources, checks the tool-facing prompt at Prompt Gate, and presents the numbered Ready Gate snapshot. Check the prompt, references and roles, and options. Research citations alone do not authorize reference assets.
6. **Approve and inspect.** If the snapshot matches the intended operation, explicitly approve that exact version for one call. If a field needs revision, ask for the change and review the new snapshot. After a successful tool call, inspect the visible result against the verified constraints. You can then ask to analyze the result or explore a variation as a new task.

### You can skip or reorder most of this

A request with sufficient evidence can skip AIS. A clear image request can go straight to ImageT, or use research evidence without developing a separate Concept or Authoring artifact. Concept can inform an image request directly or supply material for an Authoring handoff. Technical can precede a Codex handoff, and AIS findings can support Technical before Concept if the task actually needs all three. Authoring alone and the Hub baseline alone are also useful.

Only real dependencies and applicable contracts constrain local order. For example, ImageT generation requires Prompt Gate before Ready Gate and approval before the image tool call. That sequence belongs to ImageT. The Hub reassesses which packages to use for each task or turn.

## Add or request a capability

- **Build your own.** Fork or clone the repository and extend a module, package, or pipeline under the existing [architecture](HUB_ARCHITECTURE_v1.10.md). Keep the new responsibility with its appropriate owner.
- **Request a change.** [Open an issue](https://github.com/lead21pc/ChatGPT-Features-Hub/issues/new) describing the capability, the current problem, and what you expect to happen. Name a relevant package or module if you know it. You can propose the behavior without designing the implementation. The maintainer can extend an existing package, add a module or pipeline, or decline the proposal.

## Common setup mistakes

| What you see | What to check |
| --- | --- |
| A correct CI is installed, but specialization is blocked. | Confirm Router 1.1 and both 1.10 sources are present and readable in Project Sources. A package body alone cannot replace the Root Catalog. |
| Library retrieval is missing or ambiguous. | Check the exact root, file identity, version, active status, full read, and duplicate coverage. Install the listed files rather than uploading the entire module tree. |
| Every task is expected to use all installed packages. | Select only the contributions needed for the current task. AIS contributes when external evidence is needed, and ImageT can handle a clear image request directly. |
| A file's location or a previous selection is treated as a dependency. | Check the current scope and declared dependencies. Files in the same folder have no implied execution order. |
| An authored prompt, an AIS finding, or an ImageT snapshot is treated as an action or decision. | Look for separate authorization and evidence of execution or an accepted decision. A prompt is a handoff, evidence is scoped, and an image requires an actual tool result. |

## Optional Local/API backup

The Python implementation is a reference and backup. ChatGPT Web setup uses the files above and does not require Local/API. If you want to extend the backup, you can fork the repository. See the [Local/API README](legacy/README.md) for its setup and [verification records](legacy/VERIFICATION.md) for tested scope.
