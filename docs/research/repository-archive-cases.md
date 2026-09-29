# Repository and setup archive cases

> Independent historical research summary; not an official project specification.

Scope: public Development chat exports for general_dev_chat, client_build_dev_chat and swg-repos, captured 2026-09-26. Selected contextual windows were read; this is not exhaustive archive coverage. These are historical community observations, not independently reproduced bugs. No private channels used. Most cases predate widespread AI use and are domain pitfalls a harness must prevent, not attributed AI failures.

## Client/server asset differences are intentional

2020-09-01T13:31:15.491-04:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/750407439576203349)

2020 account explains client LOD files substituted on server removed ship hitboxes. Historical report, not a fresh reproduction. Harness lesson: distinguish render data from collision/server data.

## Trace asset reference chains

2020-09-24T17:16:00.946-04:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/758798922582982697)

Omega reports following custinfo → APT → SSA/LOD → mesh → shader references to identify a broken ACM input chain; replacing two files restored that chain. Do not generalize that file substitution into a permanent deployment recipe.

## Keep uncertainty attached to evidence

2020-10-19T16:41:49.73-04:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/767850015800164368)

Aconite summarizes the ACM workaround/hitbox risk, then immediately says they may not be correct. Preserve this qualification; stronger earlier first-person investigation exists.

## Superseded repository still exists

2022-01-21T15:29:34.607-05:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/934182962780590191)

Cekis explicitly says clientdata_OLD was replaced by serverdata. Current API still does not mark clientdata_OLD archived. Repository existence/archived flag is insufficient to select a baseline.

## AI review policy is a personal practice, not a failure case

2025-09-18T22:40:37.385-04:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/1418426528080990311)

Heron says they use AI for simple boilerplate but carefully review/test. No concrete defective AI patch is identified here. Adjacent September22 discussion flags a bare-metal guide as potentially deprecated because its referenced provisioning repository disappeared.

## Strings cross file formats

2025-09-29T17:51:29.958-04:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/1422340034220261538)

A contributor cannot find conversation response IDs/text after searching serverdata. Aconite directs them to Java c_stringFile and the referenced STF. Harness lesson: teach symbolic reference resolution and binary localization tools, not just text search.

## Check existing work and review architecture before expansion

2026-08-13T17:34:29.745-04:00 · #general_dev_chat · [message](https://discord.com/channels/366560008068005892/366576100941234177/1537575096397340813)

DarkJediMaster proposes a module system and asks about prior work to avoid wasted tokens. Sais distinguishes branch/repository/container selection from modular features; Aconite requests a design document for review. AI-adjacent, not evidence of a proven bad implementation.

## IDE versus toolset

2020-12-28T17:33:06.513-05:00 · #client_build_dev_chat · [message](https://discord.com/channels/366560008068005892/694859723513659463/793245170849546240)

Aconite says VS2019 works when VC++2013 and MSBuild12 are installed. Reconcile with legacy README by separating IDE and compilation toolset; do not automatically upgrade project format.

## Edition matters

2021-01-21T17:02:57.188-05:00 · #client_build_dev_chat · [message](https://discord.com/channels/366560008068005892/694859723513659463/801934890765123608)

A user reports build success after replacing VS2013 Express with full VS2013. This supports environment preflight and documented edition prerequisites, not a general claim all build failures are toolchain faults.

## #swg-repos is a directory, not maintained build truth

19 archived messages. Links include community tools and external guides; presence is not endorsement or proof the tool still works. Notable entries:

* 2020-04-13T15:01:19.998-04:00: https://modthegalaxy.com/index.php?threads/client-archive-always-in-progress-share-yours.382/ — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/699333418672193698)
* 2020-04-21T08:00:27.948-04:00: https://github.com/dpwhittaker/swg-discord-bot — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/702126606822539284)
* 2020-07-15T06:35:37.274-04:00: https://tekaohswg.github.io/new.html — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/732908223564218409)
* 2022-04-26T12:08:56.857-04:00: https://github.com/AlecH92/LegendsUtils — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/968544220535205929)
* 2023-01-29T11:58:14.46-05:00: Blender (v2.8) MGN Plugin  https://github.com/nostyleguy/io_scene_swg_mgn/ — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/1069300452258218144)
* 2023-08-03T16:56:28.289-04:00: Geit's CSR Tool (more or less):  https://github.com/Geit/swg-graphql — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/1136764547923976212)
* 2026-07-07T00:35:53.63-04:00: https://github.com/swgsais/SWGTCG-Standalone — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/1523910405804789852)
* 2026-07-10T21:07:05.446-04:00: https://github.com/Galaxies-Reborn/tre-crypt — [archive message](https://discord.com/channels/366560008068005892/370828581305188353/1525307410254790796)
