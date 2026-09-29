# Required harness intake and verifiable evidence

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

Proposed project policy and implementation specification · September 28, 2026. Not adopted or deployed. The user’s intended policy is that human code review starts only after harness intake passes.

## The filter

Every code/content/documentation submission goes through the same intake process, whether written by a person, one model or several tools. The harness returns missing information and failed checks directly to the contributor. Reviewers receive a short report for an exact revision when the applicable intake requirements are met.

The gate asks: “Is this submission sufficiently identified, checked and explained for a person to review?” It does not claim the change is correct or should merge. Maintainers still own design, gameplay, compatibility and acceptance decisions.

Questions, design discussions and requests for help remain open before passing the gate. A newcomer must be able to ask how to satisfy a check. Intake should reduce repeated mechanical work, not require every participant to be an expert.

## Proposed flow

1. Contributor prepares the change and runs local preflight. Missing context produces a specific repair instruction.
2. A project-approved verifier identifies the candidate, base, companion repository revisions and applicable policy. It selects required checks from changed surfaces and declared behavior. The model cannot select an easier profile for itself.
3. Isolated runners execute checks and record evidence. Incomplete, failed and unavailable checks remain visible. Model review is advisory evidence with its own identity, not a substitute for execution.
4. A separate trusted service validates the complete result set and issues the intake receipt. Candidate code cannot access signing credentials or decide the final verdict.
5. The PR check validates the receipt against the current submission and trusted policy. Only a valid `review-eligible` result enters the normal human review queue.
6. New commits or material changes to the base, dependencies, tests or policy require reevaluation. Earlier evidence stays historical. Cached results may be reused only when policy explicitly permits exact relevant input equivalence; the new candidate still needs a new receipt.

Use one updatable PR summary/check rather than repeated bot comments or staff notifications. Do not auto-close an incomplete submission merely because its author needs help.

## States people can understand

| State | Meaning and next action |
|---|---|
| Needs information | Required context is missing; show the precise fields to supply. |
| Running | Accepted verifier is collecting evidence. |
| Needs changes | A required check failed; show failure, location and reproduction command. |
| Blocked | Required environment/check is unavailable or inconclusive; show owner and next action. This is not a pass. |
| Stale | Receipt does not match the current candidate/policy; rerun intake. |
| Review eligible | Required intake checks passed for the named scope; queue for human review. |
| Review eligible with exception | A named maintainer explicitly accepted a listed gap for this candidate; preserve it prominently. |

A reviewer can discover an incorrect profile and return the submission for additional checks. Exceptions must identify the authorizer, candidate, missing check, reason, limits and expiry/revalidation condition. The assistant cannot grant exceptions. Emergency handling and documentation-only profiles belong in an adopted policy before enforcement starts.

## What the receipt binds

Use a versioned, machine-readable evidence manifest and a compact human summary. The signed subject should bind the manifest digest and candidate identity; the manifest references digests of available evidence and outputs.

Required fields:

- Repository identity, base/head commits, tree/patch identity and relevant companion/submodule revisions; dirty local changes cannot masquerade as a committed PR candidate.
- Harness release, policy digest, selected profile and the reason it applies; runner image/environment identity and test definitions.
- Inputs, build outputs, commands, working directories, timestamps, exit status and expected versus observed behavior.
- Every required check with `passed`, `failed`, `not-run`, `inconclusive` or justified `not-applicable`; collector errors cannot silently disappear.
- Evidence locations, retention period, hashes, redaction notes and unavailable artifacts. An inaccessible required artifact may require revalidation.
- Separate author claims, runner observations, human gameplay observations and maintainer exceptions.
- Authoring tool/provider/model identifiers as reported metadata, including unknowns and switches. Such labels do not prove which model authored code.
- Accepted verifier/signer identity and signature verification material; no API keys, private account data or raw private discussions.

Sign the exact manifest bytes using an established scheme. Do not invent a custom cryptographic protocol. A changed report must fail verification. Signing a contributor's own report attributes that report; it does not prove the tests happened.

## Trust the verifier, not the logo

A valid receipt requires the expected artifact binding, approved signer identity/issuer and approved policy/runner. Trust configuration must come from project-controlled settings, never the PR being evaluated. Test/CI/policy changes in a PR require separate review under the trusted baseline; a submission must not weaken its own admission rules.

Execute untrusted repository code in disposable environments without signing credentials, broad repository tokens or access to production. Have the trusted collector independently assemble the result inventory. Test output saying “all passed” is not sufficient. Signing must not be exposed as an unrestricted tool to a coding agent.

Use established provenance mechanisms as building blocks. [SLSA verification](https://slsa.dev/spec/v1.2/verifying-artifacts) connects artifacts to provenance and configured trust. [Sigstore verification](https://docs.sigstore.dev/cosign/verifying/verify/) documents checking artifact signatures and expected identity/issuer. Neither selects the project's gameplay tests.

For GitHub-local intake, an authenticated required check may be enough; portable signed receipts are useful when results cross tools or runners. GitHub’s own [attestation guidance](https://docs.github.com/en/actions/concepts/security/artifact-attestations) distinguishes provenance from security and discourages signing every routine test build. Therefore sign the final portable intake bundle if needed, not every intermediate log. The exact mechanism remains an implementation decision.

## Before adopting the filter

Pilot on documentation, script/data, native and client/server-boundary changes with known outcomes, including deliberately incomplete submissions. Test tampering, stale commits, untrusted signers, altered workflows, omitted failures and unavailable runtime fixtures. Track reviewer minutes, requests for missing evidence, false rejections, contributor time and missed defects. No reduction in review burden has been measured yet.

Maintain a documented recovery path when the runner is unavailable. Set compute limits and deduplicate retries so the filter does not become a new workload. Publish accepted profiles, support routes, exception owners and policy change history before making the check required. Only maintainers can adopt that rule for SWG Source.
