---
name: review-code
description: Independently review a meaningful or high-consequence code change using a compact task packet and diff. Use for CRITICAL work, large/uncertain STANDARD changes, or when fresh-context review is likely to catch regressions, spec drift, missing tests, or unnecessary complexity.
---

# Review Code

Prefer a fresh context. Start with the Task Packet, acceptance criteria, diff/changed paths, and verification summary. Do not read the whole repository or all docs by default.

1. Check requested behavior vs implementation: missing, contradictory, or unrequested behavior.
2. Check regressions, unsafe defaults, error paths, unnecessary abstraction, dependency changes, and architecture violations only where relevant to the diff.
3. Inspect nearby call sites/tests only when needed to validate a concrete concern.
4. Run focused checks only when a finding depends on runtime behavior.
5. Report actionable findings with severity, evidence, consequence, and correction. Separate them from preferences.
6. If no material findings remain, state the evidence reviewed in a few lines.
