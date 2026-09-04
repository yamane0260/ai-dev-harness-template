# Runbook: Assurance readiness is not READY

## When to use

Use when `validate-assurance` reports an invalid manifest, `verify` produces `ACTION_REQUIRED`/`BLOCKED`, or release mode exits non-zero.

## Preconditions / safety

- Work from the exact branch/revision intended for release.
- Read `.ai-artifacts/verification/<run>/summary.md` and `readiness.json` first.
- Do not edit a Claim, mark a gate N/A, or downgrade a Human Check solely to obtain READY.
- Do not paste complete logs or credentials into the manifest, Change Brief, or chat.

## Diagnose

1. Run `./scripts/ai/validate-assurance --manifest <path>` to separate structural errors from execution evidence.
2. For `STALE_EVIDENCE`, rerun verification after all code/manifest changes; do not reuse the old result.
3. For `REQUIRED_GATE_NOT_PASSING`, inspect only the named gate log from the latest run. Fix the product/check or correct an inaccurate Claim-to-gate mapping.
4. For `NO_DECISIVE_EVIDENCE`, add a deterministic check or a genuinely necessary Human Check. An AI review alone is insufficient.
5. For `MUST_HUMAN_CHECK_INCOMPLETE`, follow the bounded procedure in `human-checks.json`, record performer/time/evidence, then rerun release verification.
6. For `REQUIRED_AI_REVIEW_MISSING`, run the relevant review against the diff/evidence and save its concise findings at the declared path.
7. For reference/asymmetry errors, repair both directions of the Claim ↔ Human Check relationship and revalidate.

## Recover

1. Make the smallest correction that resolves the real evidence or mapping gap.
2. Rerun `./scripts/ai/verify --risk <level> --assurance <manifest> --release` on the final state.
3. Confirm `readiness.json` says `READY` and the fingerprint is current.

## Rollback / forward recovery

Assurance files do not mutate product data. Revert the associated product change through normal version control if valid proof cannot be established. Do not delete the failing evidence merely to hide the gap; artifact retention follows CI policy.

## Escalation

Escalate when the Claim depends on business judgment, unavailable hardware/environment, missing specialist expertise, or an irreversible risk decision. Use an Approval Packet only for the decision/risk acceptance, not for routine test execution.

## Evidence / ownership

- Policy: `ai/policies/assurance.md`
- Active records: `assurance/current/`
- Generated run evidence: `.ai-artifacts/verification/`
- Validator: `scripts/ai/validate-assurance`
