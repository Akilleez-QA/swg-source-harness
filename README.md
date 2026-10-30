# SWG Source Contribution Harness

The canonical home of a community contribution harness for SWG Source: practical guides, shared agent instructions, review templates and a provider-neutral local preflight tool.

**v0.2.0 is a usable starter harness, not a deployed project admission service.** It prepares evidence for review. It does not execute your tests, sign reports or grant review approval. This repository is maintained independently; SWG Source has not adopted or endorsed its proposed mandatory gate.

## Quick start

Requires Python 3.9+ and Git. The core CLI needs no Python packages, model subscription or API key. Optional POODO validation tools use PyYAML. Clone this repository or extract a release, then run commands from its directory. On Windows, use `py -3` instead of `python3` if appropriate.

```sh
python3 harness.py --help
python3 harness.py inspect --workspace /path/to/your/repository
python3 harness.py init --workspace /path/to/your/repository --output /path/outside/repository/task.json
```

Initialize before making changes: the template records the current commit as your base. Alternatively set `base` to the full commit ID you are proposing changes against. Work in your own branch. Fill in the task's objective, environment, expected behavior and separate AI disclosures. Perform the relevant checks, then record their actual results, the tested full commit ID, and the absolute local evidence-file path plus SHA-256. Commit your contribution before final preflight.

```sh
python3 harness.py check --workspace /path/to/your/repository --task /path/outside/repository/task.json --output /path/outside/repository/report.json
python3 harness.py verify --workspace /path/to/your/repository --report /path/outside/repository/report.json
```

Paths above are placeholders. Task/report outputs must be outside the inspected repository, and existing output files are never overwritten. Use a new report filename for each run. `check` returns 0 for structurally complete local evidence, 1 for missing/failed reported checks, and 2 for input/inspection errors. `verify` returns 1 for an incomplete report, 2 for invalid/stale input, and 0 only for a matching complete local report. It checks the report checksum and whether the clean Git candidate still matches; it does not authenticate the author or rerun evidence checks.

Inspect only a workspace you trust, on a stable checkout without concurrent edits. Git can invoke locally configured filters; this CLI is not a sandbox for hostile repositories. Index assume-unchanged/skip-worktree flags (including sparse checkouts) block clean inspection; use a full checkout without those flags. Nested initialized submodules are checked recursively. Git cleanliness does not identify ignored configs, deployed binaries or runtime data; record those separately in your validation notes.

Keep your task and raw evidence private until reviewed for secrets. Reports omit evidence contents and local evidence paths, but include changed repository paths, Git/submodule metadata and check names; review them before sharing.

## Stay current

Normal CLI commands use a daily per-user cache to check public GitHub release metadata. An unavailable cache or simultaneous starts can cause extra requests. Stable releases are preferred; previews are labeled and considered when no stable release is returned. Notices go to stderr, so `inspect` JSON remains usable. This hook only checks versions; it does not download, install, execute or change harness code. Offline failures do not fail your contribution checks. No workspace paths, task files or credentials are sent.

```sh
python3 harness.py updates
python3 harness.py updates --force
```

Use the second command to bypass the daily cache. Set `SWG_HARNESS_UPDATE_CHECK=0` in your environment to disable automatic and explicit checks (including in CI). Hooks run when the CLI is used; no background scheduler or service is installed. Agent session instructions also call the cached command. For updates, read the linked release notes and replace the harness package or update your clean Git checkout; keep task/evidence files separately.

## Work with your preferred model or tool

Give your assistant [the common instructions](instructions/COMMON.md), [the task prompt](instructions/TASK-PROMPT.md), and relevant sections of [the guides](docs/README.md). Use your tool's supported file/context mechanism. This is a portable manual integration; no automatic Codex, Claude Code, Cursor, API or MCP adapter is installed. Human-written changes use the same CLI and templates.

The assistant can help investigate and edit. The local collector checks evidence structure and hashes. A future project-controlled verifier would run adopted profiles and issue trusted intake results. These are separate responsibilities.

For the full explicit reasoning workflow, use the [bundled POODO skill and setup instructions](skills/README.md).

## What is included

- [Stock server](docs/stock-server.md), [stock client](docs/stock-client.md), and [cross-repository change routing](docs/change-routing.md): source-backed maps with pinned upstream revisions.
- [Getting started and community guides](docs/README.md): repositories, setup routes, useful questions, testing, documentation and PR standards.
- [AI-assisted work](docs/ai-assisted-work.md): evidence discipline, bounded parallel work and POODO-derived lessons.
- [PR template](templates/pr.md): concise problem/change/evidence/disclosure notes.
- `harness.py`: read-only Git inspection and local evidence preflight; never executes commands supplied in task JSON.
- [Required intake design](docs/harness-intake-and-attestation.md): proposed project-approved verifier, revision binding, exceptions and portable attestation.
- [Contributing](CONTRIBUTING.md) and [roadmap](ROADMAP.md): how to improve the harness itself.

Regenerate reports from releases before 0.2: candidate inspection now records additional Git state. JSON inputs must be regular files, at most 2 MiB, with unique fields and finite JSON numbers. Evidence must be an absolute regular-file path (not a symlink), at most 512 MiB.

A successful local report always contains `review_eligible: false` and `signed: false`. Its SHA-256 detects accidental changes, not forgery: anyone able to rewrite the report can recompute it. Do not use it as an authenticated gate.

## Develop and test

```sh
python3 -m unittest discover -s tests -v
python3 tools/package.py
```

The complete test suite requires a Git source checkout; extracted ZIPs skip the packaging-only tests. Packaging requires a Git source checkout with committed tracked changes. It reads immutable committed blobs, embeds the commit in RELEASE.json, and refuses unsupported symlinks or reuse of a version with different contents. The ZIP includes no Git history. An extracted ZIP can run the CLI and core tests but needs a Git source checkout to rebuild a release. Inspect the archive before distributing. Python tests exercise disposable repositories, not a live game server.

## Project status

The desired future filter admits only submissions with verified evidence for the current revision to human review. It must first gain maintainer adoption, trusted execution infrastructure and a measured pilot. Local preflight is preparation for that filter, not a replacement. Questions and design discussions should remain open to newcomers.

The original harness code and authored guides are MIT licensed. Referenced SWG source, game assets, external documentation and community messages retain their own terms; this package includes no game source, binaries, credentials or raw Discord exports.
