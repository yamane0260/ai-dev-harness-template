---
name: spec-gap-preflight
description: Detect important quality requirements that are absent from a functional specification before implementation. Use for STANDARD/CRITICAL changes and for MICRO changes that touch user workflows, security/data boundaries, migrations, external I/O, performance-sensitive paths, privacy, dependencies, or production operations. Produces a compact Quality Impact Vector and only the missing nonfunctional constraints that materially affect release quality.
---

# Spec Gap Preflight

Prefer a fresh, small context. Read the Task Packet and functional request first; do not explore the whole repository unless needed to resolve a specific uncertainty.

1. Identify only relevant quality domains: UX, security/abuse, data integrity, compatibility/migration, reliability/failure modes, operability/observability, performance/cost/quota, privacy/data lifecycle, architecture/maintainability, accessibility, and supply chain.
2. For each relevant domain, ask: "Could the implementation fully satisfy the written spec and still create a material production/user problem?"
3. Separate missing items into: resolved by repository defaults/policy, implementation constraint, testable invariant, and blocking human decision.
4. Add negative/invariant acceptance criteria where appropriate: what must never happen, cross-user/duplicate/concurrency behavior, failure behavior, compatibility, recovery, or resource limits.
5. Keep the result compact. Do not load domain docs that were classified irrelevant.
6. Escalate only genuinely material gaps. Do not turn every possible quality concern into ceremony.
7. Return a Quality Impact Vector plus the smallest additional constraints needed for implementation and verification.
