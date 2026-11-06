# ChatGPT Features Hub

**A general-purpose ChatGPT workspace for technical diagnosis, concept development, prompt authoring, research, image workflows, and shopping decisions.**

**[Get started with ChatGPT Web](GETTING_STARTED.md)** for the exact Project Instructions, Project Sources, and Library files.

[Quick setup](#quick-setup) · [How the Hub handles tasks](#how-the-hub-handles-tasks) · [Current packages](#current-packages) · [Prompt authoring](#prompt-authoring-with-authoring) · [Extend the Hub](#extend-the-hub)

## What the Hub is for

Central Hub is a personal project developed through practical use. Observed model behavior failures inform changes to Custom Instructions, regression checks, and tests of individual revisions. **ChatGPT Web / Project + Library** is the primary environment. The [Hub overview](HUB_OVERVIEW.md) links to the current contracts.

## Quick setup

Create a Project in **ChatGPT Web** and use the following placement map. Keep CI/Router 1.1 together with Architecture/Catalog 1.10.

| Where | What to put there |
| --- | --- |
| **Project Instructions** | Paste the full contents of [HUB_CI_v1.1.md](HUB_CI_v1.1.md). |
| **Project Sources** | Add [HUB_ROUTER_v1.1.yaml](HUB_ROUTER_v1.1.yaml), [HUB_ARCHITECTURE_v1.10.md](HUB_ARCHITECTURE_v1.10.md), and [HUB_PACKAGE_CATALOG_v1.10.yaml](HUB_PACKAGE_CATALOG_v1.10.yaml). For research or image work, add the [AIS or ImageT files](GETTING_STARTED.md#3-add-the-tool-pipelines) there too. |
| **Library → `Central Hub Config`** | Place the [10 listed files](GETTING_STARTED.md#2-place-the-library-modules) for Technical, Concept Development, Authoring, and Shopping in this root. The guide lists the exact entrypoints, local catalogs, and leaves. |

Open a new chat inside the Project and ask something simple, such as “Write a one-sentence thank-you note for a neighbor.” For specialized work, [check exact Library access](GETTING_STARTED.md#2-place-the-library-modules) and try the [short sanity checks](GETTING_STARTED.md#quick-sanity-checks). The setup uses this repository's files. Local/API and a separate Creative Workshops checkout are optional.

## How the Hub handles tasks

Start with your task. The Router selects zero, one, or several packages for the parts that need them. A simple answer can use Hub CI alone. A diagnosis can use Technical on its own, or combine Technical with AIS if the diagnosis needs current sources. A clear image request can go directly to ImageT.

The Hub brings scoped contributions together and reassesses the selection on each turn. The order follows real dependencies in the task or within a selected pipeline. See the [research-to-image walkthrough](GETTING_STARTED.md#full-walkthrough-example--not-required-order) for one possible combination and the steps you can skip.

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
| Set up ChatGPT Project + Library | [Getting Started](GETTING_STARTED.md) |
| Review the current contracts and status | [Central Hub overview](HUB_OVERVIEW.md) |
| Understand package selection and retrieval requirements | [Architecture](<HUB_ARCHITECTURE_v1.10.md>) and [Package Catalog](<HUB_PACKAGE_CATALOG_v1.10.yaml>) |
| Review promotions and results by revision | [Runtime evidence log](<RUNTIME_EVIDENCE_CHANGELOG.md>) and [Hub tests](<tests/>) |
| Try the Python/Responses API backup | [Local/API guide](legacy/README.md) |
| Find the 1.9 snapshot or M2/M3 evidence | [Local/API test records](legacy/README.md) and [VERIFICATION.md](legacy/VERIFICATION.md) |

## Extend the Hub

Fork or clone the repository to develop a capability using the existing [architecture](HUB_ARCHITECTURE_v1.10.md). To propose one upstream, [open an issue](https://github.com/lead21pc/ChatGPT-Features-Hub/issues/new) with the problem and expected behavior. See [how to propose a capability](GETTING_STARTED.md#add-or-request-a-capability).

## Verification status

The current source uses CI/Router 1.1 and Architecture/Catalog 1.10. It was split out from the Central Hub directory of ChatGPT Creative Workshops at commit `e310b451`. Static and mock Local/API checks have been run against 1.10. Earlier live Responses API results apply to the recorded workloads and revisions. Library installation, Project deployment, and live Shopping routing are tracked separately in the [Shopping 1.0 record](<SHOPPING_PROMOTION.md>).

<details>
<summary>Local/API backup</summary>

The Python entry points, runtime bindings, and Streamlit configuration are in `legacy/`. The runtime reads the current controls from the repository root. Streamlit listens on `127.0.0.1` by default. MCP provides read-only inspection over stdio. Shopping and ImageT currently have no local bindings.

From `legacy/`, run `python -X utf8 -B -m unittest discover -s tests` to test Local/API. The 1.9 snapshot, logs, and M2/M3 evidence are in [legacy/](legacy/).

</details>
