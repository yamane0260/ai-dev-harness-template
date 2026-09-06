# Assurance Evals

These fixtures verify that the harness distinguishes declared proof from actual current evidence.

Expected properties:

- a structurally complete Claim/Evidence manifest is accepted;
- broken references and unsupported MUST Claims are rejected;
- PASS on a current required gate can produce `MACHINE_VERIFIED`;
- N/A, missing, failing, or stale evidence cannot satisfy a required gate;
- a legacy `ai-review` artifact remains compatible, while a new `ai-review-record` must pass structure, scope, revision, verification-run, and evidence-integrity checks;
- a passing structured AI review is classified `AI_REVIEWED` and is not decisive proof by itself;
- open blocking findings from a human or AI origin prevent readiness;
- a pending MUST Human Check produces `ACTION_REQUIRED` and blocks release.
