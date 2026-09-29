# Finding your way around the stock SWG Source client

This independent guide maps the **official SWG-Source default branch**, not a modernized fork. Fresh GitHub branch lookups on September 29, 2026 UTC returned client-tools `949451032647e45e42c3aaef3f41b132c8af36e3` and client-assets `eb107b38d6a75e43cc25d4e335493bd2d330f676`. Source observations below use those revisions. This research did not build or run the client; build instructions and runtime behavior must be checked in your own environment.

Modernized x64/DX11 forks are separate work. Their advertised compiler, renderer, audio and input choices are not facts about stock master. Identify repository owner and commit before applying advice from that work. The stock project file examined here selects **Win32 and v120**, and the graphics loader recognizes rasterizer versions 5–7. Do not quietly substitute modern-fork setup instructions when a contributor asks about this checkout.

## Four repositories with different jobs

**client-tools** contains C++ client source and development tools. **client-assets** distributes client-side files, including `SwgClient_r.exe`, DLLs, UI files, strings, objects and other assets; it is not a replacement for the full client installation. **dsrc** supplies gameplay scripts and authored content inputs, including server and shared definitions. **serverdata** supplies the client-derived data needed by the server. A feature can cross these boundaries, but that does not mean all four repositories need changes.

The [client-tools README][readme] explicitly calls out shared files that must match the server and asks for a rebuilt client in client-assets when a change requires one. The [client-assets README][assets-readme] identifies the repository as client-only and requests plain-directory contributions rather than new TRE files. The [serverdata README][serverdata] describes the server-use boundary. Server appearance and collision representations can differ deliberately from client rendering data; copying one whole tree over the other is not a general fix.

## Build the application, not just a supporting library

The documented entry is [`src/build/win32/swg.sln`][solution]. The README instructs contributors to select the **SwgClient** project and build it in Visual Studio. `ClientGame` is a supporting library, not the executable to launch. The actual [SwgClient project][project] defines `Release|Win32`, `Optimized|Win32` and `Debug|Win32`, each using toolset `v120`. Its configuration-dependent output directory is under `src/compile/win32/SwgClient/` after resolving the relative project path.

The README describes VS2013 Community or Professional and excludes Express. It describes Release as the public gameplay configuration, Optimized as exposing additional diagnostic/QA facilities, and Debug as offering development diagnostics. It also says only Release reliably builds at that documentation revision and lists linker/dependency caveats. Having configurations in the solution does not establish that all of them build successfully. A newer Visual Studio interface does not imply a newer compiler: record the installed toolset separately from the IDE.

For a first check, open the pinned solution, select Release and Win32, and build SwgClient using the documented IDE operation. Preserve the first meaningful build error and relevant dependency/version information. Do not respond to unresolved symbols by suppressing linker failures or upgrading the entire solution without understanding the missing component. This guide supplies no unverified command-line build recipe.

## Startup and the major layers

[`WinMain.cpp`][winmain] is the Windows application entry. [`ClientMain.cpp`][clientmain] makes the startup sequence easier to follow: shared foundation/files/network/object/game services are installed before client audio, graphics, input, animation, terrain, game and UI services. Follow the actual setup function when tracing initialization or shutdown rather than adding another global initializer.

| Concern | Source starting point |
|---|---|
| Game startup and client-wide behavior | `src/engine/client/library/clientGame/src/shared/core/SetupClientGame.cpp` and `Game.cpp` |
| Client networking | `src/engine/client/library/clientGame/src/shared/network/GameNetwork.cpp` |
| Renderer loading and rendering interface | `src/engine/client/library/clientGraphics/src/win32/Graphics.cpp` |
| Generic UI mediation | `src/engine/client/library/clientUserInterface/src/shared/core/CuiMediator.cpp` |
| SWG-specific screens and UI setup | `src/game/client/library/swgClientUserInterface/src/shared/page/` and `core/SetupSwgClientUserInterface.cpp` |
| Client object-associated data | `src/engine/client/library/clientGame/src/shared/objectTemplate/ClientDataFile.cpp` |
| Asset lookup and configuration parsing | `src/engine/shared/library/sharedFile/src/shared/TreeFile.cpp` and `sharedFoundation/src/shared/ConfigFile.cpp` |

These paths are navigation aids, not interchangeable extension points. Trace an existing screen, command or object of the same kind before deciding where a new behavior belongs. The [engine client library tree][engine-client] and [game UI tree][game-ui] provide the surrounding source.

## Configuration and what actually gets loaded

ClientMain selects `client_d.cfg` when `PRODUCTION == 0` and `client.cfg` otherwise. It also contains handling for `misc/override.cfg` through TreeFile. Build configuration, compile-time production settings and the configuration file used by a particular executable should therefore be recorded separately; a filename suffix alone is not a complete environment description.

The distributed [`client.cfg`][client-config] declares `swgsource_3.0.tre` and includes `login.cfg`, `live.cfg`, `preload.cfg`, `options.cfg` and `user.cfg`. It warns that the tracked file should not normally be edited locally. The included files are not all present at the root of the assets repository: installation, local settings and the complete configured search path matter. Inspect the actual client directory and configuration chain before diagnosing a missing asset or connection problem. Do not paste credentials or private addresses from those files into a PR.

The [graphics loader][graphics] constructs a relative `gl%02d_r.dll`, `_o.dll` or `_d.dll` path according to compilation settings, loads the DLL and obtains its `GetApi` entry point. It accepts rasterizer versions 5–7 and identifies the old version 4 path as unsupported DX8. The [assets tree][assets-tree] ships `gl05_r.dll`, `gl06_r.dll` and `gl07_r.dll`. Consequently a fresh executable tested with an unrelated graphics DLL set is a different candidate, not proof of the source change alone.

The assets tree also contains Miles, Bink, DPVS and other DLLs. Presence does not prove every DLL is loaded, required or still supported by current code. The README explicitly describes removed browser/TCG/help functionality even though historical library files remain in distribution. Diagnose a loader failure from its actual missing module and dependency chain rather than treating every bundled file as an active subsystem.

## Follow UI and content through their representations

A visible UI change may involve a SWG-specific C++ mediator, UI layout/includes and localized strings. The assets repository has [`ui/ui_root.ui` and included layouts][ui-assets], plus `string/`, `datatables/`, `object/`, `appearance/`, `texture/`, `shader/` and `clientdata/` directories. Find the screen's mediator and the layout or string identifier it uses; changing a label is not necessarily a C++ task.

For object/content changes, locate the authored template or datatable and its producing tool before editing a compiled IFF. Record which generated files must ship and which repository owns them. Do not infer that a directory named `compiled` contains only disposable outputs: the wider SWG source layout also uses such directory names for authored inputs. Check the actual build rule and file type.

Changes to shared enums, message layouts, object templates or serialization need a paired server investigation. Matching names do not prove identical definitions. Compare the relevant client and server files at known revisions, then identify the deployed client/server combination the change intends to support. Rendering-only work usually has different evidence needs from a change to the network contract.

## Narrow checks that help reviewers

For a **UI adjustment**, establish the original view, change the identified mediator/layout/string, deploy only the required candidate files to a test client, and exercise opening, closing and using the affected control. Record resolution and relevant client settings. Check a neighboring view when a shared layout is involved.

For an **asset or template change**, verify the reference chain, regenerate through the identified tool where required, and confirm the intended file is the one loaded. Exercise the object in context, including collision or interaction when those are affected. A preview image alone cannot establish server-side behavior.

For a **native client fix**, record source SHA, configuration/toolset, executable identity and matching DLL/data set. First establish that it launches, then reproduce the specific player action. For a shared protocol change, also record server revision and test both ends. State what was not exercised; build success is not gameplay coverage.

Keep the source change, necessary deployment artifacts and operator instructions connected in the PR. A small reproducible scenario and precise revision information are more useful than an assertion that a modernized fork “runs smoothly.”

[readme]: https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/README.md
[solution]: https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/src/build/win32/swg.sln
[project]: https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj
[winmain]: https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/src/game/client/application/SwgClient/src/win32/WinMain.cpp
[clientmain]: https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/src/game/client/application/SwgClient/src/win32/ClientMain.cpp
[graphics]: https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/src/engine/client/library/clientGraphics/src/win32/Graphics.cpp
[engine-client]: https://github.com/SWG-Source/client-tools/tree/949451032647e45e42c3aaef3f41b132c8af36e3/src/engine/client/library
[game-ui]: https://github.com/SWG-Source/client-tools/tree/949451032647e45e42c3aaef3f41b132c8af36e3/src/game/client/library/swgClientUserInterface/src/shared
[assets-readme]: https://github.com/SWG-Source/client-assets/blob/eb107b38d6a75e43cc25d4e335493bd2d330f676/README.md
[assets-tree]: https://github.com/SWG-Source/client-assets/tree/eb107b38d6a75e43cc25d4e335493bd2d330f676
[client-config]: https://github.com/SWG-Source/client-assets/blob/eb107b38d6a75e43cc25d4e335493bd2d330f676/client.cfg
[ui-assets]: https://github.com/SWG-Source/client-assets/tree/eb107b38d6a75e43cc25d4e335493bd2d330f676/ui
[serverdata]: https://github.com/SWG-Source/serverdata/blob/3ee03ed3498849dcda777d5301c8f1f331f50a1a/README.md
