# Route a change across the source, build and deployment

Start with the behavior you want to change, then identify which files actually supply it. SWG Source spans several repositories, generated data and deployed binaries. Editing the right source file is only the first step: identify its consumer and verify the resulting behavior there.

This map comes from official GitHub source inspected on September 28, 2026. It is source-derived guidance, not a runtime validation or a claim that independently current repository heads form a tested release. It uses stock default branches, not the separate 64-bit conversion work or client forks.

## Record the starting combination

The inspected default branch was `master` in all seven repositories:

| Repository | Inspected commit |
| --- | --- |
| swg-main | `91f03571ab442a88988ddc77a64f590fae65a239` |
| src | `7d2159a337281184d6a55db30d2bc9a4013c0e80` |
| dsrc | `e3aac29b55b46fec2ce2b1518db80a8f70d798a5` |
| client-tools | `949451032647e45e42c3aaef3f41b132c8af36e3` |
| client-assets | `eb107b38d6a75e43cc25d4e335493bd2d330f676` |
| serverdata | `3ee03ed3498849dcda777d5301c8f1f331f50a1a` |
| configs | `4c5a76261b6dcb20a9f2e5b68e8a60404162adb9` |

[swg-main's submodule map](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/.gitmodules) places `src`, `dsrc`, `serverdata` and `stationapi` under the parent checkout; `configs` is mounted as `exe`, with `ignore = dirty`. Client-tools and client-assets are not entries in that map. Record their revisions separately when relevant. Inspect effective configuration too: a quiet parent status does not establish unchanged deployment settings.

Use the actual submodule commits in your checkout as the starting combination. Updating each repository to its newest default head is a change in its own right. The pinned [Ant build](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.xml) shows `update_swg` updating repositories, updating the database and compiling; it is not a harmless inspection command.

## Follow the producer and consumer

| Task | Source to inspect | Generated or deployed result | Verify at the consumer |
| --- | --- | --- | --- |
| Quest, conversation or server script behavior | Java under `dsrc/sku.0/sys.server/compiled/game/script`; associated datatables | `compile_java` writes classes beneath `data/sku.0/sys.server/compiled/game` | Exercise the affected script and inspect its errors; record which classes/server build were loaded. |
| Script calls a native engine function | Java declaration/wrapper in dsrc plus native registration/implementation in src | Java classes and rebuilt server binaries | Check the registered method name/signature, then exercise the call and its failure cases. |
| Datatable values | Relevant dsrc `.tab`, including server/shared placement | `compile_tab` invokes DataTableTool and maps tables into data outputs | Check generated output and the feature that reads it; a source edit alone is not deployment. |
| Object template behavior | Server/shared dsrc `.tpf`, inheritance and referenced scripts/assets | TemplateCompiler produces `.iff`; CRC generation and template loading are separate build steps | Confirm generated template, database registration where applicable, spawning and actual interaction. |
| Client UI control or text | client-tools UI code; client-assets UI definition and locale string table | Rebuilt client when C++ changes; updated loose client assets | Open the page, use the control and check displayed text in the intended locale. |
| Collision or other data needed by the server | Relevant serverdata asset and its source/consumer | Server-side client-data files | Check server behavior as well as client presentation; matching filenames do not prove interchangeable contents. |
| Address, cluster or runtime option | configs defaults and the operator's effective configuration | Configured files under the deployment | Confirm the running process reads the intended value; redact secrets from evidence. |

The [serverdata README](https://github.com/SWG-Source/serverdata/blob/3ee03ed3498849dcda777d5301c8f1f331f50a1a/README.md) limits that repository to client-format data needed for server operation. The Ant `create_symlinks` target links it beneath `data/sku.0/sys.client/compiled/clientdata`. The [configs README](https://github.com/SWG-Source/configs/blob/4c5a76261b6dcb20a9f2e5b68e8a60404162adb9/README.md) describes defaults as templates, not ready-to-run settings. Follow the build/deployment you actually use when locating effective files.

## Three concrete traces

**Cell permissions cross the Java/native boundary.** Stock [base_class.java](https://github.com/SWG-Source/dsrc/blob/e3aac29b55b46fec2ce2b1518db80a8f70d798a5/sku.0/sys.server/compiled/game/script/base_class.java#L19864) calls `_sendDirtyCellPermissionsUpdateToClient` and declares it with two `long` arguments and a `boolean`. [ScriptMethodsPermissions.cpp](https://github.com/SWG-Source/src/blob/7d2159a337281184d6a55db30d2bc9a4013c0e80/engine/server/library/serverScript/src/shared/ScriptMethodsPermissions.cpp#L69) registers the same name with JNI signature `(JJZ)V`. Changing this interface requires checking both sides and rebuilding their consumers. A missing native method after a script update warrants comparing those deployed versions before rewriting gameplay logic. Registration in source does not prove the running server contains it.

**A helmet checkbox joins C++, UI layout and localized strings.** [SwgCuiOptMisc.cpp](https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/src/game/client/library/swgClientUserInterface/src/shared/page/SwgCuiOptMisc.cpp#L154) requests `checkShowHelmet`. [ui_options.inc](https://github.com/SWG-Source/client-assets/blob/eb107b38d6a75e43cc25d4e335493bd2d330f676/ui/ui_options.inc#L9533) maps that code-data name to a widget; its checkbox references `@ui_opt:show_helmet` and a tooltip key. The repository contains [string/en/ui_opt.stf](https://github.com/SWG-Source/client-assets/blob/eb107b38d6a75e43cc25d4e335493bd2d330f676/string/en/ui_opt.stf). The reference chain was inspected; the binary string table's individual values were not decoded. A text-only correction and a new control need different changes. Check effective asset precedence and missing-key behavior, not just whether the client compiles.

**A bank terminal separates server behavior from shared appearance.** The server [terminal_bank.tpf](https://github.com/SWG-Source/dsrc/blob/e3aac29b55b46fec2ce2b1518db80a8f70d798a5/sku.0/sys.server/compiled/game/object/tangible/terminal/terminal_bank.tpf) references a shared template and attaches `terminal.bank` and `planet_map.map_loc`. The [shared template](https://github.com/SWG-Source/dsrc/blob/e3aac29b55b46fec2ce2b1518db80a8f70d798a5/sku.0/sys.shared/compiled/game/object/tangible/terminal/shared_terminal_bank.tpf) supplies string identifiers, an appearance and client-data reference. Follow each reference relevant to the change. Do not copy the server template wholesale to the client or assume every appearance asset belongs in serverdata.

## Keep the review boundary explicit

The [client-tools README](https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/README.md) warns that shared definitions must stay compatible across src/client-tools and describes shipping rebuilt clients through client-assets. That requires examining the affected contract, not synchronizing every file. The [client-assets README](https://github.com/SWG-Source/client-assets/blob/eb107b38d6a75e43cc25d4e335493bd2d330f676/README.md) asks contributors to use the plain directory structure rather than new TRE archives.

For each change, report the edited repositories, resulting artifacts, deployment locations and observed checks. Explicitly mark untested client/server combinations. The Ant template-compiler invocation uses `failonerror="false"`; inspect compiler diagnostics and expected outputs rather than treating the outer build's completion as sufficient evidence. Nothing in this source study establishes gameplay compatibility by itself.
