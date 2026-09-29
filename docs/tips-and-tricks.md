# Tips that save time

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Community guide draft · checked September 28, 2026. These are diagnostic habits, not a replacement installation recipe.

## Find the smallest useful work layer

Before compiling the engine, check whether the feature is driven by a script, datatable, template, string table or asset. An [expertise discussion](https://discord.com/channels/366560008068005892/694859723513659463/810903741766041621) redirected someone away from an unnecessary client build. The appropriate layer depends on the actual change.

Find a working example close to your goal and follow its references. Search for both the visible string and its identifier; a Java string-file reference may connect the code to an STF without including the displayed text.

## Check what the running game actually uses

A file visible in an editor may differ from the runtime file. Loose files and packaged assets can override one another. Record the effective path and compare it with the intended output before rebuilding everything. An [archived STF case](https://discord.com/channels/366560008068005892/441995780459462657/535523614649352202) was resolved after identifying a loose-file override.

Keep source, generated output and deployed output distinct in your notes. A successful compile in one directory does not prove the running process loaded it. Server and client assets can differ deliberately; don't bulk-copy one over the other to make them “consistent.”

## Preserve the first useful error

Copy the command, working directory, first relevant failure and a little surrounding context as text. Later errors may be consequences. Note the last known working state and the first action after which it failed. Screenshots help visual problems; searchable text helps compiler and runtime diagnostics.

Change one explanation at a time where practical. Record the result even when it fails. A short failed-attempt list prevents the next helper from repeating your work.

## Capture versions cheaply

In the relevant checkout, these read-only commands are useful starting points:

```sh
git status --short
git branch --show-current
git rev-parse HEAD
git submodule status
```

A blank branch can mean detached HEAD. Run the first three inside any changed submodule too; the parent revision alone does not capture its local edits. Review outputs before posting; local names and paths can contain private information. Record the executable/build configuration separately: repository state does not identify a binary you copied from elsewhere.

## Read a command's effects before running it

Convenient target names can hide checkout changes, configuration generation or database operations. In the inspected [swg-main build rules](https://github.com/SWG-Source/swg-main/blob/91f03571ab442a88988ddc77a64f590fae65a239/build.xml), `update_swg` updates repositories and the database as well as compiling. Choose a scoped target only after checking the rules in your own revision.

For work that can alter saved state, use a separate test copy and a restorable backup appropriate to that state. Keep the recovery path clear before the experiment.

## Distinguish the tool from its configuration

Record IDE, compiler/toolset, architecture and build configuration independently. “Visual Studio installed” is incomplete. A Release build does not establish Debug or Optimized support, and current fork instructions may differ from the stock README.

Likewise, process started, service enabled at boot, service ready and client connected are four different observations. Verify the one your question concerns.

## Turn one solved problem into a contribution

Post the exact correction, relevant version and observed result in the original discussion. If a guide was misleading, suggest the smallest wording fix and link the source. If the cause remains uncertain, say what restored operation without claiming you proved why.

A useful answer can be as small as “This step needs client_d.cfg for this debug build; here is the source reference and the launch result.” You don't need to become the project's permanent support person to help.
