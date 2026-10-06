# V5 Context Map

Do not load all capsules. Start with the Task Envelope, touched code, and preflight output.

| Trigger | Load |
|---|---|
| auth, permission, secrets, sensitive data, untrusted input | `capsules/security.md` |
| user-facing workflow, forms, navigation, visible states | `capsules/ux.md` |
| schema, migration, persistence, state transition, destructive data operation | `capsules/data.md` |
| network/external service, retry, queue, timeout, production operation | `capsules/reliability.md` |
| cross-layer change, shared abstraction, new dependency, harness/core change | `capsules/architecture.md` |

If a Perspective Scan finding reveals a domain that preflight did not detect, add that capsule and record an escalation in the scan.

Broad repository exploration belongs in the supervisor or an isolated read-only task. Do not paste broad exploration transcripts into the worker context.
