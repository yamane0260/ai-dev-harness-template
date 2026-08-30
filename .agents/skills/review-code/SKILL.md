---
name: review-code
description: Perform an independent evidence-based review of a proposed code change. Use for YELLOW/RED work, before merge of meaningful changes, after a large agent implementation, or whenever a fresh-context reviewer is needed to detect regressions, spec drift, unnecessary complexity, missing tests, and architecture violations.
---

# Review Code

Prefer a fresh agent/subagent/worktree context when the tool supports it.

1. Read the spec/acceptance criteria first, then the complete diff and relevant call sites/tests.
2. Check for: missing criteria, contradictory behavior, unrequested behavior, regressions, unsafe defaults, duplicated abstractions, dependency changes, error-path gaps, and architecture boundary violations.
3. Verify that tests assert behavior rather than merely executing code. Watch for weakened/deleted assertions or excessive mocking that hides the real path.
4. Run focused checks when a finding depends on runtime behavior.
5. Separate actionable findings from preferences. Report severity, evidence, affected path, consequence, and a concrete correction.
6. Do not approve merely because CI is green; compare against the requested behavior and repository policy.
7. If no material findings remain, state what was reviewed and what evidence was used.
