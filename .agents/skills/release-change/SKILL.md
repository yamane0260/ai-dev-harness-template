---
name: release-change
description: Prepare and execute a safe release or deployment after implementation. Use when merging/releasing/deploying a completed change, especially YELLOW/RED work that needs fresh verification, rollback readiness, post-deploy checks, and human approval only for remaining real-world consequences.
---

# Release Change

1. Determine the final risk level; never silently lower the deterministic floor.
2. Run `verify-work` on the exact revision intended for release.
3. Confirm required independent reviews are complete for the risk/surface.
4. Confirm staging/dry-run evidence where applicable.
5. Confirm rollback or forward-recovery steps are concrete and executable enough for the risk.
6. If human judgment remains, generate and validate a No-Guess Approval Packet with `prepare-approval`. RED irreversible actions require an explicit human go/no-go.
7. Release through the project's normal automation; do not bypass CI/deployment gates.
8. Run post-deploy smoke/health checks and inspect relevant logs/metrics/errors.
9. If the release creates material new errors or violates acceptance criteria, stop rollout and execute the documented rollback/recovery path.
10. Report the released revision, verification evidence, post-deploy result, and any residual risk.
