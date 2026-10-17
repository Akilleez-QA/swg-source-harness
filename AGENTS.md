# AGENTS.md

Notes for coding agents changing **this harness repository**. Agents helping someone contribute *to SWG Source* should follow [`instructions/COMMON.md`](instructions/COMMON.md) instead.

## Rules

- **Standard library only** in `harness.py` and `update_check.py`; Python 3.9+. PyYAML is allowed only for the optional bundled POODO validators (`requirements-poodo.txt`).
- **Don't hand-edit `skills/poodo/`.** It's vendored. Any change must update `skills/poodo-source-manifest.json` (hashes, plus an `adaptations` entry), or `tests/test_skill_bundle.py` fails.
- **Cross-platform.** CI runs Ubuntu, macOS and Windows. Open text files with `encoding='utf-8'`, avoid POSIX-only calls without a skip, and never patch `os.open` or other global `os` functions in tests (on Windows, tempfile retries `PermissionError` up to `TMP_MAX` times and hangs).
- **No network in tests.** Mock `urllib.request.urlopen`; set `SWG_HARNESS_UPDATE_CHECK=0` when running the CLI.
- **Honest boundaries.** Reports are unsigned local evidence. Don't add wording that implies SWG Source adoption, signing, or gameplay validation.
- **Changelog and version.** Add a bullet under `## Unreleased` in `CHANGELOG.md`. A release bumps `VERSION` in `harness.py` and renames the heading to `## x.y.z — title — YYYY-MM-DD`.
- **Commits.** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore(release):`), one logical change per PR.

## Before you push

```sh
python -m pip install -r requirements-poodo.txt
SWG_HARNESS_UPDATE_CHECK=0 python -m unittest discover -s tests -p 'test*.py' -v
python skills/poodo/scripts/validate_skill.py
python -m unittest discover -s skills/poodo/evals -v
```
