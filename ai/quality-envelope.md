# Quality Envelope

Functional acceptance criteria describe what a change should do. The Quality Envelope detects ways the implementation could satisfy that spec and still be unsafe, confusing, fragile, expensive, unmaintainable, or operationally unreliable.

Apply this as a **router**, not a checklist to load in full. Mark only material domains relevant to the change, then read/test those domains only.

## Quality Impact Vector

Use: `NONE`, `LOW`, `MATERIAL`, or `CRITICAL`.

| Domain | Typical triggers | Relevant source/check |
|---|---|---|
| UX / product appropriateness | settings, navigation, forms, workflows, user-visible behavior | `docs/UX.md`, UX Contract, `review-ux` |
| Security / abuse | auth, permissions, user-controlled input, uploads, external URLs | `docs/SECURITY.md`, `review-security` |
| Data integrity | persistence, duplicates, concurrency, state transitions | architecture/data tests |
| Compatibility / migration | schema/API changes, rolling deploys, stored data | `docs/ARCHITECTURE.md`, `docs/RELIABILITY.md` |
| Reliability / failure modes | network, external services, retries, partial failure | `docs/RELIABILITY.md` |
| Operability / observability | production workflows, async jobs, difficult failures | `docs/RELIABILITY.md`, logs/metrics/traces |
| Performance / cost / quota | lists/search, batch jobs, AI/API/storage usage | project budgets/benchmarks |
| Privacy / data lifecycle | personal/sensitive data, retention, logs | `docs/SECURITY.md` + project policy |
| Architecture / maintainability | cross-layer changes, new abstraction/dependency | `docs/ARCHITECTURE.md`, structural checks |
| Accessibility | meaningful interaction/UI changes | `docs/UX.md`, accessibility checks/task audit |
| Supply chain | new dependency/action/image/tool | dependency verification/scanning |

## Spec-Gap Preflight

Run `spec-gap-preflight` for STANDARD/CRITICAL changes, and for MICRO changes when any high-consequence trigger above applies.

For each relevant domain ask:

> Could this change fully satisfy the written functional spec and still create a material user, production, data, security, cost, or maintainability problem?

Classify each gap as one of:

- **Repository default/policy already resolves it** — no extra context.
- **Implementation constraint** — add to the Task Packet.
- **Testable invariant / negative criterion** — add a focused test/check.
- **Human/product decision** — escalate only if behavior/tradeoff cannot be derived safely.

## Negative / invariant criteria

Where material, define not only what must happen but what must never happen. Examples:

- another user/tenant cannot access or mutate the resource;
- duplicate/retried requests do not create duplicate side effects;
- invalid input does not partially mutate state;
- concurrent updates do not silently lose data;
- old/new versions remain compatible during rollout;
- an external-service timeout has bounded behavior and recovery;
- a critical operation leaves enough evidence to diagnose failure;
- representative data volume stays within the performance/cost budget.

## UI Impact

Classify user-facing changes separately from risk:

- **NONE**: no UI effect.
- **COSMETIC**: visual-only change with unchanged interaction/information architecture.
- **INTERACTION**: controls/forms/states change but overall structure is stable.
- **STRUCTURAL**: new screen, settings/navigation organization, workflow, information hierarchy, or major task flow.

STRUCTURAL requires a compact `ai/templates/ux-contract.md` before build and a `review-ux` task audit after build when a rendered environment is available.

## Keep it context-efficient

- Store the vector/constraints in the Task Packet; do not paste entire domain docs into parent context.
- Use fresh-context specialist review only for MATERIAL/CRITICAL domains.
- Deterministic checks should produce artifacts/summaries rather than raw logs in the main context.
- If every domain is `NONE/LOW`, do not create extra process for ceremony.
