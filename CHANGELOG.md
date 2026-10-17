# Changelog

All notable changes to the SWG Source Contribution Harness. Versions follow [SemVer](https://semver.org/); `VERSION` in `harness.py` is the source of truth.

## Unreleased

- CI: run Windows jobs in UTF-8 mode and stop a tempfile retry hang in the update-cache test.
- Docs: README badges and one-line pitch; add CHANGELOG.md and AGENTS.md.

## 0.2.0 — POODO, adversarial hardening and update checks — not yet published

`harness.py` reports 0.2.0; the GitHub release is still a draft and the tag is not pushed.

- Strict report/JSON validation and recursive Git inspection reject malformed evidence, hidden tracked changes and dirty nested submodules.
- Release packaging uses immutable committed blobs, records the source commit and preserves prior archives when validation fails.
- Bundle the full POODO 3.0 skill with setup instructions, optional validation tools and a provenance manifest.
- Add stock server, stock client and cross-repository change-routing guides based on pinned official GitHub sources.
- Add daily cached public GitHub update notices and `python3 harness.py updates [--force]`; `SWG_HARNESS_UPDATE_CHECK=0` disables them. Nothing is installed automatically.
- Partition Windows CI checks without reducing coverage.

Validation: 64 core/adversarial/update/packaging tests plus 3 POODO capsule tests and structural checks. Source guides were not validated by building or running SWG.

## 0.1.1 — Hands-on validation fixes — 2026-09-28

- Fix: `verify` rejects an incomplete preflight report instead of succeeding when only checksum and revision matched.
- Fix: require absolute evidence paths, avoiding caller-directory ambiguity.
- Add regression coverage and a hands-on validation report (`validation/2026-09-28.md`).

## 0.1.0 — Community harness preview — 2026-09-28

- First public preview: community guides, POODO-derived agent instructions, documentation and PR standards, testing guidance, a standard-library local preflight CLI and a proposed trusted intake design.
- 14 CLI tests, passing locally and from the extracted release ZIP.

Boundary for all versions: local reports are unsigned contributor evidence, not a trusted SWG Source admission gate or proof of gameplay correctness. SWG Source has not adopted this harness.
