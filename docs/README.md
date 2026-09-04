# Documentation Map

Use `../PROJECT_MAP.md` as the repository-wide starting point.

## Current sources

- `PRODUCT.md`: problem, users, outcomes, and product constraints.
- `ARCHITECTURE.md`: current components, dependencies, and data boundaries.
- `SECURITY.md`: current trust boundaries and security invariants.
- `DESIGN.md`: visual system and design constraints.
- `UX.md`: interaction, information architecture, and accessibility.
- `RELIABILITY.md`: failure handling, observability, and recovery expectations.
- `specs/`: feature-specific requirements too large for a task or PR record.
- `concepts/`: reusable project-specific concepts.
- `decisions/`: durable choices and their recorded tradeoffs.
- `runbooks/`: current procedures for maintenance or incidents.

## Historical source

- `changes/`: concise, evidence-grounded briefs for MATERIAL/CRITICAL changes. These explain history; current behavior still belongs in the current sources above.

## What does not belong here

- Raw verification logs, screenshots, agent transcripts, and tool traces belong in `.ai-artifacts/`.
- Claim status and required human testing belong in `../assurance/`.
- Generic framework tutorials should be linked, not copied.
