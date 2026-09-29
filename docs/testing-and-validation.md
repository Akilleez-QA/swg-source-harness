# Testing and validation

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Community draft · Sources checked September 28, 2026 · Proposed harness intake requirements, not an adopted SWG Source policy.

Test the behavior your change promises and the existing behavior it could reasonably disturb. A spelling correction and a database migration need different evidence. Start small, then expand when failures, dependencies or the consequences of a mistake justify it.

## Decide what success means before running the test

Write a short test plan before seeing the result. State the initial condition, action, expected result and one useful control. This helps avoid redefining success around whatever happened to work.

For example: “On an ordinary account, accept this quest, complete the second dialog branch and receive one reward. Reopening the dialog must not grant another reward.” An unchanged quest or the original version can provide a comparison. If the implementation changes the intended behavior during development, update the plan and explain why.

Record the tested repository owner, branch and full commit ID. For uncommitted changes, preserve an identifiable patch or equivalent snapshot. Include affected companion repositories, build configuration, platform/toolchain, deployed executable and asset versions, relevant configuration and database version where they matter. A commit ID alone does not describe a running server assembled from several repositories and local data.

Never include passwords, tokens or private connection details in the evidence package.

## Select a required profile before human review

The proposed harness uses a mandatory intake gate. Select the validation profile appropriate to the changed surfaces before running checks. The profile identifies required checks, their expected results and the policy version that defines them. Once selected, completing its requirements is a condition of becoming **review-eligible**.

Bind the report to the exact candidate commit (and relevant companion revisions/output identities), the base revision and the profile/policy version. If code changes after validation, the old report cannot silently qualify the new candidate: reassess affected checks and rerun what the new change invalidates. The gate itself must evaluate the candidate actually submitted.

An unavailable or inconclusive required check blocks the gate. A contributor or agent cannot turn it into an optional check or mark it passed. The proposed exception route requires an explicit recorded maintainer decision naming the candidate, waived check, reason and remaining limitation. This is a deliberate exception, not evidence that the check succeeded.

**Review-eligible** means the selected intake requirements passed, or a permitted maintainer exception was recorded. It does not mean approved, correct in every respect or ready to merge. Human reviewers still assess design, implementation, evidence and any remaining merge requirements.

## Match the checks to the changed surface

The following table supplies a starting point for profile design. Maintainers would adopt the actual versioned requirements. It does not require every row for every contribution: select all genuinely affected surfaces, with concrete required checks and relevant omissions explained.

| Surface | Evidence that usually helps | Useful control or regression check |
|---|---|---|
| Documentation | Check paths, links, terminology and the changed claim against its source. Preview formatting. For executable instructions, distinguish steps actually tried from source-checked steps. | Make sure a nearby prerequisite or caveat remains accurate. A wording-only edit usually needs no game build. |
| Small data adjustment | Parse or compile the edited data as applicable; verify the changed value reaches the intended consumer. Check row identity, units and column types. | Inspect one unaffected entry or compare the generated output. Test gameplay when the value changes behavior. |
| Scripts and game logic | Compile the affected scripts and trigger the relevant event in game. Test the intended account/character state, one relevant alternate branch and any changed error handling. | Repeat the action where duplicates or state changes matter; exercise an existing neighboring path. |
| Generated content, templates and assets | Check generator/compiler diagnostics, expected outputs, references and any registration step. Load the content with the intended client/server data. | Inspect an existing comparable asset; verify repeat generation where reproducibility matters. A successful generator exit does not prove correct output. |
| Native server/client/tool code | Build affected targets in the supported configuration being claimed. Exercise the changed path, with a focused automated regression test where practical. | Reproduce the original defect against a suitable old version or show a meaningful negative control; check a nearby unaffected case. Claim additional platform/architecture support only with corresponding evidence. |
| Lifecycle, shutdown and recovery | Observe startup/readiness, the requested stop path and process exit. If saves are promised, change identifiable state and reload it after restart. Exercise interruption/failure only in a disposable environment when that is part of the change. | Compare graceful shutdown with failure recovery as separate tests. No crash log is not proof that all save acknowledgements completed. |
| Protocols and shared contracts | Inspect both endpoints and shared definitions. Check field widths/order, representative encoded bytes and decoding, plus an actual exchange when integration behavior changes. | Test the supported peer versions and boundary values relevant to the change. Round-tripping through the same changed encoder and decoder alone can preserve the same mistake. |
| Persistence and migration | Use a recoverable copy with the relevant starting schema/data. Verify upgrade results, expected transformations, constraints and reload behavior. Test rerun/rollback behavior only where supported or promised. | Compare against declared invariants and known records. Reapplying a migration to an already-upgraded database does not prove the original upgrade path. |
| Authentication and privileges | Test intended access with valid credentials/roles and rejection for invalid or ordinary-user cases. Check the server-side decision and relevant session transitions. | A privileged success case alone is insufficient. Verify that a rejected operation leaves protected state unchanged where applicable. |

Cross-cutting changes may need several rows. A quest reward can involve script logic and persistence; an item can involve templates, client assets and database registration. Follow the actual dependency chain rather than classifying only by file extension.

## Distinguish building, deploying and exercising

Keep these results separate:

1. **Built:** the relevant compilation/generation completed and diagnostics were checked.
2. **Deployed:** the intended outputs and configuration reached the test environment.
3. **Exercised:** the action actually entered the changed behavior.
4. **Verified:** observed results matched the expected behavior and relevant controls.

For example, the inspected [swg-main build.xml](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.xml) invokes TemplateCompiler with `failonerror="false"`. Ant's final success message therefore cannot establish that every template compiled successfully. Inspect the tool's errors and expected output.

Likewise, an archived [Conversation Editor investigation](https://discord.com/channels/366560008068005892/694859723513659463/748649720343298139) produced scripts that compiled and attached to an NPC but failed after the first dialog response. A first-screen smoke test would have missed the actual defect.

These examples support a general habit: verify the consumer's behavior, not only the producer's exit status. For build commands and content flow, see [Building and debugging](building-and-debugging.md).

## Make regression checks sensitive to the defect

A useful regression check should fail when the problem is present and pass when it is corrected. Where practical, run it on an appropriate pre-fix revision or introduce a controlled negative case in an isolated test fixture. Do not modify a live environment merely to prove test sensitivity.

Choose an independent reference where possible: a documented file-format expectation, known message bytes, an existing working feature or a confirmed earlier behavior. A test that calculates its expected answer using the same new implementation may prove very little.

Manual tests are valid when they are specific and repeatable. Record the character/account role, input state, steps and observed result sufficiently for another person to try them. Screenshots help with visible results; logs and stored-state comparisons help with events that cannot be seen reliably. Neither needs to become a giant evidence dump.

## Report outcomes without rounding them up

| Status | Meaning |
|---|---|
| **Pass** | The stated test ran on the identified candidate and met its expected result. |
| **Fail** | The test ran and contradicted the expected result. Preserve the failure and explain any repair/retest separately. |
| **Blocked** | A specific prerequisite prevented execution or interpretation. State what is needed to proceed. |
| **Not run** | The check was not attempted. Explain why if the omission affects confidence in the change. |
| **Inconclusive** | The check ran, but the observation was insufficient or ambiguous. Identify the missing signal. |

An environment failure is not automatically a code regression, but it still means the affected claim is unverified. A test disabled to make the suite green is not a pass. If a test has narrower scope than the requirement, report the scope explicitly.

Retain failed attempts that materially explain the final conclusion. Once relevant tests pass, repeat or broaden them when subsequent changes, new failures or unresolved concerns justify it. Avoid requiring unrelated full-game testing for a narrow, low-impact change.

## A compact evidence report

Include this in a PR description or link a short checked-in report when the detail would otherwise overwhelm the change:

```text
Change and promised behavior:
Affected surfaces:

Candidate:
- Repository / full revision / base revision / uncommitted patch reference:
- Relevant companion repository and runtime data revisions:
- Environment / toolchain / architecture / configuration:
- Deployed output identity, if needed:
- Selected validation profile / policy version:

Test:
- Starting condition:
- Action or command, including working directory:
- Expected result (set before execution):
- Control or regression case:
- Observed result:
- Status: Pass / Fail / Blocked / Not run / Inconclusive
- Evidence: concise log excerpt, output comparison or screenshot:

Intake result:
- Review-eligible / Blocked:
- Required checks and results:
- Explicit maintainer exception reference, if any (candidate, check, reason):

Remaining limits:
- Which claim is not yet established?
- What specific check or prerequisite would establish it?
```

Scale the report to the change. A small documentation fix may need two sentences; a shared protocol or migration change deserves enough evidence for another reviewer to assess the compatibility claim. Reviewers should be able to tell what changed, what was actually demonstrated and what remains uncertain without reconstructing the entire development conversation.
