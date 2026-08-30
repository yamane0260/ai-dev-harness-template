---
name: debug-systematically
description: Diagnose and fix a defect without guess-and-patch iteration. Use for test failures, production/staging bugs, intermittent issues, regressions, performance anomalies, and any situation where the root cause is not already proven.
---

# Debug Systematically

1. Reproduce the failure or collect the closest available objective evidence (test, log, trace, screenshot, metric, request/response).
2. Define the expected and observed behavior precisely.
3. Narrow the failing boundary before editing: input, state, dependency, network, persistence, concurrency, rendering, or configuration.
4. Form one or more explicit hypotheses and identify evidence that would distinguish them.
5. Inspect/instrument only enough to test the hypotheses. Avoid broad speculative rewrites.
6. Fix the proven root cause with the smallest safe change.
7. Add a regression test or durable detector when practical.
8. Run the relevant risk-level verification using `verify-work`.
9. Record any remaining uncertainty; do not translate "could not reproduce" into "fixed".
