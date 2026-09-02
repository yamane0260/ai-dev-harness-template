# Context Map

Use this file to decide what to read. **Do not load every project document by default.** Start from touched paths/behavior plus the Quality Impact Vector in `ai/quality-envelope.md`.

| Area / trigger | Read first | Read additionally only if relevant |
|---|---|---|
| Copy/docs/comments only | affected file | PRODUCT if meaning/requirements change |
| Cosmetic UI | DESIGN + affected component | UX only if interaction meaning changes |
| Settings/navigation/forms/workflow | UX + affected UI | PRODUCT/spec; DESIGN for visual expression |
| User-visible behavior | PRODUCT/spec + affected code | UX; DESIGN; ARCHITECTURE for cross-layer changes |
| API/service/business logic | relevant spec + affected service | ARCHITECTURE; SECURITY for trust/data boundaries; RELIABILITY for failure modes |
| Auth/permissions/session | SECURITY + affected auth paths | ARCHITECTURE + relevant spec |
| DB/schema/migration/persistence | ARCHITECTURE + affected migration/schema | RELIABILITY for rollout/recovery; SECURITY for permissions/sensitive data |
| External integration/webhook/upload/URL | relevant spec + affected integration | SECURITY; RELIABILITY; operability evidence |
| Performance/cost-sensitive path | affected path + project benchmark/budget | ARCHITECTURE if redesign is required |
| Personal/sensitive data | SECURITY + affected path | data lifecycle/retention policy as applicable |
| New dependency/tool/action/image | affected manifest/config | SECURITY + supply-chain checks |
| Deployment/production/observability | RELIABILITY + affected config | ARCHITECTURE; SECURITY for secrets/network boundaries |
| Harness/policy/CI itself | affected `ai/`, `scripts/ai/`, `.github/` files | risk/quality policy as applicable |

## Exploration rule

For STANDARD/CRITICAL work, broad repository exploration should be delegated to a read-only explorer/subagent when supported **before** the main implementation context becomes large. The explorer should return `ai/templates/task-packet.md`, not raw search transcripts.

Run `spec-gap-preflight` in a small/fresh context when its triggers apply. It should return only relevant domains and missing constraints, not a general quality essay.

If the task is MICRO and the relevant path is obvious with no material Quality Envelope trigger, skip delegated exploration/preflight.
