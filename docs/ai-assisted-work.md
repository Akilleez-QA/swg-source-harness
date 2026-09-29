# Working well with AI assistance

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Community guide draft · checked September 28, 2026 · proposed practice, except the linked project policy.

AI can help you search unfamiliar code, explain relationships, draft changes and identify tests. You still own the contribution. Keep the result small enough that you can explain what changed, why it belongs there, and what you actually tested.

## Start with a useful task

Give the assistant the project and fork, repository revisions, relevant setup, intended behavior and one reproducible example. Say whether you want an explanation, investigation or edit. Name what it may change. A conversation about SWGEmu/Core3, another server's custom fork or a different client generation may have different answers.

Try this starting prompt:

> I am working on SWG Source, repository/fork ___ at commit ___. My setup is ___. I want ___; currently ___. First trace the existing implementation and relevant configuration/data. Identify the smallest change and a test of the player-visible result. Cite actual files and distinguish observations from guesses. Ask before expanding scope or making destructive changes.

Don't upload credentials, account records or private conversations to create context. Relevant excerpts with secrets removed are usually more useful than a whole machine dump.

## Inspect before changing

Ask the assistant to find the current owner of the behavior, its callers, configuration and a nearby working example. A symbol matching your question is only a lead: group-window sizing code is not necessarily the server's group membership limit. A table name does not tell you which relationships it stores.

For content, trace the authored input through compilation, deployment and effective runtime file. For engine code, trace existing queues, ownership and lifecycle before introducing a parallel mechanism. For a command, establish whether it runs in the host terminal, VM terminal, SQL tool, server console or client chat.

Useful follow-up:

> Show the path from this input to the behavior. Which existing component should own the change? What evidence would show that your interpretation is wrong?

## Borrow the useful habits from POODO

These practices adapt POODO's evidence, contradiction and handoff lessons. This guide is not a requirement to run its full decision process for every contribution.

| Habit | What it looks like in ordinary work |
|---|---|
| Define success first | “Choosing each conversation response reaches its intended branch,” rather than “Java compiled.” |
| Separate facts and guesses | “The log contains this error”; “a stale native library could explain it”; “I have not tested that yet.” |
| Keep a competing explanation | Compare missing generated data with a stale deployed copy before rewriting the reader. |
| Choose a discriminating check | Identify which actual file the process loaded; searching the source tree alone cannot answer that. |
| Match claims to evidence | A build passed; launch was observed; gameplay or save/reload may still be untested. |
| Respect contradictions | If the original symptom remains, withdraw the “fixed” claim and preserve the failed result before trying again. |
| Preserve continuity | Record exact revision, attempts, results, unresolved questions and the next useful check. |
| Scale the effort | A text correction needs a preview. Persistence, protocol or lifecycle changes need checks at those boundaries. |

Do not change a test's expected answer merely because the implementation failed. If the test itself is wrong, explain the independent reason and keep a record of the correction.

## Use parallel agents for coverage

Give agents different bounded questions: one maps callers, another checks configuration and assets, another examines test gaps. Each should return source locations, findings and uncertainties. Choose one integration owner to reconcile their results before edits overlap.

Five agents repeating the same answer from the same archive message provide one source of evidence. Compare approaches on the same task and artifact using correctness, useful coverage, elapsed time, rework and reviewer effort. These archives do not establish a reliable model leaderboard.

## Stop a guessing loop early

After repeated failed attempts, summarize what changed and what the results ruled out. Gather a new observation: the first error, effective config, loaded asset, process endpoint or smallest reproduction. Reinstalling repeatedly can erase the evidence and leave the same misunderstanding intact.

A useful handoff is short:

```text
Goal and original symptom:
Repo/commit, build, environment:
What I changed:
Checks and actual results:
Hypotheses ruled out, with evidence:
What remains unknown:
Next discriminating check:
```

Share this summary when asking for help. A raw AI transcript makes other people reconstruct your investigation; attach only relevant excerpts if requested.

## Disclose and review

The project's [AI and modernization policy](https://discord.com/channels/366560008068005892/818213460612612146/1547403437204054096) requires disclosure of AI authorship in the contribution and separately in the PR itself. The contributor remains responsible for the submission. For example:

```text
AI assistance in code/content: [none, or describe the scope]
AI assistance in PR text: [none, or describe the scope]
Human review: [what I personally reviewed]
Validation: [commands/scenarios and actual results]
Not yet checked: [remaining boundaries]
```

Use the current policy for third-party dependencies and modernization proposals too. A model's claim that a library or asset is suitable does not establish project approval or licensing terms.

## Where these lessons came from

Historical examples help select checks; they are not universal fixes:

- A bot's database advice for a visual problem was corrected to environment data; the reporter then [reported success](https://discord.com/channels/366560008068005892/366560008608940035/1322369422379323414).
- A helper corrected earlier debug-client configuration advice after [source inspection contradicted it](https://discord.com/channels/366560008068005892/694859723513659463/1146500021878009976). Humans also benefit from this discipline.
- A contributor [reported an AI change bypassing an existing batch/queue](https://discord.com/channels/366560008068005892/567731005725737011/1549787950076657715). The archive did not supply a patch or scaling benchmark.
- A generated conversation [compiled and attached but failed interaction](https://discord.com/channels/366560008068005892/694859723513659463/748649720343298139). This was a tool-generated code example, not a demonstrated generative-AI failure.

The [full POODO skill](../skills/poodo/SKILL.md) and [setup instructions](../skills/README.md) are bundled. This quick guide adapts its epistemic-integrity, contradiction-protocol and continuity-and-ledger references. The skill is not an SWG Source community policy or a required installed tool.
