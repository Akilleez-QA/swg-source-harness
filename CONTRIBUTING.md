# Improve the harness

This repository is the canonical development home of this harness. It is independently maintained and does not speak for SWG Source staff.

Useful first contributions include clearer instructions, corrected source links, reproducible CLI bugs, better check profiles and examples of confusing submissions. Open an issue with the behavior, your version/setup, minimal steps and expected/actual result. Never include tokens, private archives or account data.

For code changes, work on a branch, keep a coherent scope and run `python3 -m unittest discover -s tests -v`. Add meaningful coverage for changed behavior. Explain limitations. For documentation, check linked sources, local links and any runnable commands. Use templates/pr.md and disclose AI assistance in code/content and PR prose separately.

Discuss provider adapters, trust/signing changes and gate architecture before substantial implementation. Local self-reports must never be promoted to trusted approval. Signing and candidate execution need separate authority. Test commands supplied by contributors remain data unless an explicitly designed, isolated executor owns their execution.

Review comments should point to behavior, evidence or a concrete improvement. Beginners can ask for help without completing intake. Reply to review feedback and keep PR notes aligned with the final diff.

The mandatory submission gate described in docs is a proposal for downstream adoption, not an existing requirement for contributing here. Until an accepted verifier exists, ordinary human review and CI are used. Do not label a proposed adapter or platform supported until its documented workflow has been exercised.
