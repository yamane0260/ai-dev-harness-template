---
name: review-security
description: Review security-sensitive code and data-boundary changes using deterministic scanners plus independent reasoning. Use for authentication, authorization, personal/sensitive data, uploads, external URLs, secrets, dependencies, serialization, database permissions/migrations, payments, or any RED security boundary change.
---

# Review Security

Prefer a reviewer independent from the implementation context.

1. Map trust boundaries and identify attacker/user-controlled inputs.
2. Review authentication and authorization separately. Confirm server-side enforcement and cross-user/cross-tenant denial paths.
3. Review validation, injection, SSRF/external URL access, path handling, file uploads, unsafe deserialization, XSS/output encoding, secrets, and sensitive logging as applicable.
4. Review new/changed dependencies. Verify packages actually exist and use the configured dependency/security scanners.
5. For database changes, examine permissions, destructive behavior, transactionality, migration compatibility, and rollback/forward recovery.
6. Run the configured `security` and `dependency` gates and relevant integration tests. Re-run scanners after fixes.
7. Treat the same agent writing both critical security code and its only tests as insufficient evidence; seek an independent pass or deterministic control.
8. Report residual risk and blocking unknowns explicitly. Do not issue a cosmetic approval when specialist expertise is genuinely required.
