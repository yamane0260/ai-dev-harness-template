# Assurance Claims

## Purpose

An Assurance Claim is an observable property that connects a requirement to the evidence or human observation used to judge it. It replaces statements such as "tests passed" with a narrower statement: "this property is supported by these current checks, and this part still needs a person."

## Relationship model

| Record | Meaning | Example form |
|---|---|---|
| Requirement | Requested outcome or constraint | Invalid input must not partially mutate state |
| Claim | Bounded property expected to be true | A rejected request leaves the stored record unchanged |
| Gate evidence | Deterministic current-run support | Integration gate runs the rollback-focused test |
| AI review | Evidence-grounded scrutiny, not proof | A structured review matches the verification run and has no open blocking finding |
| Human Check | Judgment/observation automation cannot establish | Real-device workflow is understandable and recoverable |
| Residual uncertainty | Known limit of the stated support | Load above the tested volume remains unverified |

Claims should describe behavior or a preserved invariant, not implementation activity. "Add a validator" is a task; "malformed relationships are rejected before release" is a Claim.

## Facets, not a score

- `MACHINE_VERIFIED`: every declared required gate for the Claim passed on the current fingerprint.
- `AI_REVIEWED`: required review evidence satisfies its declared contract; new `ai-review-record` evidence is bound to the supplied verification run and checked for open blocking findings. This may coexist with machine or human facets.
- `HUMAN_REQUIRED`: a linked check remains incomplete.
- `HUMAN_VERIFIED`: linked checks contain a recorded passing observation.
- `UNVERIFIED`: decisive support is absent, failed, N/A, or stale.
- `N/A`: no obligation in that facet; never an implicit pass for a required gate.

## Lifecycle

1. Create a manifest before non-trivial implementation and refine Claim wording as the behavior becomes concrete.
2. Implement focused tests/checks and link the relevant gate plus locator.
3. Complete any MUST Human Checks and save their tracked results.
4. Run `verify` to generate exact-run evidence for the stable state.
5. Run `review-assurance` against that evidence and save any declared `ai-review-record` below `.ai-artifacts/`.
6. Run `validate-assurance --evidence <the-reviewed-evidence.json> --release` to fail closed on remaining MUST gaps without creating a different verification run. Carry the validated Agent Trace summary when the manifest requires one.
7. Move or retain the record according to project audit/maintenance needs; never treat historical evidence as current proof for a new revision.

## Common mistakes

- Treating the existence of a test file as evidence that it ran.
- Linking every Claim to a broad `unit` gate without naming the focused test/behavior.
- Using an AI review as the only basis for a MUST Claim.
- Reusing a hash-valid review from another verification run on the same revision.
- Writing "none" for uncertainty while silently excluding an important environment or failure mode.
- Asking a human to certify technical correctness they cannot evaluate instead of improving deterministic evidence.
