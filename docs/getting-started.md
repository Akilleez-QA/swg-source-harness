# Getting started with SWG Source

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Community draft · Sources checked September 28, 2026 · Proposed guidance, not an adopted project policy.

You can contribute by testing, documenting, investigating, creating content or writing code. Start with something you can reproduce and explain. A useful bug report or a corrected setup instruction saves other volunteers time too.

## Choose what you want to do

| Your goal | Start here |
|---|---|
| Run a local server and explore | [swg-main quickstart](https://github.com/SWG-Source/swg-main) and the linked [VM guide](https://github.com/SWG-Source/swg-main/wiki/Initial-Setup-Of-The-Virtual-Machine-VM-version-3.0-%28%22Irish%22%29) |
| Change quests, NPC behavior, scripts or tables | [dsrc](https://github.com/SWG-Source/dsrc), an existing feature like yours, and the [wiki](https://github.com/SWG-Source/swg-main/wiki) |
| Change server engine behavior | [src](https://github.com/SWG-Source/src), built within the swg-main environment |
| Change the game client or development tools | [client-tools](https://github.com/SWG-Source/client-tools) and its branch-specific build instructions |
| Investigate models, textures or client content | [client-assets](https://github.com/SWG-Source/client-assets), [mesh](https://github.com/SWG-Source/mesh), and the wiki's content/tool guides |
| Work on chat, friends or mail infrastructure | [stationapi](https://github.com/SWG-Source/stationapi) alongside the calling server code |
| Find an existing task | Issues in the relevant repository and [qa-testing](https://github.com/SWG-Source/qa-testing); check whether someone is already working on it |

These are starting points. A feature can cross several repositories. Adding an item may involve a server template, a shared template, a client appearance and database template registration. Editing a shared enum or network message can require matching client and server changes. Trace a working example before deciding which files to edit.

**SWG Source is a particular project.** Advice for Core3, another emulator or another Source fork may describe different APIs, tools or behavior. When searching or asking an AI for help, provide the repository owner, branch and relevant source files.

## Get a known baseline working

The official swg-main README directs newcomers to a prepared VM. That is a documented route to a local environment; it is not the only possible setup. The linked guide describes VM3 “Irish” and contains older software versions and network examples. Read it alongside current download information in Discord's rules-and-info channel, reached through the [project's Discord link](https://discord.gg/Va8e6n8). Do not assume a historical image or someone else's IP address matches your environment.

Keep these activities separate:

- **Obtaining the playable client:** the [client update guide](https://github.com/SWG-Source/swg-main/wiki/How-To-Update-The-Client) describes a package and `UpdateSwgClient.bat`.
- **Compiling client source:** client-tools has a separate Windows toolchain and produces executables/tools; it does not by itself supply a complete playable data installation.
- **Building the server:** swg-main coordinates server code, Java scripts, data compilation, configuration and database steps.

Before modifying anything, record which versions you have and prove you can reach your intended baseline: start the local server, connect the client, load a character and try the area you want to change. Keep a recoverable copy or snapshot before setup changes that affect existing data. Use your own development environment for experiments.

A local development VM may intentionally allow password-free accounts and broad GM access. Public access is a separate configuration task: see [account authentication](https://github.com/SWG-Source/swg-main/wiki/Enabling-Auth-To-Make-Accounts-Require-Passwords-For-Login), [GM restrictions](https://github.com/SWG-Source/swg-main/wiki/Enabling-Admin---God-Mode-Restriction---Limit-Admin-Commands-To-Specific-Accounts) and [external access](https://github.com/SWG-Source/swg-main/wiki/Enabling-External-Access-To-Your-Server). Establish the actual host/VM/network arrangement before changing it.

## Pick a first contribution you can finish

Good starting points include reproducing an issue on a stated revision, correcting a broken documentation link, adding a missing test step, or making a small content fix with an existing example. State the desired player-visible behavior before editing. Keep unrelated cleanup for another change unless it is necessary to make this one correct.

For example, a historical contributor attempted a full client build because they thought an expertise edit required C++. The [discussion redirected them to datatables and icon mappings](https://discord.com/channels/366560008068005892/694859723513659463/810903741766041621). The useful habit is to identify the smallest existing mechanism that implements the behavior.

If using AI, give it that same task boundary and ask it to identify the actual implementation before editing. Read its diff, run the affected behavior and explain the result in your own words. An agent's confidence or another agent's agreement is not a test result.

## Ask questions that are easy to help with

Choose the relevant development or support channel using its current description and pins. Search recent discussion, then provide the smallest useful context:

```text
Goal:
Repository / branch / commit:
Setup (VM or custom, OS, toolchain, client build):
What I changed or ran:
Expected result:
Actual result and first relevant error:
What I already checked:
```

Share text logs when possible and remove passwords, tokens and personal account details. Include the command's working directory; include a screenshot when the problem is visual. You do not need to solve the bug before asking, and it is fine to say which part you do not understand.

Maintainers and contributors volunteer their time. Keep the discussion in one relevant place, allow time for replies and avoid repeatedly tagging people. When something works, reply with the fix and any remaining limitation. That final update makes the conversation useful to the next person.

Next: [Building and debugging](building-and-debugging.md).
