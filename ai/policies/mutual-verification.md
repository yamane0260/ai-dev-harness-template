# Mutual Verification

## Governing principle

AI output, human interpretation, requirements, test expectations and explanations
are all revisable.
Agreement between people and agents does not establish correctness.
Decision authority is separate from evidence about actual behavior.

## Before implementation

For a material behavior, record the intended outcome, an unacceptable outcome,
the basis for expected behavior, and the important untested assumptions.
Use the existing Task Packet rather than a separate document for every question.
An assumed requirement must remain distinguishable from a confirmed requirement.

## During implementation and review

Continue autonomous implementation, verification and repair where the consequences
are bounded and reversible.
Derive relevant expectations from requirements, contracts or user examples before
relying on the implementer's explanation.
Select a meaningful boundary or counterexample; do not invent ritual test cases.

When a human or agent predicts a different result, preserve the disagreement.
Its correction target may be a requirement, implementation, test, explanation,
or still unknown.
Construct a small discriminating observation before deciding who was mistaken.
A human's disagreement is neither automatically a defect nor automatically a
learning failure.
An AI's agreement with a criticism is not evidence that the criticism is correct.

Resolve a real issue by correcting its actual cause.
Reject an incorrect issue only with an explanation and supporting observation.
Do not close an issue merely because participants agree.
Escalate unclear business choices, irreversible consequences and unresolved
material disagreements, not unfamiliar technology alone.

## Required review records

For required reviews, the artifact is a JSON record produced from
`ai/templates/review-record.json`, stored below
`.ai-artifacts/reviews/<change-id>/`.
Declare it with evidence kind `ai-review-record`.
Copy the complete revision object and verification run ID from the current
verification evidence, then reference that evidence file with its SHA-256.
Create the record after actual review; never pre-populate a successful result.

Each check records its Claim, kind, expectation basis, scenario, expected result,
observed result and hashed repository-relative evidence references.
Every covered Claim needs a relevant boundary or counterexample.
Each finding records its Claim IDs, origin, possible correction target, severity,
statement, status, resolution and evidence.
A rejected finding means the criticism was refuted, not that it was inconvenient.

Preserve material assumptions, disagreement outcomes and remaining uncertainty
in the Change Brief or decision record before final verification.
Raw observations, verification evidence and exact-revision review records remain
separate artifacts.
A code, test, requirement or durable-record correction requires new verification
and a review matching the resulting revision.

The legacy evidence kind `ai-review` retains its existence-only behavior so that
historical manifests remain reproducible.
New manifests use `ai-review-record`; a legacy Markdown PASS label must not be
translated into a successful structured review automatically.

The validator checks structure, scope, revision and referenced file integrity.
It also binds the review to the supplied verification run and requires an AI
reviewer before reporting `AI_REVIEWED`.
It does not authenticate reviewer identity or independence, prove an observation
was honestly recorded, validate an oracle's meaning, or measure human understanding.
A passing review never replaces required machine evidence or Human Checks.

## Release and learning

Open blocking findings prevent release, even when machine gates pass.
Advisory findings belong in residual uncertainty and follow-up work.
Knowledge Impact alone does not require a blanket human approval or examination.

Use explanation, prediction, modification and diagnosis to improve both the
implementation and the maintainer's model.
Do not grade understanding against an implementation assumed correct.
Use incidents and missed defects to add focused regression cases, including
cases where a human criticism or a test expectation was wrong.

Stabilize tracked implementation, tests, requirements, manifests, completed
Human Check records and durable knowledge before final verification.
Perform the structured review against that evidence.
If review, Human Check completion or legibility work changes a tracked file, repeat
verification and review against the new revision before release evaluation.
Evaluate release with `validate-assurance --evidence` against the reviewed evidence
file.
Carry the validated Agent Trace summary into that command when the manifest
requires trace coverage.
Running `verify` again creates a new run that requires its own review.

The caller must supply the relevant manifest to release verification.
CI artifact transport and selection of release manifests require explicit
integration in the adopting repository.
