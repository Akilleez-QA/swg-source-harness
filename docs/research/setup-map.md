# SWG Source setup and build knowledge map

> Independent historical research summary; not an official project specification.

Checked 2026-09-28 (session research; local archive dated 2026-09-26). Read-only investigation, no setup commands run. Findings describe documented routes and historical troubleshooting, not a newly validated installation recipe. No assumption that the user's server migration is the community baseline.

## Strong archive cases: follow the correction, not the first answer

Source: public Discord export: `SWG Source - Development chat - client_build_dev_chat [694859723513659463].json`, 1,792 messages. `win-dev-chat [772240046731821087].json` contains zero exported messages; absence of evidence only. These cases predate recent AI use and are not allegations of AI-caused errors. They identify traps a harness should prevent.

### Toolchain is more precise than IDE version

December 28 2020 Aconite announced VS2019 compatibility provided Visual C++2013/MSBuild2013 remained installed. January21 2021 a user tried Debug, switched Release, then reported RC1015 missing `afxres.h` with VS2019 plus **2013 Express**. Advice about newer MFC components did not settle it; the user installed full2013 and explicitly confirmed Release built with zero errors. Optimized still lacked `dpvs.lib`. Current local client-tools README specifically excludes Express but broadly says VS2013-only: distinguish IDE, compiler/toolset, component packages, architecture and configuration. Do not interpret Release success as Optimized success.

- [VS2019 with old toolset](https://discord.com/channels/366560008068005892/694859723513659463/793245170849546240)
- [Actual afxres.h error](https://discord.com/channels/366560008068005892/694859723513659463/801926338247655494)
- [Confirmed full2013 fix](https://discord.com/channels/366560008068005892/694859723513659463/801934890765123608)
- [Remaining Optimized failure](https://discord.com/channels/366560008068005892/694859723513659463/801940064920666112)

### Determine the change layer before choosing a build

February15 2021 Jayne hit an archive.lib link failure while trying to change expertise. The reason for compiling the client was hearsay that adding expertise boxes required it. Aconite clarified that changes within existing tree constraints are datatable changes; new entries additionally need icon mapping/sprites, not necessarily client C++ or UI editor changes. He supplied his GU16 commit as a working comparison. The numerical tree limit was tentative ('I think'); do not promote 7x7 into policy without source verification. Linker error itself has no confirmed resolution in this excerpt; task-layer misunderstanding does.

- [Reason for attempted client compile](https://discord.com/channels/366560008068005892/694859723513659463/810903395887349800)
- [Correction](https://discord.com/channels/366560008068005892/694859723513659463/810903741766041621)
- [Known implementation](https://github.com/SWG-Source/dsrc/commit/3a0c0f697906d5e9de8b8985016a85517316a718)
- [Icon mapping qualification](https://discord.com/channels/366560008068005892/694859723513659463/810906255395913740)

### Working directory, matching DLLs and config entry point are runtime dependencies

August30 2023 SgtMustang's debug executable built but launch reported missing skufree. Aconite directed the VS working directory to the actual client data installation and supplied matching `_d.dll` dependencies; user confirmed launch. Subsequent profiler setup revealed incomplete guidance: Aconite first said all configurations entered through client.cfg. SgtMustang checked ClientMain.cpp and found a separate client_d.cfg requirement; Aconite explicitly corrected the advice. Debug menu became visible; later messages still reported profiler output absent. A successful launch or debug menu is not proof profiling worked.

- [Initial runtime symptom](https://discord.com/channels/366560008068005892/694859723513659463/1146466592222363779)
- [Working directory](https://discord.com/channels/366560008068005892/694859723513659463/1146467683899031622)
- [Matching DLLs](https://discord.com/channels/366560008068005892/694859723513659463/1146468212637184160)
- [Launch confirmed](https://discord.com/channels/366560008068005892/694859723513659463/1146470936560816188)
- [Initial incorrect config inference](https://discord.com/channels/366560008068005892/694859723513659463/1146473190416187523)
- [Source contradicts inference](https://discord.com/channels/366560008068005892/694859723513659463/1146500021878009976)
- [Explicit correction](https://discord.com/channels/366560008068005892/694859723513659463/1146500887871770695)
- [Profiler still absent](https://discord.com/channels/366560008068005892/694859723513659463/1146497925476786297)
- [Aconite's resulting Google document](https://docs.google.com/document/d/1zsMRAdlUHlPyt-DBBnAXxPiaa_6XhsxvEZlvNYnHSbw/edit) was linked/pinned in this conversation; document contents not fetched here.

### Generated code can compile and fail behaviorally

August27 2020 Aconite reported Conversation Editor generated Java compiled, attached to NPC, and displayed root dialog but returned to root after first response. Discussion inspected old/new generator output and Java string equality, including a previously applied fix and another occurrence found. August28 Aconite reported it fixed but could not identify the causal change. Harness should require multi-branch interaction tests and preserve a reproducible fix, not encode an uncertain diagnosis as fact.

- [Observed failure](https://discord.com/channels/366560008068005892/694859723513659463/748649720343298139)
- [Candidate code changes](https://github.com/SWG-Source/client-tools/pull/4/commits/fa9e0af1b70cbe5eae1cb60134633cf4f580db9f)
- [Resolution without causal attribution](https://discord.com/channels/366560008068005892/694859723513659463/748767713471627337)

### Alternative builds are not interchangeable

September10 2020 a contributor warned their alternate GitHub client built from an old Reddit lead broke commands and DWB behavior. Other contributors favored getting the current project repository building with supporting docs instead of hunting alternate repositories. No exact code root cause proved in excerpt.

- [Explicit warning](https://discord.com/channels/366560008068005892/694859723513659463/753698520577474673)
- [Repository/documentation response](https://discord.com/channels/366560008068005892/694859723513659463/753701109671133425)

## Official setup routes and boundaries

| Need | Source and interpretation |
|---|---|
| Start a local server | [swg-main README](https://github.com/SWG-Source/swg-main) points to [VM3 Irish guide](https://github.com/SWG-Source/swg-main/wiki/Initial-Setup-Of-The-Virtual-Machine-VM-version-3.0-%28%22Irish%22%29), edited Jan2 2023. It covers VirtualBox appliance, network/hostname, install, snapshots, server start and client login. Versions/timings/IP examples belong to that appliance, not every machine. VM/client download location is Discord rules-and-info. |
| Custom environment | [swg-prepare](https://github.com/SWG-Source/swg-prepare) contains preparation scripts; its linked https://tekaohswg.github.io/new.html returned HTTP404 in this check. A community derivative [langelusse/SWG_prepare](https://github.com/langelusse/SWG_prepare) documents Oracle/Alma/Rocky8 and distinct single/multi-server routes; it clones SWGEvolve scripts and is not an official interchangeable SWG-Source installer. No official container recipe was established in this bounded search. |
| Server build | [Ant guide](https://github.com/SWG-Source/swg-main/wiki/Building-SWG-with-ANT) explains separate src/chat/Java/tab/miff/tpf targets, template CRC generation and database loading. Inspect the actual [build.xml](https://github.com/SWG-Source/swg-main/blob/master/build.xml) before running: `swg` chains clean, checkout, configuration and database creation, whereas scoped compile targets address narrower changes. |
| Existing server update | [2019 update guide](https://github.com/SWG-Source/swg-main/wiki/How-To-Update-The-Server) is historical. `ant update_swg` involves repository updates, database update and compile in local source. It names `compile_dsrc`, absent from inspected local build.xml, so cannot be copied blindly. It explicitly describes ant stop as forcible; local stop target invokes killall. |
| Obtain/update playable client | [2020 client guide](https://github.com/SWG-Source/swg-main/wiki/How-To-Update-The-Client) uses a client package and UpdateSwgClient.bat. This downloads runtime assets; it is not a client source build. Connect by setting login.cfg to the intended server. |
| Compile client/tools | [client-tools README](https://github.com/SWG-Source/client-tools) describes SwgClient project, win32 solution, Release/Optimized/Debug, VS2013 and matching shared changes in src. A changed shipped client binary also belongs in client-assets. Modern forks require their own pinned instructions, not mixing this README with unrelated x64 instructions. |
| Accounts and passwords | [Auth guide](https://github.com/SWG-Source/swg-main/wiki/Enabling-Auth-To-Make-Accounts-Require-Passwords-For-Login) describes VM default username-only account creation, external auth and registration. Existing names must be registered when auth is enabled. This is distinct from game character persistence or GM privilege. |
| GM authorization | [God-mode restriction guide](https://github.com/SWG-Source/swg-main/wiki/Enabling-Admin---God-Mode-Restriction---Limit-Admin-Commands-To-Specific-Accounts) distinguishes universal dev privileges from an admin table, compiles source .tab to .iff, and configures Game/Connection/Login servers. Test both allowed and ordinary accounts. |
| External networking | [External-access guide](https://github.com/SWG-Source/swg-main/wiki/Enabling-External-Access-To-Your-Server) ties cluster_list advertised address, easyExternalAccess, client login address and router/firewall behavior together. Historical broad port-range/DMZ advice is not a universal setup requirement; inspect actual process endpoints and network topology. |
| Content/tools/operations | [Wiki index](https://github.com/SWG-Source/swg-main/wiki) covers zone selection, load manager, SIE, God Client, vendors, quests, objects, ACM, metrics, database transfer and lifetime management. Its SWGSource.com and StellaBellum sections are explicitly archives; titles are not proof every recipe fits current master. |

## Repository relationships to teach

The inspected `.gitmodules` in swg-main maps `src`, `dsrc`, `stationapi`, `serverdata`, and `exe` (the configs repository). Configs marks dirty submodule state ignored, making explicit per-repository inspection valuable. Fresh GitHub organization metadata describes serverdata as clientdata excluding meshes (mesh repository separately). Client runtime data and server content are coupled; updating only server code cannot make missing client assets visible. Build outputs such as .iff and Java .class differ from their authoring inputs, even when source directories are named `compiled`.

Current API lists a `docs` repository pointing to docs.swgsource.com, but its main tree contains only README.md and .gitignore; docs.swgsource.com was inaccessible through the web tool. Do not claim this is a complete live documentation corpus. Local `src/README.md` mentions a 64-bit work-in-progress and historic profiling modes; branch-specific documentation must be checked against the checkout rather than equated with universal stable support.

## Suggested harness context, not new community policy

1. Inventory repository owner/ref, content inputs, build outputs, executable/config/data roots, and target environment before prescribing commands.
2. Route task to script/data/assets/client/server/tooling before deciding to compile or change C++.
3. Separate fresh installation, incremental development, data migration, and runtime operations; tag commands with their actual effects.
4. Track toolchain components and build configuration independently from IDE name.
5. Record evidence at the right level: compile, launch, login, feature behavior, save/reload and diagnostics are distinct.
6. For archive retrieval, include followup corrections, timestamp, exact project/fork and confirmed outcome. Unresolved hypotheses remain unresolved.
7. Keep quickstart appliance defaults separate from public-server auth/privilege/network configuration.
8. Retrieve specialized workflows only when relevant: conversation generation, icons/expertise, object/template pipelines, diagnostics and profiling, database operations.

Local reference commits: client-tools `949451032647e45e42c3aaef3f41b132c8af36e3`; swg-main `91f03571ab442a88988ddc77a64f590fae65a239`. Local source findings describe these checkouts; no fetch or branch change performed.
