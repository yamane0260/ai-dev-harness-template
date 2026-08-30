---
name: develop-feature
description: Implement a product feature or meaningful behavior change under this repository's agent-led development policy. Use for new features, API/UI behavior changes, data-flow changes, or substantial refactors that need acceptance criteria, risk classification, tests, fresh verification, and evidence-based completion.
---

# Develop Feature

1. Read the applicable product/spec, architecture, security, design, and reliability docs. Read only what the change needs.
2. If acceptance criteria do not exist, write concise observable criteria under `docs/specs/` before implementation. Do not silently invent ambiguous business rules; record an open decision when needed.
3. Run `./scripts/ai/classify-risk` to obtain the deterministic floor. Raise risk if consequences or uncertainty justify it; never silently lower the floor.
4. Plan the smallest implementation that satisfies the criteria. Prefer existing patterns and dependencies.
5. Add or update tests before or alongside the behavior change so the requested behavior is independently observable. For a bug-prone boundary, confirm the new test would fail without the fix when practical.
6. Implement narrowly. Avoid speculative abstractions, unrelated cleanup, invented content/data, and "while here" rewrites.
7. Run the relevant local checks during iteration.
8. Before completion, invoke `verify-work` and obtain independent review when required by risk or consequence.
9. For user-facing visual changes, invoke `review-design`. For security boundaries or sensitive data, invoke `review-security`.
10. If a non-automatable decision remains, invoke `prepare-approval`; otherwise do not create ceremonial human approval work.
