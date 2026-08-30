---
name: verify-work
description: Verify that current code changes are actually complete and safe enough for their risk level. Use before claiming a task is fixed/done, before opening or updating a PR, after review fixes, and before release. Requires fresh command evidence rather than confidence or prior test results.
---

# Verify Work

1. Determine the risk floor with `./scripts/ai/classify-risk`; raise it if the change has higher real-world consequences or unresolved uncertainty.
2. Run `./scripts/ai/verify --risk <level>` against the current revision.
3. Inspect failed logs. Fix root causes; do not delete/weaken checks merely to obtain green status.
4. Re-run verification after any change that could invalidate previous evidence.
5. Compare the result to the acceptance criteria/spec. Passing tests does not prove that the requested behavior was the right behavior or that unrequested behavior was not added.
6. Report the exact verification summary path and any N/A gates with their reasons.
7. Do not claim completion if a required gate is failing, unconfigured, stale, or a blocking unknown remains.
