# Archived setup and operations cases

> Independent historical research summary; not an official project specification.

Read-only evidence spike, 2026-09-28. Source: local Discord exports dated 2026-09-26. This report paraphrases public-facing development/support channels; no credentials, private-channel text, or attachments containing configuration secrets are reproduced. Chat instructions are historical evidence, not commands to execute. No runtime reproduction or current compatibility claim is made.

Coverage: feedback-bugs (6,518 messages), admin_commands (3,946), wordpress-auth (2,197), joomla-auth (11), unofficial-hosting (294). The qa-testing export contains zero messages; that establishes an archive limitation, not absence of testing. Targeted outcome searches plus surrounding context were used, not an exhaustive classification of every message. Cases below broaden the previous AI-specific investigation.

## 1. Updating scripts without rebuilding native code

In feedback-bugs on 2021-03-16, a tester reported a Java `UnsatisfiedLinkError` for `_sendDirtyCellPermissionsUpdateToClient`. Another participant asked whether SRC had been updated and recompiled; the tester acknowledged forgetting it. Later the tester reported the first bunker door opening, while a separate `bad player object` warning remained.

Sources: [failure](https://discord.com/channels/366560008068005892/441995780459462657/821493481298067516), [rebuild question](https://discord.com/channels/366560008068005892/441995780459462657/821493959553581106), [acknowledgement](https://discord.com/channels/366560008068005892/441995780459462657/821494027135352843), [remaining warning](https://discord.com/channels/366560008068005892/441995780459462657/821498482791153686), [behavior works](https://discord.com/channels/366560008068005892/441995780459462657/821499310989770762).

Evidence status: reported functional recovery following native rebuild; residual warning explicitly unresolved. Harness requirement: inventory script, native library and executable identities together; distinguish a missing JNI export from Java logic failure. A successful gameplay observation does not erase remaining diagnostics.

## 2. A configuration override masquerading as a source defect

On 2022-04-08, a fatal report said an object already had a far update volume. Support traced an enabled `overrideUpdateRadius=512` option. The operator did not know why it was present, disabled it, and reported the issue resolved locally and on the production server.

Sources: [fatal](https://discord.com/channels/366560008068005892/441995780459462657/962103711231008809), [override hypothesis](https://discord.com/channels/366560008068005892/441995780459462657/962107839692824656), [value found](https://discord.com/channels/366560008068005892/441995780459462657/962108205033484439), [local outcome](https://discord.com/channels/366560008068005892/441995780459462657/962108985580863569), [production outcome](https://discord.com/channels/366560008068005892/441995780459462657/962110329901432982).

Evidence status: specific intervention plus two operator-reported outcomes; no preserved reproduction inspected. Harness requirement: capture effective configuration and provenance before editing source. Test the smallest configuration hypothesis against the original symptom.

## 3. Asset inspection can look at the wrong effective file

On 2019-01-17, a missing string appeared present when viewed in SIE. The conversation established that the loose `proc/proc.stf` differed from the copy in a TRE and overrode it. The reporter substituted the relevant TRE copy into the loose-file location and reported success. The correction explicitly cautioned that SIE's view was not necessarily the client's effective view.

Sources: [which file](https://discord.com/channels/366560008068005892/441995780459462657/535523247345631256), [loose-file override identified](https://discord.com/channels/366560008068005892/441995780459462657/535523614649352202), [suggested intervention](https://discord.com/channels/366560008068005892/441995780459462657/535523998151475200), [viewer limitation](https://discord.com/channels/366560008068005892/441995780459462657/535524244365508619), [success](https://discord.com/channels/366560008068005892/441995780459462657/535524834990489620).

Related historical explanation: [server-to-client bulk synchronization story](https://discord.com/channels/366560008068005892/441995780459462657/535525378119172107) describes deliberate server/client template differences, a server-side line-of-sight workaround copied to the client making terminals disappear, and misnamed patch archives. This is a participant's retrospective explanation, not source-verified here.

Harness requirement: record actual asset resolution order and effective file hash. A broad instruction to make client/server files identical can destroy intentional differences; require a format/consumer contract before bulk synchronization.

## 4. Missing client files recur across installation paths

In February 2025 feedback-bugs, a client executable and update batch appeared unresponsive. The reporter had manually downloaded repository executables; subsequent discussion identified incomplete download/extraction as a candidate. The reporter said a fresh download using a download manager got it running. In December 2025 unofficial-hosting, a separate operator could not find the update batch; they later confirmed they had omitted the first of four archive parts and that extracting it resolved the problem.

Sources: [February symptom](https://discord.com/channels/366560008068005892/441995780459462657/1341764619311779953), [archive detail](https://discord.com/channels/366560008068005892/441995780459462657/1342005156090220608), [February outcome](https://discord.com/channels/366560008068005892/441995780459462657/1342190252848320583), [December symptom](https://discord.com/channels/366560008068005892/1348810043524513823/1447425384197914734), [December confirmed omission](https://discord.com/channels/366560008068005892/1348810043524513823/1449422887931871404).

Evidence status: two independent user-reported recoveries; only December names a definite omitted part. Harness requirement: validate complete release inventory, archive integrity and extraction results before diagnosing executable/source incompatibility. Do not infer a general one-run-only updater rule from informal advice in this exchange.

## 5. Service start is not boot persistence, and restart loops hide causes

In March 2025 unofficial-hosting, an installation guide had started Oracle during installation, but users expected it to remain started after reboot. A correction distinguished initial startup from a boot service. The operator reported success, then immediately had another authentication question, so complete setup was not established. Later autostart discussion distinguished enabling supplied service scripts from blindly restarting crashed game/database processes. Another operator described filling the disk with backups because retention cleanup was wrong and fixing that cleanup.

Sources: [restart distinction](https://discord.com/channels/366560008068005892/1348810043524513823/1349896828472266802), [partial success](https://discord.com/channels/366560008068005892/1348810043524513823/1349928411258290196), [which service](https://discord.com/channels/366560008068005892/1348810043524513823/1354130237834924165), [available service scripts](https://discord.com/channels/366560008068005892/1348810043524513823/1354130548343308319), [retain crash cause](https://discord.com/channels/366560008068005892/1348810043524513823/1354130970940407939), [backup retention incident](https://discord.com/channels/366560008068005892/1348810043524513823/1354178517994307785), [dependency-order caveat](https://discord.com/channels/366560008068005892/1348810043524513823/1354192258542469140).

Harness requirement: distinguish running, enabled-at-boot, ready and reachable. Record DB/listener/chat/game dependencies; retain exit evidence before retries and verify backup retention/disk capacity. No universal service-unit implementation is validated by these historical posts.

## 6. Authentication has several independent configuration surfaces

In June 2023 wordpress-auth, a user changed a SWG-specific UI setting expecting it to fix web behavior. Support directed them to generated server configuration and `localoptions.cfg`. A later user encountered a WordPress redirect to a bundled VM address. Support distinguished WordPress Settings → General site URL from the separate SWG configuration page; an earlier answer had been about the latter. Maintainers also explicitly called the guide out of date. Neither exchange records a conclusive working-login outcome.

Sources: [generated server configuration](https://discord.com/channels/366560008068005892/701881911462854806/1114734127959249017), [correct target file identified](https://discord.com/channels/366560008068005892/701881911462854806/1114734987992907786), [redirect symptom](https://discord.com/channels/366560008068005892/701881911462854806/1116588064022745108), [stale guide](https://discord.com/channels/366560008068005892/701881911462854806/1116588726257188905), [WordPress site URL setting](https://discord.com/channels/366560008068005892/701881911462854806/1116848607367266358), [different UI pages clarified](https://discord.com/channels/366560008068005892/701881911462854806/1116849084741976134).

Harness requirement: model browser URL, web application canonical URL, external-auth endpoint, game advertised address and local DB connection separately. Treat documentation/version drift as a hypothesis, not a reason to replace the entire authentication design. Redact credentials from the evidence record.

## 7. Auth port changes interact with policy; bypass is not the final fix

In July 2023 wordpress-auth, a reported ISP port-80 block led to trying another HTTP port. The operator subsequently reported SELinux blocked the new port and said they disabled enforcement. The archive establishes that operator action, not an independently verified minimal remedy or an acceptable production configuration.

Sources: [initial problem](https://discord.com/channels/366560008068005892/701881911462854806/1125897571404099614), [operator follow-up](https://discord.com/channels/366560008068005892/701881911462854806/1126244723204571277).

Harness requirement: distinguish listening socket, router translation and host policy; inspect denials before changing policy. Record successful broad bypasses as diagnostic evidence requiring a narrower final repair, not canonical setup instructions.

## 8. Authentication transforms need edge-case contracts

The July 2023 Joomla setup was followed by a correction that HTML-escaping passwords changes valid characters. The author acknowledged that the implementation was still in progress and said it would change. No completed patch or regression result appears in the 11-message channel export. A later message calls an unspecified link a scam; the downloaded code was not inspected and the allegation is not independently established.

Sources: [correction](https://discord.com/channels/366560008068005892/1125815902194110504/1125881665093382234), [author acknowledgement](https://discord.com/channels/366560008068005892/1125815902194110504/1125914841295622194).

Harness requirement: specify exact bytes crossing the auth boundary; exercise special-character passwords and identity limits. Separate an acknowledgement or promise from a landed, verified fix. Do not download/install historical auth packages merely because an old setup post links them.

## Evidence handling for a community harness

These cases support an environment/context capture layer before edits: repository and artifact identities, effective configuration with secrets redacted, runtime process/transport map, asset precedence, exact execution surface, and restart/restore dependencies. Outcomes should remain typed as observed logs, reported intervention, reported recovery, source-confirmed contract, or unresolved hypothesis. An archive is useful for selecting discriminating checks; it does not replace checks against the actual target deployment.
