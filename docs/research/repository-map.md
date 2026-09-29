# SWG Source repository and setup knowledge map

> Independent historical research summary; not an official project specification.

Observed 2026-09-29T00:27:01.088016+00:00. Read-only official GitHub API plus local tracked documentation. No builds or installations performed. Repository metadata is current at observation; documentation claims are separately labeled and may be stale.

## Repository inventory

| Repository | Role | Default branch | Archived | Last pushed |
|---|---|---|---|---|
| [dependencies](https://github.com/SWG-Source/dependencies) | Legacy external dependency payloads; root includes i386 Oracle and Java; Debian10 dir includes x64/aarch64 Java. | `master` | False | 2021-02-06T00:32:03Z |
| [SWG-Source.github.io](https://github.com/SWG-Source/SWG-Source.github.io) | Jekyll project website, links wiki/Discord and defers current downloads to Discord. | `master` | False | 2020-11-04T18:13:23Z |
| [configs](https://github.com/SWG-Source/configs) | Config templates, used as swg-main exe submodule; not ready-to-run configs. | `master` | False | 2026-05-15T22:55:18Z |
| [dsrc](https://github.com/SWG-Source/dsrc) | Game Java scripts plus text asset/template/datatable inputs. | `master` | False | 2026-05-31T03:06:25Z |
| [swg-main](https://github.com/SWG-Source/swg-main) | Server orchestration: Ant build, submodules, configs and startup scripts. | `master` | False | 2025-06-21T21:26:33Z |
| [clientdata_OLD](https://github.com/SWG-Source/clientdata_OLD) | Historical data repo superseded by serverdata; not marked archived in API. | `master` | False | 2019-06-05T13:15:56Z |
| [src](https://github.com/SWG-Source/src) | C++ server/engine source, database code, native tools; duplicated shared client/server contracts. | `master` | False | 2026-07-26T16:45:04Z |
| [client-tools](https://github.com/SWG-Source/client-tools) | Windows client and authoring/tool source; upstream README describes legacy v120/Win32 build. | `master` | False | 2026-05-13T23:38:49Z |
| [client-assets](https://github.com/SWG-Source/client-assets) | Client-only deployed binaries/assets; plain directories, no new TREs requested by README. | `master` | False | 2026-06-16T01:03:04Z |
| [auth-site](https://github.com/SWG-Source/auth-site) | VM authentication website/scripts. | `master` | False | 2024-02-02T11:51:27Z |
| [web-data](https://github.com/SWG-Source/web-data) | PHP Oracle query helpers. | `master` | False | 2021-07-09T18:24:19Z |
| [stationapi-old](https://github.com/SWG-Source/stationapi-old) | Archived previous stationapi. | `master` | True | 2021-11-27T06:06:44Z |
| [mesh](https://github.com/SWG-Source/mesh) | Model meshes for server and client. | `master` | False | 2020-03-27T19:38:17Z |
| [serverdata](https://github.com/SWG-Source/serverdata) | Server-required client-derived data, excluding client-only sound/most visual assets. | `master` | False | 2026-05-16T22:17:27Z |
| [mods](https://github.com/SWG-Source/mods) | Community mod storage. | `master` | False | 2021-04-12T17:13:49Z |
| [whitengold](https://github.com/SWG-Source/whitengold) | Historical original-source backup fork; provenance/reference, not maintained build baseline. | `main` | False | 2020-10-22T00:33:51Z |
| [qa-testing](https://github.com/SWG-Source/qa-testing) | QA project-tracking repo; empty contents API. | `main` | False | 2020-11-18T16:57:29Z |
| [docs](https://github.com/SWG-Source/docs) | Documentation placeholder/entry point (README only plus gitignore). | `main` | False | 2021-01-02T07:31:31Z |
| [arachne](https://github.com/SWG-Source/arachne) | Ancillary core/tool repository; inspect README before assigning a build role. | `main` | False | 2021-03-02T05:54:06Z |
| [discordeka](https://github.com/SWG-Source/discordeka) | Discord/Station API integration (not this user’s archive bot). | `main` | False | 2021-05-28T07:28:57Z |
| [SubAtom](https://github.com/SWG-Source/SubAtom) | Shared design/development utility library placeholder (README only). | `main` | False | 2021-07-22T14:06:35Z |
| [stationapi](https://github.com/SWG-Source/stationapi) | Standalone SOE-protocol chat gateway/library; Boost/sqlite3/udplibrary dependencies. | `master` | False | 2021-11-27T20:20:05Z |
| [swg-prepare](https://github.com/SWG-Source/swg-prepare) | Older server provisioning helper fork; external guide linked. | `master` | False | 2020-05-02T01:05:12Z |
| [type_examples](https://github.com/SWG-Source/type_examples) | MIF formatting examples for SWG asset types. | `main` | False | 2023-02-11T04:25:41Z |
| [imperator-src](https://github.com/SWG-Source/imperator-src) | Archived Beyond SRC fork. | `master` | True | 2023-06-13T19:26:03Z |
| [releases](https://github.com/SWG-Source/releases) | Large binary release distribution repo. | `main` | False | 2025-06-14T21:55:01Z |
| [swg-auth-wordpress](https://github.com/SWG-Source/swg-auth-wordpress) | WordPress authentication integration fork; description not supplied. | `master` | False | 2026-01-04T22:17:34Z |

## Build and deployment boundaries

* `swg-main/.gitmodules` maps stationapi, dsrc, src, serverdata, and `exe`→configs. Capture all five revisions, not just parent HEAD. `build.properties` separately selects branches; `git_update_submods_to_latest_commit` can move their versions.
* Native C++ `src` and Java `dsrc` are separate compile steps. `swg-main/build.xml` compiles MIF, TAB, TPF/TDF into runtime representations; `load_templates` writes generated templates into the database. A directory named `compiled` under dsrc can still hold authored Java/text inputs; classify by build rule and extension rather than pathname alone.
* `update_swg` includes remote updates, database update and compilation; it is not a read-only or build-only command. `drop_database` and `reset_repos` are explicitly destructive targets. A harness should inspect target dependencies before invoking a convenient command.
* `serverdata` contains server-use data, while `client-assets` is client-only. Appearance/collision variants can differ intentionally; do not simply synchronize all assets both ways.
* Shared client/server source exists in separate repositories. client-tools README explicitly requires coordinated shared-file changes and shipping rebuilt client executables in client-assets when necessary. Cross-repo compatibility must be traced per task; deployment outputs and authored sources are different review artifacts.
* `configs` README references `build_linux.sh`, but that file is absent from current swg-main root listing. Actual `build.xml:update_configs` expands cluster/address/database placeholders. This is a concrete stale-documentation mismatch, not proof the current setup is broken.
* `build.properties` asks users to put settings in `local.properties` rather than edit distributed defaults. Treat resolved configs and local properties as potentially secret; do not add them to context packs.
* Native source CMake requires Bison, Flex, JNI, LibXml2, Oracle, PCRE, Perl, threads, zlib, curl (and platform-specific dependencies). stationapi also needs C++14, Boost program_options, sqlite3 and source udplibrary. Exact architecture and dependency version must follow the selected branch, not blanket “latest”.
* The documented quick start uses a preconfigured VM and wiki. The website mentions VirtualBox and says obtain latest downloads in Discord. This research did not verify downloadable VM/client checksums, supported host matrix, current passwords, or a reproducible bare-metal install.
* client-tools README says VS2013 community/professional (not Express), Win32, `src/build/win32/swg.sln`, Release reliably builds; Optimized/Debug have caveats. A maintainer archive message clarifies VS2019 IDE can use installed VC++2013/MSBuild12. IDE version and target toolset are distinct. Modern fork instructions must not overwrite stock branch guidance.

## Documentation navigation caveat

The official docs README describes a Sphinx `docs/` tree, `make html`, and automatic ReadTheDocs publishing at docs.swgsource.com / swgsource.readthedocs.io. The current default-branch root API listing contains only README.md and .gitignore, with no `docs/` tree. Therefore those build/contribution instructions cannot be assumed executable from the observed default checkout. Website availability and alternate documentation branches were not checked here. The swg-main wiki is the README-linked setup entry point.

## Branch observations

* **swg-main**: `64-bit-types`, `archive-1.2.1`, `master`, `tekaoh/errorless-cfgs`
* **src**: `3.1`, `64-bit-types`, `atmo`, `feature/configurable-entertainer-captcha`, `master`, `testing`
* **dsrc**: `3.1`, `archive-1.2.1`, `atmo`, `bug/space-rls-command`, `feature/configurable-itv-city-travel`, `feature/configurable-tcg-vendors`, `feature/conversation-manager`, `feature/developer-content-utilities`, `feature/lair-interactivity-config`, `feature/space-rare-loot-system`, `feature/wod-integration`, `fix/randbell-deviation-clamp`, `fix/shellfish-harvesting-planet-resource`, `master`, `profession-fixes`, `qa/jedi-qa-gear`, `space-battle-fix-and-refinement`, `wod`
* **client-tools**: `cpp17-refactor`, `feature/configurable-entertainer-captcha`, `master`, `stdlib`, `test`, `wolfssl`
* **serverdata**: `master`, `qa/jedi-qa-gear`
* **client-assets**: `bug/space-rls-commands`, `bugfix/space-parts_patch`, `client-lair-interactivity-search-reset`, `feature/developer-content-utility-commands`, `feature/space-rare-loot-system`, `feature/wod-integration`, `master`, `qa/jedi-qa-gear`, `v3.1`, `wod`, `wod-integration`
* **configs**: `3.0/enable-auth`, `feature/space-rare-loot-system`, `master`, `revert-3-3.0/enable-auth`, `tekaoh/errorless-cfgs`

Matching feature names across repositories suggest coordinated changes, but name equality does not establish compatible commits. `master` is the default on core repos, while ancillary repos commonly use `main`; hard-coding main would fail. Historical/work-in-progress branch names are not release guarantees. Forks such as Galaxies-Reborn are outside this organization inventory and require separate provenance/compatibility review.

## Primary source paths

* `swg-main` local inspected HEAD `91f03571ab442a88988ddc77a64f590fae65a239`; [README](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/README.md).
* `src` local inspected HEAD `7d2159a337281184d6a55db30d2bc9a4013c0e80`; [README](https://github.com/SWG-Source/src/blob/7d2159a337281184d6a55db30d2bc9a4013c0e80/README.md).
* `dsrc` local inspected HEAD `e3aac29b55b46fec2ce2b1518db80a8f70d798a5`; [README](https://github.com/SWG-Source/dsrc/blob/e3aac29b55b46fec2ce2b1518db80a8f70d798a5/README.md).
* `client-tools` local inspected HEAD `949451032647e45e42c3aaef3f41b132c8af36e3`; [README](https://github.com/SWG-Source/client-tools/blob/949451032647e45e42c3aaef3f41b132c8af36e3/README.md).
* `client-assets` local inspected HEAD `eb107b38d6a75e43cc25d4e335493bd2d330f676`; [README](https://github.com/SWG-Source/client-assets/blob/eb107b38d6a75e43cc25d4e335493bd2d330f676/README.md).
* `serverdata` local inspected HEAD `3ee03ed3498849dcda777d5301c8f1f331f50a1a`; [README](https://github.com/SWG-Source/serverdata/blob/3ee03ed3498849dcda777d5301c8f1f331f50a1a/README.md).
* `configs` local inspected HEAD `4c5a76261b6dcb20a9f2e5b68e8a60404162adb9`; [README](https://github.com/SWG-Source/configs/blob/4c5a76261b6dcb20a9f2e5b68e8a60404162adb9/README.md).
* `stationapi` local inspected HEAD `0ac9d0cc2efc0eb2ec26e86435ae98c1cc687997`; [README](https://github.com/SWG-Source/stationapi/blob/0ac9d0cc2efc0eb2ec26e86435ae98c1cc687997/README.md).
* [Build rules](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.xml), [submodules](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/.gitmodules), [build properties](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.properties).
* The package includes curated summaries and public source links; raw API and archive exports are intentionally omitted.
* [Archived community cases and limits](repository-archive-cases.md).
