# ChatGPT Features Hub

**A general-purpose ChatGPT workspace for technical diagnosis, concept development, prompt authoring, research, image workflows, and shopping decisions.**

**[Get started with ChatGPT Web](GETTING_STARTED.md)** for the exact Project Instructions, Project Sources, and Library files.

[How the Hub handles tasks](#how-the-hub-handles-tasks) · [Current packages](#current-packages) · [Prompt authoring](#prompt-authoring-with-authoring) · [Where to start](#where-to-start) · [Verification status](#verification-status)

## What the Hub is for

Central Hub is a personal project developed through practical use. Observed model behavior failures inform changes to Custom Instructions, regression checks, and tests of individual revisions. **ChatGPT Web / Project + Library** is the primary environment. The [Hub overview](HUB_OVERVIEW.md) links to the current contracts.

## How the Hub handles tasks

The Hub keeps the objective of the current request in view and assigns each part of the task to an appropriate package. A routine explanation or conversation may only need Hub CI. When several packages contribute, each works within its assigned scope and the Hub brings the results together.

```text
Current request
  ↓
Hub CI · operation, state, and authorization to act
  ↓
Router + Catalog · scope, package selection, and source verification
  ↓
Selected packages · internal modules or pipelines for the assigned scope
  ↓
The Hub combines the results
```

[Hub CI 1.1](<HUB_CI_v1.1.md>) provides the Project's Custom Instructions. [Router 1.1](<HUB_ROUTER_v1.1.yaml>) uses [Architecture 1.10](<HUB_ARCHITECTURE_v1.10.md>) and [Package Catalog 1.10](<HUB_PACKAGE_CATALOG_v1.10.yaml>) to identify packages, check bindings, and assign work by scope. Each package resolves its internal modules through its own catalog. ChatGPT retrieves sources and calls tools when the applicable conditions are met.

## Current packages

| Package | Role in a request |
| --- | --- |
| **Technical** | Explains mechanisms, distinguishes between hypotheses, and designs tests to identify a cause or verify a technical change. |
| [**Concept Development**](<library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md>) | Develops and examines ideas. Creative elaborates within a premise, Brainstorm develops alternatives, and Debate challenges proposals. |
| [**Authoring**](<library_modules/HUB-CAP-AUTHORING_v0.7.md>) | Turns a request into a self-contained prompt for the selected target. |
| [**AIS**](<tool_pipelines/AIS/AIS_PIPELINE_v1.1.md>) | Finds, reads, and evaluates external evidence for the parts of a Hub task that require research. |
| [**ImageT**](<tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2.md>) | Analyzes images and prepares or performs image operations according to the pipeline's authorization and verification requirements. |
| [**Shopping**](<library_modules/HUB-DOM-SHOPPING_v1.0.md>) | Compares purchase options against requirements, SKUs, offers, prices, and evidence coverage. The Hub selects AIS separately when external research is needed. |

## Prompt authoring with Authoring

Use `/AUTHOR` with the desired target, then describe the request in ordinary language. Authoring produces the prompt and stops there.

```text
/AUTHOR CODEX
Write a prompt for Codex to diagnose why the app slows down when opening large files.
Require measurements before proposing changes.
```

Add `ISOLATED` to limit which sources can supply content for the current authoring turn. The [Authoring 0.7 contract](<library_modules/HUB-CAP-AUTHORING_v0.7.md>) specifies the available targets, presets, and activation conditions.

## Where to start

| If you want to | Start here |
| --- | --- |
| Read or evaluate the ChatGPT Project + Library setup | [Central Hub overview](HUB_OVERVIEW.md) |
| Understand package selection and retrieval requirements | [Architecture](<HUB_ARCHITECTURE_v1.10.md>) and [Package Catalog](<HUB_PACKAGE_CATALOG_v1.10.yaml>) |
| Review promotions and results by revision | [Runtime evidence log](<RUNTIME_EVIDENCE_CHANGELOG.md>) and [Hub tests](<tests/>) |
| Try the Python/Responses API backup | [Local/API guide](legacy/README.md) |
| Find the 1.9 snapshot or M2/M3 evidence | [Local/API test records](legacy/README.md) and [VERIFICATION.md](legacy/VERIFICATION.md) |

## Verification status

The current source uses CI/Router 1.1 and Architecture/Catalog 1.10. It was split out from the Central Hub directory of ChatGPT Creative Workshops at commit `e310b451`. Static and mock Local/API checks have been run against 1.10. Earlier live Responses API results apply to the recorded workloads and revisions. Library installation, Project deployment, and live Shopping routing are tracked separately in the [Shopping 1.0 record](<SHOPPING_PROMOTION.md>).

<details>
<summary>Local/API backup</summary>

The Python entry points, runtime bindings, and Streamlit configuration are in `legacy/`. The runtime reads the current controls from the repository root. Streamlit listens on `127.0.0.1` by default. MCP provides read-only inspection over stdio. Shopping and ImageT currently have no local bindings.

From `legacy/`, run `python -X utf8 -B -m unittest discover -s tests` to test Local/API. The 1.9 snapshot, logs, and M2/M3 evidence are in [legacy/](legacy/).

</details>
