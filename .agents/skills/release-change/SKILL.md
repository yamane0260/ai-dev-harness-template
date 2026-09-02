---
name: release-change
description: Prepare and execute a safe release with context-efficient evidence handling and human-readiness checks. Use when merging/releasing/deploying a completed change, especially YELLOW/RED work needing exact-revision verification, rollback readiness, post-deploy checks, and human approval only for remaining real-world consequences.
---

# Release Change

1. Determine final risk; never silently lower the deterministic floor.
2. Run `./scripts/ai/verify --risk <level>` on the exact revision. Read the summary first; import raw logs only for targeted failures.
3. Confirm specialist reviews actually required by Quality/Risk are complete; do not create review ceremony solely because this Skill is running.
4. Confirm Human Legibility requirements are complete. MATERIAL changes need a Change Brief and fresh legibility pass when supported. CRITICAL operational changes need applicable current runbooks; `BLOCKING-READINESS-GAP` prevents release.
5. Confirm staging/dry-run and rollback/forward-recovery evidence where applicable.
6. If a non-automatable human decision remains, use `prepare-approval`. RED irreversible actions require explicit human go/no-go. Do not ask for approval merely because a technology is unfamiliar.
7. Release through normal automation without bypassing CI/deployment gates.
8. Run focused post-deploy smoke/health checks and inspect relevant errors/metrics only.
9. Report revision, verification summary, post-deploy result, Knowledge Impact/readiness status, rollback status, and residual risk concisely.
