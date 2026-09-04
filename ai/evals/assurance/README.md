# Assurance Evals

These fixtures verify that the harness distinguishes declared proof from actual current evidence.

Expected properties:

- a structurally complete Claim/Evidence manifest is accepted;
- broken references and unsupported MUST Claims are rejected;
- PASS on a current required gate can produce `MACHINE_VERIFIED`;
- N/A, missing, failing, or stale evidence cannot satisfy a required gate;
- an AI review artifact is classified `AI_REVIEWED` and is not decisive proof by itself;
- a pending MUST Human Check produces `ACTION_REQUIRED` and blocks release.
