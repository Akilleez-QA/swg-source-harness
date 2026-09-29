# Adversarial validation for 0.2

Scope: local preflight, report consistency, Git identity and release packaging. Three agents tested separate surfaces using disposable local repositories. No fixture PRs, issues or submissions were posted. Shared model/context means these are partitioned tests, not independent-model corroboration.

## Reproduced defects and repairs

| Surface | Reproduction | Repair and regression evidence |
|---|---|---|
| Report schema | Recomputed checksums let missing/malformed fields, empty evidence and false changed-path lists reach verification success | Strict shape/status validation and comparison with actual Git diff; adversarial-input and report-contract tests |
| Special JSON inputs | FIFO task/report files blocked waiting for a writer | Regular-file checks before reading and descriptor checks after opening; bounded FIFO regression |
| Ambiguous JSON | Duplicate fields and non-finite numbers were accepted by the default decoder | Strict parser rejects duplicates, non-finite constants and overflowed floats |
| Git identity | Index suppression flags hid modified tracked files | Flags block clean inspection without changing the index; Git adversarial tests |
| Nested dependencies | Submodule ignore settings hid a dirty nested dependency | Recursive inspection of initialized submodules; dirty nested fixture rejected |
| Release identity | Staged/unstaged bytes entered the same release version | Require committed tracked state and read immutable Git blobs; embed source commit |
| Packaging boundary | Symlinked directories included external bytes; rejected inputs damaged previous ZIP | Reject linked inputs, build in a temporary location, preserve previous artifacts on validation failure |

Controls exercise ordinary complete/incomplete submissions, linked worktrees, invalid HEADs, uninitialized/mismatched dependencies, private-log omission, nonexecution of task commands, ZIP extraction with spaced paths and reproducible packaging. Tests do not treat a supplied success narrative as proof it happened.

## POODO bundle review

All 25 supplied source text files were inspected for personal/project material. No personal usernames, home paths, credentials or project-specific operational instructions were found. Bytecode caches were excluded. Generic example paths/dates remain. Added standalone setup/dependency notes and removed executable-bit checks that were inappropriate for Python-invoked scripts extracted from ZIPs. The source manifest records original/bundled digests and adaptations; the user's installed skill remains untouched.

The structural validator and three capsule tests passed locally. The behavioral evaluation specification is included but was not run against models. A low-stakes evaluation case may need reconciliation with the skill's strict research gate before such evaluation; no claim of behavioral improvement is made.

## Evidence limits

The local report is still unsigned and contributor-supplied. A checksum is not authentication; malformed-report rejection does not make valid-looking lies true. This release does not execute submitted test commands or enforce a project-approved admission gate. Hostile repositories remain outside the CLI's trusted-checkout boundary; Git configuration can invoke filters. Ignored runtime/configuration files are not covered by Git cleanliness. Large evidence and JSON inputs have documented limits. Sparse/index-suppressed workspaces must use a full checkout for this version.

Tests exercise the implementation, not SWG gameplay, native builds, model-provider integration or measured reviewer-time savings. CI results identify the OS/Python combinations actually exercised and report platform-specific skips.

## Combined local result

After integration, 64 core/adversarial/update/packaging tests and 3 POODO capsule tests passed on Linux; POODO structure checks passed. A read-only live call to the public GitHub releases endpoint returned the expected canonical release notice using an isolated temporary cache. Network-failure tests used mocks; no test submissions were posted.

The update hook now tolerates cache FIFOs, huge timestamps, malformed/deep JSON and incomplete HTTP responses, caches checks daily and never downloads or executes updates. Source-study guides pin official server/client/content revisions and explicitly do not claim runtime validation.
