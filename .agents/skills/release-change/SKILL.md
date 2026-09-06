---
name: release-change
description: Prepare and execute a safe release with context-efficient evidence handling and human-readiness checks. Use when merging/releasing/deploying a completed change, especially YELLOW/RED work needing exact-revision verification, rollback readiness, post-deploy checks, and human approval only for remaining real-world consequences.
---

# Release Change

1. Determine final risk; never silently lower the deterministic floor.
2. Complete and record any required Human Checks on the stable tracked state, then run `./scripts/ai/verify --risk <level> --assurance <manifest>` on that exact revision for YELLOW/RED or STANDARD/CRITICAL work. Read `summary.md` and `evidence.json` first; import raw logs only for targeted failures.
3. Create any declared `ai-review-record` against that evidence. Then run `./scripts/ai/validate-assurance --manifest <manifest> --evidence <the-reviewed-evidence.json> --release`, carrying `--agent-trace-summary <validated-summary.json>` when the manifest requires it. Do not rerun `verify` between review and release evaluation because it creates a different verification run. A later tracked Human Check or documentation correction must restart this step from verification. Confirm every MUST Claim has current decisive evidence, required structured review records pass integrity checks without being mislabeled as machine proof, every required Agent Trace event is present, and every MUST Human Check is passed. `ACTION_REQUIRED` or `BLOCKED` prevents release.
4. Confirm specialist reviews actually required by Quality/Risk are complete; do not create review ceremony solely because this Skill is running.
5. Confirm Human Legibility requirements are complete. MATERIAL changes need a Change Brief and fresh legibility pass when supported. CRITICAL operational changes need applicable current runbooks; `BLOCKING-READINESS-GAP` prevents release.
6. Confirm staging/dry-run and rollback/forward-recovery evidence where applicable.
7. If a non-automatable human decision remains, use `prepare-approval`. RED irreversible actions require explicit human go/no-go. Do not ask for approval merely because a technology is unfamiliar.
8. Release through normal automation without bypassing CI/deployment gates.
9. Run focused post-deploy smoke/health checks and inspect relevant errors/metrics only.
10. Report revision, verification/evidence path, assurance readiness, post-deploy result, Knowledge Impact/readiness status, rollback status, and residual risk concisely.

## Mutual verification

Read `ai/policies/mutual-verification.md` when applying this workflow.
Preserve and investigate material disagreements from either humans or agents.
Correction is not restricted to explanation: requirements, implementation and
test expectations remain revisable.
Required review results use the structured review-record contract.
