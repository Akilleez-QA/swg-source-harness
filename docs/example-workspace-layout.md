# Example local workspace layout

> Unofficial independent example. Not endorsed or required by SWG Source. Use
> any directory structure that preserves the same boundaries.

A useful local setup keeps reference source, active changes, generated output,
test installation and evidence separate. This prevents a build or test artifact
from looking like authored source and makes it easier to state what a result
actually proves.

Terms such as **canonical source** and **adjusting source** are sometimes used
for the first two roles below. This guide uses **reference** and **working** to
avoid implying that a local checkout is the project's canonical repository.

```text
swg-work/
  harness/
    swg-source-harness/       # this package; no game source or private evidence

  reference/
    swg-main/                 # clean checkout at the chosen upstream/base revision
    client-tools/             # only when relevant to the task

  working/
    swg-main/                 # writable branch containing the proposed change
    client-tools/             # separate candidate when a client change is required

  generated/
    server-build/             # compiler/generator output, safe to recreate
    client-build/

  staging/
    test-server/              # files prepared for a disposable test environment
    test-client/

  records/
    task.json                 # private local preflight input
    report.json               # review before sharing
    evidence/                 # focused logs, screenshots or comparisons
    runtime-captures/         # observations tied to a named environment and time
```

The names are placeholders. Do not copy personal paths, credentials, server
addresses or private configuration into a contribution.

## What each lane establishes

| Lane | Purpose | It does not establish by itself |
|---|---|---|
| Reference source | Stable comparison point for the selected upstream or base revision | Current deployment or successful gameplay |
| Working source | Exact candidate being authored and reviewed | Successful build, installation or runtime behavior |
| Generated output | Compiler or generator result for named inputs and toolchain | That the output was installed or consumed |
| Staging or test installation | Candidate artifacts prepared for a named test target | That the intended path was exercised successfully |
| Runtime capture | Observation from a named environment, artifact set and time | Behavior on another server, client or later revision |
| Task and report | Contributor intent, candidate identity and local evidence binding | Independent verification, project approval or truth of narrative fields |

Keep the reference checkout clean and pinned while investigating a change. The
working checkout may start at the same commit, but it has a different role: it
contains the candidate branch and is the workspace passed to `harness.py`.
Compare both when local work may already differ from the upstream reference.

Generated files belong in source control only when the destination repository
expects them as contribution inputs or checked-in outputs. Otherwise keep them
outside the working checkout or in an established ignored build directory. Do
not hand-edit generated output when an authoritative source and supported
generator exist.

## Use the local preflight

Initialize the task against the working checkout before making changes. Store
the task outside that checkout so creating the record does not make the candidate
dirty:

```sh
python3 /path/to/harness/harness.py init \
  --workspace /path/to/swg-work/working/swg-main \
  --output /path/to/swg-work/records/task.json
```

After committing and testing the candidate, record the actual checks and bind
each one to the full tested commit. Evidence paths must identify focused regular
files. Keeping them outside the inspected workspace avoids mixing private test
records with candidate source. Then create and verify the report:

```sh
python3 /path/to/harness/harness.py check \
  --workspace /path/to/swg-work/working/swg-main \
  --task /path/to/swg-work/records/task.json \
  --output /path/to/swg-work/records/report.json

python3 /path/to/harness/harness.py verify \
  --workspace /path/to/swg-work/working/swg-main \
  --report /path/to/swg-work/records/report.json
```

The CLI inspects only the named working repository and its initialized nested
submodules. It does not compare the reference checkout, inspect sibling
repositories, run builds, verify a staging directory or observe a runtime. Those
identities and results remain explicit contributor evidence.

## Changes across repositories

Treat each submitted repository as its own candidate with its own commit and
validation boundary. Record relevant companion repository commits in
`change_review.companion_revisions`, link companion pull requests, and state the
combination and deployment order that were tested.

The current harness does not verify sibling companion checkouts. A parent
repository's initialized submodules are inspected recursively, but a quiet parent
status does not identify unrelated client repositories, ignored configuration,
deployed binaries or runtime data.

## Smaller setups

The separation is conceptual, not a requirement to duplicate every repository:

- A clean detached Git worktree can serve as the reference while another
  worktree contains the candidate.
- A pinned remote commit can be the source reference when its exact content is
  available and no separate reference checkout is needed.
- Generated and staging directories can be omitted for documentation-only work.
- Runtime captures are unnecessary when the promised result is fully addressed
  by source or documentation checks.

Use only the lanes relevant to the claim, but do not collapse different roles
into one conclusion. A clean build tree is not a reference source, and a source
diff is not a runtime observation.
