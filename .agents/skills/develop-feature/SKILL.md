---
name: develop-feature
description: Implement product features and behavior changes with context-efficient routing and a targeted Quality Envelope. Use for normal software changes that need the smallest relevant context, observable acceptance criteria, detection of missing quality constraints, risk-aware verification, and specialist review only when genuinely triggered.
---

# Develop Feature

1. Classify **work mode**: MICRO, STANDARD, or CRITICAL. Separately obtain the risk floor with `./scripts/ai/classify-risk` when a diff exists; raise risk if consequences/unknowns justify it.
2. Build a compact Task Packet. Read `ai/context-map.md`; load only the docs/code needed for the touched area.
3. Apply `ai/quality-envelope.md`. For STANDARD/CRITICAL, or a MICRO change touching user workflow, trust/data boundaries, migrations, external I/O, production operations, performance-sensitive paths, personal data, or dependencies, run `spec-gap-preflight` in a small/fresh context when supported.
4. Record the Quality Impact Vector in the Task Packet. Load only docs for domains marked relevant.
5. Add concise positive acceptance criteria plus any material negative/invariant criteria discovered by preflight. Escalate only unresolved business/product decisions; do not invent them.
6. For user-facing UI, classify UI Impact: NONE / COSMETIC / INTERACTION / STRUCTURAL. STRUCTURAL changes require a compact UX Contract from `ai/templates/ux-contract.md` before implementation. Use existing product/platform patterns before inventing interaction patterns.
7. For STANDARD/CRITICAL, delegate broad read-only repository exploration when supported and keep raw results out of the main context.
8. Implement the smallest change using existing patterns. Avoid unrelated refactors, speculative abstractions, and invented requirements/data.
9. Add/update focused tests and checks that prove both requested behavior and relevant invariants/failure behavior. Keep raw logs outside the main context.
10. Run `./scripts/ai/verify --risk <level>` before completion. Invoke `review-security`, `review-ux`, `review-design`, or `review-code` only when their trigger applies. For STRUCTURAL UI, `review-ux` is the primary usability check; `review-design` remains visual/brand QA.
11. Invoke `prepare-approval` only when a non-automatable human decision remains.

Return a concise completion summary: what changed, Quality Impact domains covered, verification result/path, residual risk/unknowns, and any human decision actually required.
