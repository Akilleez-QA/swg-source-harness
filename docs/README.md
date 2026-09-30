# Building and contributing to SWG Source

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Community guide drafts · September 28, 2026. Start small, learn from a working example, and leave the next person enough information to reproduce your result. Beginners, testers, writers, artists and programmers can all contribute.

These guides combine public project sources, archived troubleshooting and POODO-inspired evidence habits. Linked official rules remain authoritative; proposed standards here have not been adopted by SWG Source. This independent package now includes a Python 3 standard-library CLI for local static preflight. Remote admission, signing and provider adapters remain designs.

## Start here

| What you want to do | Guide |
|---|---|
| Find the project, choose a setup or make a first contribution | [Getting started](getting-started.md) |
| Understand the stock server source and processes | [Stock server](stock-server.md) |
| Understand the stock client build and runtime | [Stock client](stock-client.md) |
| Trace a change across repositories | [Change routing](change-routing.md) |
| Review architecture, intent and preserved behavior | [Architecture and intent review](architecture-and-intent-review.md) |
| Separate reference, working, generated and evidence files locally | [Example workspace layout](example-workspace-layout.md) |
| Build, change content or investigate a failure | [Building and debugging](building-and-debugging.md) |
| Pick up useful habits | [Tips and tricks](tips-and-tricks.md) |
| Ask for help, choose a channel or help another contributor | [Community and support](community-and-support.md) |
| Prepare and follow through on a contribution | [Contributing](contributing.md) |
| Use AI while keeping ownership of the result | [AI-assisted work and POODO lessons](ai-assisted-work.md) |
| Write usable documentation and PR notes | [Documentation and PR standard](documentation-and-pr-standard.md) |
| Know which checks and evidence a change needs | [Testing and validation](testing-and-validation.md) |
| Understand the proposed required review filter | [Harness intake and attestation](harness-intake-and-attestation.md) |
| Run local preflight and understand integration limits | [Harness setup and integration plan](harness-setup-and-integrations.md) |

## The proposed contribution path

Choose a small task → identify the right repository and runtime → define the expected result → make the change → run the applicable checks → submit concise evidence → pass harness intake → human review → address feedback and rerun affected checks.

The proposed mandatory filter applies to human-written and AI-assisted submissions alike. Passing means eligible for review; it does not promise acceptance. Questions and design discussions remain welcome before anyone has a passing submission.

## Finding current information

Use the [project website](https://www.swgsource.org/), [GitHub organization](https://github.com/SWG-Source), [wiki](https://github.com/SWG-Source/swg-main/wiki) and [Discord rules and information](https://discord.com/channels/366560008068005892/818213460612612146). Read later corrections and check the branch/version before applying an archive answer. The Discord server-forum is for server promotion/recruitment; it is not a separate canonical setup manual. Legacy website/forum material linked in the wiki can be historical or describe another project.

## Editorial and implementation boundaries

No installation or gameplay validation was performed for these guides. Some archive outcomes are user reports and are labeled accordingly. No reliable model ranking follows from these anecdotes. No project policy, required GitHub check, signing authority or deployment was changed.

Before publication, maintainers should review project-policy summaries, choose supported setup versions and agree on intake profiles/exception handling. Before enforcement, an implementation must demonstrate the end-to-end gate and measure reviewer burden in a pilot.

Research companions: [repository map](research/repository-map.md), [setup map](research/setup-map.md), [operations cases](research/archive-operations-cases.md), [repository archive cases](research/repository-archive-cases.md). Raw archive exports and private configuration should not be bundled with a public guide release.
