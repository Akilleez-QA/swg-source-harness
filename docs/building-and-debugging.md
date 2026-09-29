# Building and debugging without losing the thread

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Community draft · Sources checked September 28, 2026 · Proposed guidance, not an adopted project policy.

Start by finding which input controls the behavior and which output the running game actually loads. A successful compile is useful evidence, but it cannot prove that the correct executable, configuration or asset reached the game.

## Record the workspace you actually have

In each affected Git repository, these read-only commands help establish the starting point:

```sh
git status --short --branch
git rev-parse HEAD
git remote -v
```

In swg-main, `git submodule status` shows recorded submodule state. Inspect changed subrepositories individually too. The [submodule map](https://github.com/SWG-Source/swg-main/blob/master/.gitmodules) connects src, dsrc, stationapi, serverdata and `exe` (configs). Existing local work may be intentional; preserve it before updates or cleanup.

Also record the compiler/toolset, build configuration and executable/data directories. For a client, distinguish the IDE version from the installed compiler and libraries. A [historical setup problem](https://discord.com/channels/366560008068005892/694859723513659463/801934890765123608) was resolved by installing full Visual Studio 2013 rather than Express, even though the person was using the VS2019 IDE. It does not follow that those exact versions are appropriate for every modern fork.

## Select the build step by the change

The [Ant guide](https://github.com/SWG-Source/swg-main/wiki/Building-SWG-with-ANT) explains the server build. Check the target and its dependencies in your own `build.xml` first. Run Ant from the swg-main directory containing that file; `ant -projecthelp` lists documented targets without selecting a build target.

| Changed input | Target to inspect | What to verify afterwards |
|---|---|---|
| Server C++ in src | `compile_src` | Intended binary built and running; affected server behavior |
| Station API code | `compile_chat` | Correct chat executable and affected social interaction |
| Java scripts in dsrc | `compile_java` | Updated class output and the script's actual event/interaction |
| Datatables (`.tab`) | `compile_tab` | Generated table, expected columns/types and an affected row in game |
| MIF assets (`.mif`) | `compile_miff` | Compiler diagnostics, expected output and how the consumer loads it |
| Object templates (`.tpf`) | `compile_tpf` and applicable CRC/database steps | Template output, registration where required and actual object creation |
| Several content/code layers | Relevant targets or `compile` after examining its dependencies | Every affected layer, including client data where required |

This is a routing table, not a promise that every branch has identical targets. An older [update guide](https://github.com/SWG-Source/swg-main/wiki/How-To-Update-The-Server) names `compile_dsrc`, which was absent from the inspected swg-main checkout. `update_swg` also updates repositories and the database; it is not just a local compile. `swg` includes initial setup and cleaning steps, so it should not be the automatic response to a small edit.

Read individual tool diagnostics as well as Ant's final summary. In the inspected [build.xml](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.xml), the TemplateCompiler apply step uses `failonerror="false"`; a top-level success message alone is insufficient evidence that every template compiled.

## Follow the content all the way to the consumer

A path named `compiled` inside dsrc can still contain authoring inputs. Identify the file type and build rule rather than guessing from the directory name. For a missing or unchanged object, trace:

1. The authoring file and a comparable working example.
2. Its generated output and any table/CRC/template registration.
3. The deployed file, search path or archive that the runtime uses.
4. The server and client components that must agree.
5. The visible behavior after the appropriate reload or restart.

Preserve datatable headers, types and tab separators. For icons, models or textures, verify references and client-side mappings as well as the asset itself. A server-only update may leave a client unable to show new content. Use the wiki's [content and tool guides](https://github.com/SWG-Source/swg-main/wiki), including SIE and ACM guidance, when that workflow applies.

## Client build and runtime checks

Follow the README for the exact client-tools branch. Choose the actual SwgClient project and an explicitly supported architecture/configuration. Release, Optimized and Debug have different dependencies and behavior; success in one does not establish success in another. When a shared definition changes, inspect its counterpart in src. The [upstream README](https://github.com/SWG-Source/client-tools) also explains the client-assets distribution step for changed client binaries.

A built executable needs the correct runtime data, configuration and matching DLLs. Check the debugger's working directory, not only the executable path. In a [2023 debugging thread](https://discord.com/channels/366560008068005892/694859723513659463/1146467683899031622), pointing Visual Studio at the playable client directory and supplying debug DLLs helped get a debug client running. Later advice about the configuration filename was [corrected after source inspection](https://discord.com/channels/366560008068005892/694859723513659463/1146500887871770695). Inspect the entry point in your branch instead of assuming every configuration loads the same file.

For a linker failure, find the earliest missing library or failed prerequisite project. Avoid suppressing link failures merely to produce an executable. For a missing asset at runtime, first establish whether the intended configuration and data directories were loaded before modifying source.

## Test the promise of the change

Use the smallest test that exercises the intended behavior and a nearby case that should still work. Examples:

- A conversation: reach multiple branches, check conditions and rewards, then reopen it.
- A table change: test the edited entry and one unaffected entry; include relevant ordinary-player permissions.
- A new item: create it, inspect appearance and interaction, and reload it if persistence matters.
- A client/UI change: show the affected screen, perform its action and check server-visible effects where applicable.
- A build-tool change: prove it produces the required outputs from the documented starting state.

These are examples, not a mandatory full-game checklist for every patch. Add failure or boundary cases where the change depends on them. Historical [conversation-editor output compiled successfully while dialog branching failed](https://discord.com/channels/366560008068005892/694859723513659463/748649720343298139), which is why compilation and behavior need separate results.

## Keep a short investigation record

Write down the first reproducible symptom, the source revision, each meaningful hypothesis and the observation that confirmed or ruled it out. Change one relevant thing at a time when possible. If a change fixes the symptom but you cannot explain why, say so and preserve a before/after comparison.

For server operations, inspect what the command actually does. The historical wiki describes `ant stop` as forcible and the inspected target calls `killall`; do not treat the command name as proof of graceful saves. Use the shutdown procedure appropriate to your environment and verify the outcome needed for your test.

End with a compact result others can reuse:

```text
Changed:
Tested revision and environment:
Commands / steps:
Observed result:
Not yet tested or still failing:
Relevant log / screenshot:
```

A clear partial result helps volunteers continue the investigation. It is more useful than saying “works” when only the build completed.
