# Finding your way around the stock SWG Source server

Community draft · Upstream checked September 28, 2026 · Source-derived guide; this inspection did not build, start or validate a server.

“Stock” here means the official **SWG-Source** repositories at the revisions below. It does not mean a private fork, a proposed migration branch or a guarantee that every shipped default suits your environment. Record the actual checkout you are using before following a command or borrowing an implementation.

## Which stock revision?

Fresh GitHub API reads resolved these official `master` heads:

| Repository | Examined commit |
|---|---|
| [src](https://github.com/SWG-Source/src/tree/7d2159a337281184d6a55db30d2bc9a4013c0e80) | `7d2159a337281184d6a55db30d2bc9a4013c0e80` |
| [swg-main](https://github.com/SWG-Source/swg-main/tree/91f03571ab442a88988ddc77a64f590fae65a239) | `91f03571ab442a88988ddc77a64f590fae65a239` |
| [configs](https://github.com/SWG-Source/configs/tree/4c5a76261b6dcb20a9f2e5b68e8a60404162adb9) | `4c5a76261b6dcb20a9f2e5b68e8a60404162adb9` |
| [dsrc](https://github.com/SWG-Source/dsrc/tree/e3aac29b55b46fec2ce2b1518db80a8f70d798a5) | `e3aac29b55b46fec2ce2b1518db80a8f70d798a5` |
| [stationapi](https://github.com/SWG-Source/stationapi/tree/0ac9d0cc2efc0eb2ec26e86435ae98c1cc687997) | `0ac9d0cc2efc0eb2ec26e86435ae98c1cc687997` |

**Latest repository heads and swg-main's recorded submodules are different baselines.** At the examined swg-main commit, the gitlinks record src `625e4d1`, dsrc `c7294da`, configs/exe `be961fc`, stationapi `66dc49f`, and serverdata `df41a07`. A clone initialized at those pins is not the same source combination as independently updating every repository to master. Neither combination was runtime-tested for this guide. Use `git submodule status` and record the full component revisions in your own environment. The [submodule declarations](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/.gitmodules) explain which repository belongs at each path.

## The server is a group of programs

The [startup wrapper](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/startServer.sh) invokes Ant. Ant eventually runs [exec.sh](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/exec.sh), which changes to `exe/linux`, launches LoginServer with `@servercommon.cfg`, waits four seconds, and launches TaskManager with the same configuration. That delay is a script detail, not proof of readiness.

The [taskmanager.rc registry](https://github.com/SWG-Source/configs/blob/4c5a76261b6dcb20a9f2e5b68e8a60404162adb9/linux/taskmanager.rc) lists CentralServer, ConnectionServer, SwgDatabaseServer, PlanetServer, SwgGameServer, ChatServer, LogServer and CommoditiesServer launch commands. MetricsServer is commented out there. This is a registry of programs, not a universal count of running processes: zones and load configuration affect topology.

For orientation, follow these components when investigating:

| Symptom or task | First source area to inspect |
|---|---|
| Login, account validation or character-list exchange | `engine/server/application/LoginServer/src/shared/`, including ClientConnection.cpp, DatabaseConnection.cpp and LoginServer.cpp |
| Process management or cluster startup | `engine/server/application/TaskManager/` and `CentralServer/`, plus the effective task and node configuration |
| Client sessions and message forwarding | `engine/server/application/ConnectionServer/` and the corresponding message definitions |
| Planet/process assignment or world simulation | `PlanetServer/`, `game/server/application/SwgGameServer/` and `engine/server/library/serverGame/` |
| Object persistence or database processing | `game/server/application/SwgDatabaseServer/`, `engine/server/library/serverDatabase/` and `game/server/database/` |
| Chat integration | `engine/server/application/ChatServer/` and the separate stationapi repository |
| Auctions or market behavior | `engine/server/application/CommoditiesServer/` and its callers |

These are navigation hints, not a complete architecture specification. Begin at an observed event or message and trace the actual call path before choosing the owner of a fix. The [server application tree](https://github.com/SWG-Source/src/tree/7d2159a337281184d6a55db30d2bc9a4013c0e80/engine/server/application) provides concrete entry points.

Station API is not simply another name for ChatServer. Its [README](https://github.com/SWG-Source/stationapi/blob/0ac9d0cc2efc0eb2ec26e86435ae98c1cc687997/README.md) describes a standalone `stationchat` gateway with SQLite data and dependencies including Boost and the SOE UDP library. A running game cluster alone does not establish that this separately configured service works.

## Gameplay scripts meet native code through JNI

Many content changes start in dsrc's `sku.0/sys.server/compiled/game/script/`, despite `compiled` appearing in the directory name. Its files include Java authoring inputs such as [base_script.java](https://github.com/SWG-Source/dsrc/blob/e3aac29b55b46fec2ce2b1518db80a8f70d798a5/sku.0/sys.server/compiled/game/script/base_script.java) and reusable [library/quests.java](https://github.com/SWG-Source/dsrc/blob/e3aac29b55b46fec2ce2b1518db80a8f70d798a5/sku.0/sys.server/compiled/game/script/library/quests.java). Find a similar working feature before adding another engine API.

The native bridge is in [serverScript/src/shared](https://github.com/SWG-Source/src/tree/7d2159a337281184d6a55db30d2bc9a4013c0e80/engine/server/library/serverScript/src/shared). `ScriptMethods*.cpp` separates areas such as combat, money, containers, quests and object creation. `JavaLibrary.cpp` dynamically loads the JVM, obtains `JNI_CreateJavaVM`, constructs the classpath and registers native methods. Consequently, “Java compiled” does not prove that the game loaded those classes or that a changed native signature matches them. Trace the Java declaration, native registration/signature and C++ implementation together when changing that boundary.

The [SwgGameServer Linux main](https://github.com/SWG-Source/src/blob/7d2159a337281184d6a55db30d2bc9a4013c0e80/game/server/application/SwgGameServer/src/linux/main.cpp) installs file access, networking, shared game facilities, terrain, scripting and pathfinding before entering `GameServer::run`. This helps distinguish missing setup/data from a defect in a particular gameplay script.

## Building involves code, generated data and sometimes the database

The stock [top-level CMake file](https://github.com/SWG-Source/src/blob/7d2159a337281184d6a55db30d2bc9a4013c0e80/CMakeLists.txt) requires C++17 and finds JNI, Oracle, Bison/Flex, LibXml2, PCRE, Perl, Zlib and CURL among its dependencies. Its UNIX flags explicitly include `-m32` and architecture-specific settings. Do not assume a 64-bit host produces a 64-bit server or that a new compiler automatically matches this configuration. Check compiler, native libraries and JVM architecture together. These are source observations, not certification of a supported modern toolchain.

[swg-main/build.xml](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.xml) orchestrates the work:

- `compile_src` builds native server code; `compile_chat` builds the separate chat gateway; `compile_java` invokes javac for script classes.
- `compile_tab`, `compile_miff` and `compile_tpf` transform content inputs using project tools.
- Object/quest CRC generation and `process_templates` feed `load_templates`, which invokes SQL*Plus. The combined `compile` target includes this chain.
- `update_database` runs `game/server/database/build/linux/database_update.pl` with delta mode. Database creation and deletion are separate consequential operations.
- `create_symlinks` connects runtime clientdata to serverdata and `exe/linux/bin` to built tools/binaries.

Inspect target dependencies before execution. A command called “compile” is not necessarily limited to compiler output. Check generated files and tool diagnostics: this revision's TemplateCompiler invocation sets `failonerror="false"`, so Ant's final result alone is insufficient proof of template success.

## Configuration has layers and runtime context

[linux/servercommon.cfg](https://github.com/SWG-Source/configs/blob/4c5a76261b6dcb20a9f2e5b68e8a60404162adb9/linux/servercommon.cfg) includes the shared configuration, default.cfg, network settings, localOptions.cfg, nodes.cfg and additional gameplay files. The startup working directory matters because includes and launch commands use relative paths. Inspect the include chain, command-line overrides and environment used by the actual process; editing an unused copy changes nothing.

[localOptions.cfg](https://github.com/SWG-Source/configs/blob/4c5a76261b6dcb20a9f2e5b68e8a60404162adb9/linux/localOptions.cfg) contains repeated `startPlanet` entries, server-specific sections, scripting controls and GM settings. The examined defaults include broad development privileges, while servercommon disables external authentication. Those defaults are not a public-server access policy. Authentication and GM authorization are separate checks; trace effective LoginServer and GameServer settings and test an ordinary account as well as an allowed account. Never paste private configurations or credentials into a contribution report.

## Lifecycle and updates deserve explicit inspection

In this stock Ant file, `start` depends on `stop`, and `stop` invokes process-name `killall` commands, including `-9` for SwgGameServer. These commands are not isolated to a selected checkout and do not prove graceful persistence. Do not use them casually on a machine hosting another cluster. Establish the intended environment and its shutdown procedure before operating it.

`update_swg` updates repositories, applies database changes and compiles. Its submodule update target checks out master and pulls; it is not a way to preserve a carefully selected candidate automatically. Inventory branches and local changes first. This guide inspected these operations without running them.

For an ordinary contribution, map the smallest affected script, table, native component and client dependency; record the actual versions; then test the claimed behavior and relevant regression. A server build, cluster readiness, successful login and durable saved state are separate observations. Use [Building and debugging](building-and-debugging.md) and [Testing and validation](testing-and-validation.md) to turn that source map into an appropriately scoped evidence plan.
