---
name: review-security
description: Independently review security-sensitive changes with minimal relevant context plus deterministic evidence. Use for authentication, authorization, sensitive data, uploads, external URLs, secrets, dependencies, database permissions/migrations, payments, or other RED security-boundary changes.
---

# Review Security

Use a fresh context when supported. Start from the Task Packet, security-relevant diff, `docs/SECURITY.md` only when applicable, and current scanner/test summaries.

1. Identify only the trust boundaries and attacker-controlled inputs affected by the change.
2. Check authn/authz, validation/injection, external URL/file handling, secrets/logging, dependencies, and DB permissions/migrations as applicable; do not run an irrelevant full checklist.
3. Inspect targeted surrounding code only when needed to prove or reject a concern.
4. Use configured security/dependency/integration checks; re-run after fixes when evidence changed.
5. Treat same-agent critical code plus its only tests as insufficient evidence when an independent control is practical.
6. Return material findings, residual risk, and blocking unknowns concisely. Escalate genuinely specialist questions rather than asking for cosmetic human approval.
