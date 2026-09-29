# Run the local harness

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; trusted remote intake and provider integrations are not implemented.

The package contains a Python 3 standard-library CLI, task/report files and community guides. You do not need an AI subscription, API key or provider adapter. Use a human editor or any authoring assistant; the local checks inspect the resulting workspace and task record.

## What the commands do

Run from the unpacked harness directory in a terminal with Python 3 and Git available. Use the actual workspace path and choose task/report output files outside the source workspace so collecting evidence does not change the candidate being inspected. Paths below are placeholders; replace them before running.

```sh
python3 harness.py init --workspace /path/to/workspace --output /path/to/task.json
python3 harness.py inspect --workspace /path/to/workspace
```

`init` writes a task file at the chosen output location. Edit it to describe your objective, scope, acceptance criteria and other requested fields. `inspect` reports the discovered workspace. Confirm that it identifies the intended checkout and revisions before relying on the result. Consult `python3 harness.py --help` and each subcommand's help for the supported arguments.

After preparing your change and task record:

```sh
python3 harness.py check --workspace /path/to/workspace --task /path/to/task.json --output /path/to/report.json
python3 harness.py verify --workspace /path/to/workspace --report /path/to/report.json
```

`check` performs **read-only static inspection of the workspace** and writes the requested report. It does not execute commands written in the task file, compile code, launch a server or client, run gameplay tests, install dependencies or update a database. Report fields describing contributor testing remain contributor-supplied evidence; their presence is not proof the tests ran or passed.

`verify` checks the report against the current workspace according to the local implementation. It does not contact a trusted remote verifier or validate a maintainer-issued signature. A locally generated report is preparation evidence, not an official admission receipt. Read failures and limitations in the report and resolve or explain them; do not replace a failed result with narrative claims.

If source content or revisions change, generate a fresh report. Preserve older reports as evidence of the earlier candidate. The proposed intake policy requires new results for new commits; that future policy is not enforced by a project-approved service in this package.

## Keeping the workspace safe

Use a trusted checkout without concurrent edits. Git may run locally configured filters; this tool is not a sandbox for hostile repositories. Ignored configuration and runtime outputs are outside Git identity checks.

The CLI's preflight commands inspect your checkout; they do not fix it. Review any manual changes separately. Keep credentials and personal configuration out of task descriptions, attached logs and PR notes. Do not infer that a check is safe to run on a live server merely because its name contains “build” or “update”; the underlying SWG build scripts can have broader effects.

There is no global installer or automatic modification of your coding tool's instruction files. To try an updated package, keep the previous package and use the new copy with fresh reports. Preserve your task records and source checkout when removing an old package directory.

## Integrations that remain proposals

| Possible integration | Current status |
|---|---|
| Human editor and local terminal | Uses the local CLI and shared documentation; no model calls required |
| Coding assistants | Can read these files and invoke authorized local commands through their own tools; no tested provider-specific adapter is bundled |
| Hosted model APIs or local model endpoints | No adapter, credential handling or model transport is implemented |
| MCP or another agent framework | No server or integration is implemented |
| GitHub required checks, protected verifier or signed portable receipts | Design only; local reports do not provide this authority |

Future adapters should preserve the same objective, permissions, repository identities and evidence boundaries when switching models. They should keep authentication and provider behavior outside the core and be tested on named host/tool versions before claiming support. Connecting a model or an MCP server would not itself enforce project review rules.

See [intake and attestation design](harness-intake-and-attestation.md) for the proposed trusted gate and [documentation and PR notes](documentation-and-pr-standard.md) for preparing a reviewable submission. The package's root README and tests describe the current implementation; these design documents must not be read as a claim that remote verification exists.
