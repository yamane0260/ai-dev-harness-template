---
name: explain-system
description: Explain an AI-developed system, change, component, function, or selected line through progressive drill-down, using durable project relationships and the reader's domain-specific familiarity. Use when someone asks how/why code works or needs to take responsibility without reading the original AI session.
---

# Explain System

1. Start at `PROJECT_MAP.md`. Build/read `.ai-artifacts/index/project-index.json` and retrieve only nodes related to the requested system/change/component/path.
2. Read `.harness-user.json` only if it exists locally. Use domain-specific familiarity; do not reduce the reader to a global junior/senior label.
3. Begin at the user's requested zoom level: system, component, change/Claim, concept, function/symbol, or selected line. Expand prerequisites or implementation detail only where needed.
4. State the project role first, then the mechanism, constraints/invariants, likely failure mode, and verifying evidence/Human Check.
5. For "why", distinguish `RECORDED`, `DERIVED`, and `INFERRED`. If historical rationale was not recorded, say so.
6. Never change Claim criticality, Human Check level, security expectations, or release criteria based on familiarity.
7. Do not write a permanent tutorial unless the explanation reveals a reusable project-specific concept or missing readiness knowledge. Otherwise answer on demand.

Return a concise explanation with paths/Claim IDs that let the reader drill one level deeper.
