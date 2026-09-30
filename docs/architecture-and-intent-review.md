# Architecture and intent review

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This is
> contributor guidance, not a new project approval gate.

Use this review for changes where choosing the wrong owner or preserving the
wrong behavior could matter: gameplay logic, lifecycle, persistence, scheduling,
protocols, client/server contracts, build or generation paths, and broad
player-visible behavior. A spelling fix, link correction or similarly narrow
change normally needs only its focused validation.

The purpose is to make the intended change and its architectural fit reviewable
before implementation grows around an assumption. The resulting note records a
decision; it is not evidence that the decision is correct or that the behavior
works.

## Establish the intent boundary

Inspect the request and enough of the existing implementation to distinguish
requested behavior from assumptions. Preserve behavior that the change does not
need to alter. Ask a focused question when different answers would materially
change scope, compatibility, persistence, safety or player experience.

Keep a short working contract:

```text
Outcome:
In-scope changes:
Behavior to preserve:
Decisions that change existing requirements:
Implementation assumptions and unresolved questions:
Acceptance checks:
```

`harness.py init` includes the same concerns in an optional `change_review`
object. Leave `required` false for a narrow change that does not need this
review. Set it true for a consequential change and complete the generated
fields before local preflight:

```json
{
  "change_review": {
    "required": true,
    "scope": "Behavior and explicit exclusions",
    "preserved_behavior": "Nearby behavior that must remain unchanged",
    "affected_surfaces": ["script/game-logic", "persistence"],
    "companion_revisions": ["related-repository@full-commit: reason it matters"],
    "owner_and_integration": "Owning component and existing integration path",
    "precedents_and_alternatives": "Comparable paths and rejected shortcuts",
    "risks_and_unknowns": "Remaining uncertainty or none known within scope",
    "player_visible_effects": "Mechanics, feedback, timing and recovery effects",
    "final_diff_notes": "Alignment, deviations and newly discovered coupling"
  }
}
```

The scaffold is contributor-supplied context. Local preflight checks its shape
and completeness when required and binds the task digest to the candidate; it
does not verify the statements or publish their contents in the report. Older
`swg-task/v1` files without this object remain valid.

Silence does not turn an implementation assumption into a project decision. If
a consequential question remains unresolved, present the alternatives and their
effects before building one of them into a large patch.

## Trace ownership before editing

Follow the current path from authored input to its consumer. Identify the
component that owns the state, lifecycle or contract being changed, not merely a
file containing a matching word. Inspect callers, configuration, generated
artifacts and the other side of shared interfaces where they affect the result.

For a consequential change, compare one or more existing implementations that
share the relevant ownership and failure conditions. Two or three comparisons
are useful when the source provides them. Nearby syntax alone is weak precedent;
prefer examples with the same lifecycle phase, queue, persistence model,
protocol boundary or recovery behavior.

Look for the repository's established process before adding a new wrapper,
manager, queue, cache or generation path. Add diagnostics and validation around
that process when possible. If the established path is a blocker, describe the
blocker and the smallest necessary departure rather than silently creating a
parallel mechanism.

## Record a compact architecture note

Use only the fields relevant to the change:

```text
Task and affected behavior:
Affected repositories and surfaces:
Likely owning component:
Relevant lifecycle, persistence or contract boundaries:
Important symbols, files and generated outputs:

Comparable implementations:
- [path/symbol and why it is comparable]

Direct observations:
Inferences and remaining uncertainty:
Proposed integration point and why it fits:
Alternatives considered:
Shortcuts rejected:
Likely files:
Validation plan and useful control:
Design discussion or maintainer decision still needed:
```

Label observations and interpretations separately. Source inspection can show
an implementation path; it cannot establish which artifact is deployed or what
happened during gameplay.

## Include the player experience when relevant

For a gameplay or player-facing change, inventory only the dimensions the patch
can affect. Mark each one as changed, preserved, added, removed, uncertain or not
applicable:

- mechanics, numerical outcomes and progression;
- text, counters, visual effects, sound and other feedback;
- timing, pacing, transitions and overlapping mechanics;
- controls, agency, counterplay and strategic consequences;
- failure, retry, reset, entry, exit and disconnect behavior;
- group members, pets, spectators and eligibility; and
- rewards and persistence across resets or restarts.

Mechanics and presentation can represent different facts. Test them separately
when that distinction matters. A correct numerical effect does not establish
that its counter or telegraph communicates the intended state, and a correct
display does not establish the underlying effect.

## Review the final change

Before handoff, compare the complete diff with the intent contract and
architecture note:

- Confirm that the selected component owns the changed behavior and state.
- Check that the patch uses the identified lifecycle, queue and contract paths.
- Identify new global hooks, polling, duplicated state, direct database access,
  generated-file edits or bypassed processes and explain why they are necessary.
- Record material deviations, newly discovered coupling and unresolved limits.
- Confirm that unchanged behavior named in the contract still has suitable
  coverage.

Classify affected tests rather than rewriting expectations by default:

- **Retain:** the requirement is unchanged and the test should continue to pass.
- **Replace:** the requirement intentionally changed; explain the decision that
  makes the old expectation obsolete.
- **Correct fixture:** independent evidence shows that setup or expected data was
  wrong; preserve the reason for the correction.

Run the checks appropriate to the affected surfaces and report what they
actually establish. Compilation, deployment and intended-use behavior remain
separate results. The local preflight can bind contributor-supplied evidence to
a candidate, but it does not approve the architecture or independently verify
the reported outcome.
