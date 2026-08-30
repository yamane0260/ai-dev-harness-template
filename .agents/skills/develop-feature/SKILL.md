---
name: develop-feature
description: Implement product features and behavior changes with context-efficient routing. Use for normal software changes that need the smallest relevant context, observable acceptance criteria, risk-aware verification, and specialist review only when genuinely triggered.
---

# Develop Feature

1. Classify **work mode**: MICRO, STANDARD, or CRITICAL. Separately obtain the risk floor with `./scripts/ai/classify-risk` when a diff exists; raise risk if consequences/unknowns justify it.
2. Read `ai/context-map.md`. Load only the docs and code needed for the touched area.
3. For MICRO, stay in the current context unless exploration becomes broad. Use concise acceptance criteria in the working notes; do not create a spec file solely for process compliance.
4. For STANDARD/CRITICAL, delegate broad read-only exploration when supported. Ask the explorer for a compact Task Packet using `ai/templates/task-packet.md`; do not import raw search/file dumps into the main context.
5. If requirements are ambiguous in a way that changes user/business behavior, record the open decision. Otherwise use concise observable acceptance criteria and proceed.
6. Implement the smallest change using existing patterns. Avoid unrelated refactors, speculative abstractions, and invented requirements/data.
7. Add/update focused tests where they materially prove the requested behavior. Use deterministic commands directly; keep raw logs outside the main context.
8. Run `./scripts/ai/verify --risk <level>` before completion. Do not invoke `verify-work` merely as another prose workflow step; use it only when an explicit independent verification pass is useful.
9. Invoke `review-security` only for its security-sensitive triggers. Invoke `review-design` only for meaningful user-facing visual changes. Invoke `review-code` for CRITICAL work or when independent fresh-context review is warranted; it is not mandatory ceremony for routine MICRO work.
10. Invoke `prepare-approval` only when a non-automatable human decision remains.

Return a concise completion summary: what changed, verification result/path, residual risk/unknowns, and any human decision actually required.
