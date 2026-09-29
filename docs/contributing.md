# Helping build SWG Source

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

You can make a useful contribution without knowing the whole engine. Pick a small problem you can explain, establish what happens today, and leave enough evidence for someone else to check your result.

This is a proposed community guide, researched September 28, 2026. The **published policies** below come from SWG Source. The workflow and template that follow are practical suggestions, not additional project rules.

## Start with something you can finish

Useful first contributions include:

- Reproduce a reported bug and add clear steps, versions and a short relevant log.
- Test somebody’s change and report what passed, what failed and what you could not test.
- Correct one outdated setup instruction after trying its replacement.
- Explain a confusing file relationship with a small working example.
- Trace a missing string, broken asset reference or script condition before changing it.
- Fix a contained defect with a before-and-after example.

Check existing issues, pull requests and the relevant public discussion first. A short note describing the problem and intended scope helps avoid two people doing the same work. You do not need a large proposal for a spelling fix. For an architectural change or new shared system, describe the design and compatibility implications before investing in a broad implementation; a maintainer explicitly encouraged that approach in the [module-system discussion](https://discord.com/channels/366560008068005892/366576100941234177/1537575762662527036).

## Published policies to know

Read the current [rules-and-info channel](https://discord.com/channels/366560008068005892/818213460612612146) before contributing. Its recorded policies include:

- The project supports non-commercial, non-profit development and restoration through Game Update 22. Allowed changes include restoring qualifying player content, internal/admin utilities, and bug fixes, including bugs present on live. [Mission and contribution scope](https://discord.com/channels/366560008068005892/818213460612612146/818425611756240927)
- Where the historical behavior is ambiguous, consider the original designers’ intent. Changes that make content easier or remove gates should have switches allowing them to be disabled; other features should expose practical operator configuration. [Contribution policy continued](https://discord.com/channels/366560008068005892/818213460612612146/818425661223075930)
- **Disclose generative AI use in the contribution and separately in the PR text.** The contributor remains responsible for the submitted work. The September 2026 policy also sets conditions on changing third-party libraries and limits supported engine/asset modernization; read the original before proposing work in those areas. [AI and modernization policy, September 10, 2026 UTC](https://discord.com/channels/366560008068005892/818213460612612146/1547403437204054096)
- Ask questions publicly rather than sending staff unsolicited direct messages, and allow time for volunteers to respond. [Behavior policy](https://discord.com/channels/366560008068005892/818213460612612146/1201676144710262804)

These are summaries, not a replacement for the current policy or a legal assessment. This guide does not introduce a CLA, a required model, a universal automated-test requirement or a mandatory commit style.

## Find the layer you are changing

| If the problem concerns… | Start looking in… | Check for related changes in… |
|---|---|---|
| Gameplay scripts, quests, content definitions or datatables | `dsrc` | Client strings/assets, configuration and generated server data |
| Native server behavior, database integration or engine code | `src` | `dsrc`, database updates and shared client contracts |
| Client behavior or development tools | `client-tools` | Matching shared server files and a deployable client build |
| Client-distributed assets or binaries | `client-assets` | Their authored source and the server’s matching requirements |
| Server-use appearance/collision or other client-derived data | `serverdata`, sometimes `mesh` | Asset reference chains and intentionally different client versions |
| Startup, build orchestration or config defaults | `swg-main`, `configs` | Generated local configuration and dependency versions |
| Chat service behavior | `stationapi` | Server integration and the selected chat configuration |

Use the [repository map](research/repository-map.md) for details and source links. These are starting points, not permission to change every related repository. Follow the actual call or asset reference chain. For example, a Java conversation can name an STF string table; searching only text in `serverdata` will not locate the display string.

Record the repository, branch and commit you actually used. Check the intended PR base instead of assuming every repository uses `main`, or that the same feature branch name means matching revisions across repositories. Keep local settings and passwords out of the patch and logs.

The [client-tools README](https://github.com/SWG-Source/client-tools#shared-files) calls out matching shared files and shipping rebuilt clients through client-assets when required. The [client-assets README](https://github.com/SWG-Source/client-assets) requests plain directory contributions rather than new TRE files. Server and client assets can differ intentionally; copying an entire client asset tree onto the server is not a general synchronization method.

## Prepare a change someone else can review

Aim for one understandable outcome. A quest fix can include its necessary script and data changes; it does not need unrelated formatting or a dependency upgrade. If work spans repositories, link the companion PRs and explain the compatible combination and deployment order.

Use commits that explain meaningful steps: fix the behavior, add its useful regression coverage, update the relevant instructions. Avoid making reviewers reconstruct the final change from abandoned experiments. Follow any existing repository conventions; do not rewrite commits other people are using without coordinating.

Read your complete final diff. Remove accidental generated files, debug output and unrelated edits. Keep required generated or deployment artifacts when the repository expects them, and explain how they were produced. Compare the behavior with the problem you set out to solve, not just whether the compiler stopped reporting errors.

A small validation record is enough when it answers the right questions:

- What revision and environment did you test?
- What exact command or player action exercised the change?
- What happened before, and what happened afterward?
- What relevant behavior did you check stayed working?
- What remains untested, and what would another tester need to verify it?

Use automated tests where they check meaningful behavior and are practical for the change. A documentation correction may need a verified command; a gameplay fix may need a reproducible in-game scenario. Do not describe a successful build as proof of a working quest or a database migration. Attach short relevant output instead of dumping an entire agent transcript.

## A short PR description

Adapt this to the repository’s existing template. Delete irrelevant sections rather than filling them with boilerplate.

```markdown
## Problem and result
When [specific action], [old behavior]. This change makes [new behavior].

## Scope
[Main change and why. Link related issues/PRs; note operator steps if needed.]

## Checked
- [Revision/environment; command or scenario; observed result.]
- Still untested: [specific limitation, or none known within this scope].

## AI disclosure
- Contribution: [No generative AI / Used for ...; describe the scope accurately.]
- PR description: [No generative AI / Drafted or edited with ...].
```

You own the result even when an agent helped. Be able to explain the important code, where its assumptions came from and how you checked it. If you cannot explain a section yet, investigate it before asking someone else to approve it.

## Make review easier to finish

Answer each substantive review point with the change you made or the evidence behind a different conclusion. Link the relevant commit or lines. If feedback reveals a broader issue, explain the new scope before expanding the patch. After revisions, rerun the checks affected by those revisions and update the PR description so it describes the current result.

If you need help, ask a bounded public question: “I traced this to these two functions; this input gives this result; which behavior is intended?” Include enough context to answer without downloading your entire environment. Say when a result is a hypothesis. Let reviewers respond on their own schedule, and leave a clear handoff if you cannot continue.

A useful contribution leaves the next person with less uncertainty: a reproducible bug, a verified instruction, a focused fix or a well-explained test result all count.
