---
name: review-assurance
description: Review whether a non-trivial change's Claims are meaningful and are actually supported by current evidence or explicit Human Checks. Use for STANDARD/CRITICAL assurance records, YELLOW/RED release preparation, or when verification output exists but it is unclear what the tests prove.
---

# Review Assurance

Use a fresh context when supported. Receive the Task Packet/spec, active assurance manifest, human checks, changed diff, and generated `summary.md`, `evidence.json`, and `readiness.json`. Do not receive the original implementation transcript.

1. Validate structure with `./scripts/ai/validate-assurance --manifest <path> --evidence <path>`.
2. Check each Claim is an observable property within a bounded scope, not a restatement of an implementation task.
3. Trace every requirement to at least one Claim and every MUST Claim to meaningful decisive evidence or a Human Check.
4. Inspect whether the named gate/test can actually establish the Claim. A broad passing gate is insufficient when the locator does not exercise the claimed behavior.
5. Keep `AI_REVIEWED`, `MACHINE_VERIFIED`, `HUMAN_REQUIRED`, `HUMAN_VERIFIED`, and `UNVERIFIED` distinct.
6. Confirm a Human Check is used only where automation cannot establish the property, and that its procedure and expected observation are executable by the named audience.
7. Check residual uncertainty and scope exclusions are explicit. Do not infer full-system safety from a narrow Claim.
8. Report only material gaps. Fix manifest wording/relationships when the evidence is sound; add tests/checks when proof is missing; do not weaken the Claim merely to obtain READY.

Return:

- result: `PASS / NEEDS-EVIDENCE / NEEDS-HUMAN-ACTION / INVALID-MAPPING`;
- unsupported or overstated Claim IDs;
- stale/missing evidence;
- exact Human Checks still required;
- minimal correction and whether release is blocked.
