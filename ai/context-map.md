# Context Map

Use this file to decide what to read. **Do not load every project document by default.** Start from the touched paths/behavior and load the smallest applicable set.

| Area / trigger | Read first | Read additionally only if needed |
|---|---|---|
| Copy/docs/comments only | affected file | PRODUCT if meaning/requirements change |
| UI component/layout/style | DESIGN + affected component | PRODUCT for behavior/content intent; ARCHITECTURE only for data boundaries |
| User-visible behavior | PRODUCT/spec + affected code | DESIGN for visual outcome; ARCHITECTURE for cross-layer changes |
| API/service/business logic | relevant spec + affected service | ARCHITECTURE; SECURITY if trust/data boundary changes |
| Auth/permissions/session | SECURITY + affected auth paths | ARCHITECTURE + relevant spec |
| DB/schema/migration | ARCHITECTURE + affected migration/schema | RELIABILITY; SECURITY for permissions/sensitive data |
| External integration/webhook/upload/URL | relevant spec + affected integration | SECURITY; RELIABILITY for retries/failure recovery |
| Deployment/production/observability | RELIABILITY + affected config | ARCHITECTURE; SECURITY if secrets/network boundaries change |
| Harness/policy/CI itself | affected `ai/`, `scripts/ai/`, `.github/` files | risk/quality policy as applicable |

## Exploration rule

For STANDARD/CRITICAL work, broad repository exploration should be delegated to a read-only explorer/subagent when supported **before** the main implementation context becomes large. The explorer should return `ai/templates/task-packet.md`, not raw search transcripts.

If the task is MICRO and the relevant path is already obvious, skip delegated exploration.
