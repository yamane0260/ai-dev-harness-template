---
name: release-change
description: Prepare and execute a safe release with context-efficient evidence handling. Use when merging/releasing/deploying a completed change, especially YELLOW/RED work needing exact-revision verification, rollback readiness, post-deploy checks, and human approval only for remaining real-world consequences.
---

# Release Change

1. Determine the final risk level; never silently lower the deterministic floor.
2. Run `./scripts/ai/verify --risk <level>` on the exact revision intended for release. Read the summary first; do not import raw logs unless a failure needs investigation.
3. Confirm any specialist/independent reviews actually required by the change are complete. Do not create new review ceremony solely because this Skill is running.
4. Confirm staging/dry-run and rollback/forward-recovery evidence where applicable.
5. If a non-automatable human decision remains, use `prepare-approval`. RED irreversible actions require explicit human go/no-go.
6. Release through normal automation without bypassing CI/deployment gates.
7. Run focused post-deploy smoke/health checks and inspect relevant errors/metrics only.
8. Report revision, verification summary path, post-deploy result, rollback status, and residual risk concisely.
