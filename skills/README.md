# Bundled POODO skill

[POODO 3.0](poodo/SKILL.md) is included with its references, agent metadata, evaluation specification, capsule checker and fixtures. Invoke it explicitly for consequential or ambiguous work. The ordinary harness workflow does not silently activate the full skill.

## Use without installation

Give your coding assistant `skills/poodo/SKILL.md` as a file and explicitly ask it to use POODO for the task. Keep the whole directory available: relative references are part of the skill. Tools without a native skill system can read the same files as task instructions within their own permissions.

## Install into a skill-capable tool

Copy the complete `skills/poodo` directory into the skills directory documented by your chosen tool. Keep the destination directory named `poodo`. If one already exists, compare versions first; do not overwrite local modifications. Refresh/restart the tool's skill discovery if required, then explicitly invoke its displayed POODO skill (for hosts supporting that syntax, `$poodo`). This package does not modify your tool configuration or install providers automatically.

The included `agents/openai.yaml` supplies explicit-only discovery metadata for compatible hosts; other tools may ignore it. Native goal controls and subagents are available only when the host actually exposes them. The skill never grants additional permissions.

## Optional checks

Reading/invoking the Markdown skill needs no Python dependency. Its capsule/structure tools require PyYAML. In an isolated Python environment, from the harness root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-poodo.txt
.venv/bin/python skills/poodo/scripts/validate_skill.py
.venv/bin/python -m unittest discover -s skills/poodo/evals -v
```

On Windows use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. These checks validate structure, not the quality of a model's reasoning. The behavioral evaluation cases are specifications; no model/provider evaluation is claimed by passing the capsule tests.

## Provenance and privacy

The skill was supplied by the harness owner for bundling. Its source manifest records upstream and bundled file digests and any packaging adaptations. The original local installation is not modified. The bundle excludes bytecode caches and contains generic examples, not user conversation history or live project state.

The public skill was checked for personal usernames, machine paths, credentials, private endpoints and project-specific instructions. Generic sample paths and synthetic dates in fixtures are retained. No personal project material was found in the supplied text files. A portability adaptation removes Unix executable-bit requirements from structural validation because the documented invocation uses Python directly, including ZIP installations.
