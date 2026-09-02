---
name: review-legibility
description: Independently test whether a MATERIAL or CRITICAL software change can be understood, maintained, and recovered from without the original implementation agent or chat history. Use after an evidence-grounded Change Brief is created, especially for new architecture, dependencies, data/recovery mechanisms, security controls, or operational procedures.
---

# Review Legibility

Run this review in a fresh context when supported. Do not read the original implementation transcript.

Inputs should normally be limited to the Change Brief, relevant current docs/decisions/runbooks, changed diff, focused tests, and verification summary.

Ask the **AI Absence Test**:

1. What changed, in project terms?
2. Why is this approach used? Distinguish `RECORDED`, `DERIVED`, and `INFERRED` rationale.
3. What invariants, failure modes, or boundaries must a future maintainer preserve?
4. Where should a maintainer look and what should they change for the most likely next modification?
5. If it fails in production, how can a maintainer detect, diagnose, and recover from it?

Pass only when a fresh maintainer can answer the questions from durable repository evidence without relying on the original agent session.

For `CRITICAL` operational knowledge, require a concrete current runbook when a human may need to intervene during an incident. For reusable technical concepts, prefer one canonical concept document over repeated explanations in many Change Briefs.

Return only:
- result: PASS / NEEDS-DOC-FIX / BLOCKING-READINESS-GAP;
- missing or misleading knowledge, with paths/evidence;
- minimal documentation correction required;
- whether the gap affects release readiness.

Do not turn a documentation/readiness gap into ceremonial human approval. Approval remains a separate policy decision.
