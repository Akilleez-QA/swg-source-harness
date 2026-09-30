# Documentation and PR notes: a proposed working standard

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

This is a proposal for SWG Source contributors, not an adopted project policy. Use existing repository templates where present. The aim is to let another person understand, repeat and review the work without reconstructing a chat conversation.

The project’s September 2026 policy already requires separate disclosure of generative AI assistance in the contribution and in the PR text. That requirement is independent of the suggestions below. [Published AI policy](https://discord.com/channels/366560008068005892/818213460612612146/1547403437204054096)

## Write documentation for a known environment

Start with who the instructions help and what they accomplish. Identify the applicable repository revision, release or branch and the environment you checked. A branch name alone can move; include a tested commit when the instructions depend on particular code.

Before an executable step, make these things clear:

| Detail | What a reader needs |
|---|---|
| Prerequisites | Required tools, versions, files and an already-working starting state |
| Execution surface | Host or VM, operating system, shell or application, and working directory |
| Inputs and outputs | Which files are authored, which are generated, and where results appear |
| Command effects | Whether the step builds, downloads, changes repositories, edits configuration, updates a database or starts/stops services |
| Expected result | A specific observation that shows the step worked |
| Failure and recovery | Where to find relevant errors; how to restore the previous state when the step changes persistent state |

Scale the detail to the action. Reading a file does not need a rollback plan. Updating a database needs a recoverable starting point and a verified recovery procedure or an explicit statement that recovery has not been tested. Do not imply reversing a Git commit reverses data changes.

Show literal commands only after checking them in the stated environment. Mark values the reader must supply as placeholders; do not embed personal paths, credentials or live server addresses. If a command is illustrative and untested, label it that way rather than presenting it as a working setup recipe. Explain broad wrapper commands: an “update” command may also switch revisions, modify a database and rebuild.

Keep instructions near the component they describe. Link to the canonical prerequisite rather than copying a long setup guide that can drift. Cite historical Discord advice with its date and retain any uncertainty. When documentation and the checkout disagree, record the discrepancy and verify the replacement before publishing it as fact.

### Small documentation template

```markdown
# [Task and intended reader]

Applies to: [repository/release/revision and platform].
Verified: [date, exact revision and environment; or clearly marked unverified].
Outcome: [observable result].

Prerequisites: [tools/versions, input files, starting state].
Run in: [host or VM, shell/application, working directory].
Effects: [what changes; source and generated-output locations].

1. [Verified step or command.]
   Expected: [specific result].
2. [Next step, if needed.]
   Expected: [specific result].

If it fails: [relevant log/check and safe next action].
Recovery: [when relevant; restore steps and verification status].
Limits: [what this guide does not establish].
Sources: [canonical documentation or pinned source links].
```

### Example: choosing the right asset repository

**Task:** Identify where to propose an asset change before editing files.

**Applies to:** The SWG-Source repository layout inspected September 28, 2026. Sources: [client-assets README at eb107b38d6](https://github.com/SWG-Source/client-assets/blob/eb107b38d6/README.md) and [serverdata README at 3ee03ed349](https://github.com/SWG-Source/serverdata/blob/3ee03ed349/README.md).

**Run in:** A repository browser or local text editor. **Effects:** Read-only; no installation or build.

1. Determine whether the file is used only by the game client or is needed by the server. The client-assets README identifies that repository as client-only; serverdata describes its server-use boundary.
2. Trace references to the file and locate its authored source. If it is generated, record the producing tool or build rule before editing the output.
3. Record the intended repository and any separately required client/server variants.

**Expected result:** A proposed file location backed by its consumers and source references. **Limit:** This identifies scope; it does not prove the asset loads correctly. If usage remains unclear, include the file path and references in a focused public question before substituting assets across environments.

## Proposed review intake gate

Under the proposed adoption policy, the project would review only submissions that have passed through the harness. This would apply equally to human-authored and AI-assisted work, regardless of model or tool. **This gate is proposed; it is not current adopted SWG Source policy.**

A successful harness result would establish eligibility for review, not correctness or permission to merge. The PR would link its harness result, the exact evaluated commit and the harness version, alongside meaningful validation and known limits. Every new commit would invalidate the previous intake result for the current submission: rerun the harness on the new commit. Preserve earlier results as historical evidence rather than relabeling them as current.

If the harness cannot evaluate a submission, record that outcome accurately. Any exception process or unavailable-check handling needs to be explicitly agreed as part of adoption; a contributor or agent should not silently bypass the proposed gate.

## Write PR notes for the final change

Lead with the concrete problem and resulting behavior. Explain why the chosen change addresses it. Describe the final implementation; omit the sequence of unsuccessful agent attempts unless it explains a remaining tradeoff.

Keep one coherent scope. Include necessary related files and generated artifacts, but separate unrelated cleanup. Organize commits into meaningful review steps and follow repository conventions. For changes spanning repositories, link companion PRs, identify compatible revisions and state any required deployment order.

Make validation traceable to the submitted code:

- Record the exact tested commit and whether additional local changes were present. A test of an earlier commit is still useful evidence, but label it and explain whether later edits require another run.
- List the relevant command or scenario, environment and observed result. Distinguish compilation, automated checks and in-game testing.
- State limitations directly, including unavailable environments or scenarios not exercised. Avoid “fully tested” when only a narrow path was checked.
- Explain operator steps and recovery where the change affects configuration, deployed files or persistent data.

Keep useful logs and screenshots focused. Link a reproducible test or short evidence file rather than pasting raw model transcripts, entire console sessions or unsupported claims from an agent. The contributor should be able to explain the change and answer review questions.

### Short PR template

```markdown
## Problem and behavior
[Trigger, previous behavior and resulting behavior.]

## Change
[Approach and important tradeoff. Related issues/PRs and source/generated
artifacts where relevant.]

## Architecture and preservation
[For consequential changes: owning component and integration point, relevant
precedent, behavior preserved, and unresolved coupling. Delete if not applicable.]

## Harness intake (proposed adoption requirement)
Result: [link/status], evaluated commit: [SHA], harness version: [version].

## Validation
Tested commit: [SHA; disclose additional local changes if any].
Environment: [only versions/configuration relevant to reproducing the result].
- [Command or scenario] → [observed result].
Known limits: [specific untested behavior or remaining risk].

## Operator notes
[Only if relevant: configuration/data/deployment steps, related revisions,
and recovery procedure/status.]

## AI disclosure
- Contribution: [none / assistance used and its scope].
- PR text: [none / assistance used and its scope].
```

After review edits, update the description to match the new diff and rerun the checks affected by those edits. Reply to each substantive point with the change or supporting evidence. A readable PR should make its status apparent: what changed, what was checked and what still needs attention.
