# Assurance Policy

The harness does not ask whether an AI-generated change is trustworthy in the abstract. It records separate, inspectable grounds for responsibility transfer.

## Model

For non-trivial changes, use this chain:

```text
Requirement -> Claim -> Evidence requirement -> Exact-run evidence
                         -> Human Check
Claim -> affected path/component
Claim -> decision/concept/runbook
```

The committed manifest records the relationships and expected proof. `scripts/ai/verify` records what actually ran. `scripts/ai/validate-assurance` joins the two and calculates readiness.

## Evidence classes

- `MACHINE_VERIFIED`: a declared deterministic gate passed on the current repository state.
- `AI_REVIEWED`: an evidence-grounded AI review artifact exists. This is useful scrutiny, not independent machine proof.
- `HUMAN_REQUIRED`: a linked check requires human judgment or observation and is not complete.
- `HUMAN_VERIFIED`: the linked human check records performer, time, procedure/result evidence, and a passing result.
- `UNVERIFIED`: required support is missing, failed, stale, or not applicable without an accepted reason.
- `N/A`: a domain/check is not applicable and has an explicit reason. N/A never silently satisfies a declared required gate.

Do not collapse these into one confidence score. A Claim can simultaneously have machine evidence and require a human check.

## Claim rules

1. Claims must be observable properties, not task names such as "implement authentication."
2. `must` Claims block release when their required gate evidence is not current or a linked MUST Human Check is not passed.
3. A `must` Claim needs at least one decisive basis: current machine evidence or a passed human check. `AI_REVIEWED` alone is never decisive.
4. Evidence requirements name a configured gate and, where possible, a focused test/check locator. A broad gate without a meaningful Claim relationship is weak evidence.
5. Residual uncertainty is explicit. Use `none` only when no material known uncertainty remains within the Claim's stated scope.
6. N/A requires a reason and should normally remove or revise the inapplicable Claim instead of being used as a release shortcut.

## Human checks

- `MUST`: incomplete or failed blocks release.
- `SHOULD`: strongly recommended; an incomplete check is visible but does not automatically block.
- `OPTIONAL`: situational confirmation.
- `NONE`: do not create a placeholder check.

Human checks state why automation is insufficient, a bounded procedure, and the expected observation. A passed check records who performed it, when, and what evidence/result was observed. Familiarity profiles never change the level.

## Exact-revision evidence

Generated evidence records the HEAD commit, whether the tree was dirty, a working-tree fingerprint, command, result, exit code, log path/hash, and execution environment. Evidence is stale when the repository fingerprint differs.

Raw evidence is audit material. Keep it out of Git and normal model context; retrieve only the summary or targeted failing log.

## Release readiness

`READY` means every MUST Claim has its required current gate evidence, required AI review artifacts exist, every linked MUST Human Check passed, and no blocking validation error remains.

`ACTION_REQUIRED` means human work is pending. `BLOCKED` means evidence failed, is missing/stale, a MUST Human Check failed, or the manifest is invalid.

Readiness applies only to the declared Claims and scope. It is not a claim that the system is correct in every possible condition.
