# Context Map

Use this file to decide what to read. **Do not load every project document by default.** Start from touched paths/behavior plus the Quality Impact Vector and Knowledge Impact.

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
| MATERIAL/CRITICAL Knowledge Impact | changed diff + verification summary + relevant current docs | `ai/policies/human-legibility.md`; existing related change/decision/concept/runbook only if needed |
| Harness/policy/CI itself | affected `ai/`, `scripts/ai/`, `.github/` files | risk/quality/human-legibility policy as applicable |

## Exploration rule

For STANDARD/CRITICAL work, delegate broad repository exploration to a read-only explorer when supported **before** the main context becomes large. Return `ai/templates/task-packet.md`, not raw transcripts.

Run `spec-gap-preflight` only when triggered. For Human Legibility, generate records after the implementation is stable from durable evidence; do not import original chat history merely to explain it.

If the task is MICRO and the relevant path is obvious with no material Quality/Knowledge trigger, skip delegated exploration/preflight/review.
