---
name: develop-feature
description: Implement product features and behavior changes with context-efficient routing, a targeted Quality Envelope, Claim-based assurance, and proportional human-legibility records. Use for normal software changes that need the smallest relevant context, observable criteria, missing-quality detection, verification, explicit human checks, and durable understanding without approval ceremony.
---

# Develop Feature

1. Classify **work mode**: MICRO, STANDARD, or CRITICAL. Separately obtain the risk floor with `./scripts/ai/classify-risk` when a diff exists; raise risk only for actual consequences/unknowns.
2. Build a compact Task Packet. Read `ai/context-map.md`; load only docs/code needed for the touched area.
3. Apply `ai/quality-envelope.md`. Run `spec-gap-preflight` only when its triggers apply; record material Quality Impact domains and concise positive + negative/invariant criteria.
4. For STANDARD/CRITICAL or YELLOW/RED work, create an active assurance record from `ai/templates/assurance/`. Map requirements to observable Claims, required deterministic gates, any non-decisive AI review, explicit Human Checks, affected paths/components, and residual uncertainty. MICRO/GREEN/LOW changes may remain an inline Change Record when no material assurance mapping is useful.
5. For user-facing UI, classify UI Impact. STRUCTURAL changes require a compact UX Contract before implementation; use existing product/platform patterns before inventing interaction patterns.
6. For STANDARD/CRITICAL, delegate broad read-only exploration when supported and keep raw results out of the main context.
7. Implement the smallest change using existing patterns. During work, record only non-reconstructable decisions, constraints, invariants, rejected material alternatives, and Claim relationships; do not produce long narration.
8. Add/update focused tests/checks that prove requested behavior and material invariants/failure behavior.
9. Run `./scripts/ai/verify --risk <level> --assurance <manifest>` when an assurance record exists. Invoke security/UX/design/code review only when its trigger applies. An AI review artifact is `AI_REVIEWED`, not `MACHINE_VERIFIED`.
10. Use `review-assurance` for STANDARD/CRITICAL assurance records after evidence exists. Every MUST Claim must be supported or explicitly routed to a completed MUST Human Check before release.
11. Apply `ai/policies/human-legibility.md` after the implementation is stable. Classify Knowledge Impact independently:
   - NONE: no extra record.
   - LOW: short inline Change Record only.
   - MATERIAL/CRITICAL: use `explain-change` to create an evidence-grounded Change Brief; update canonical concept/decision/runbook only if warranted.
12. For MATERIAL/CRITICAL, run `review-legibility` in a fresh context when supported. A CRITICAL blocking readiness gap prevents release. Do not give the reviewer the original implementation transcript.
13. Invoke `prepare-approval` only when a non-automatable human decision remains. Knowledge/readiness documentation is not itself an approval trigger.

Return a concise completion summary: outcome, material Quality Impact, verification/evidence path, assurance readiness, Knowledge Impact + one-sentence knowledge delta + record path if any, residual uncertainty/readiness gaps, and exact Human Checks still required.
