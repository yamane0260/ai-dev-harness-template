# V4 Contract Index

This directory defines the contract-first V4 architecture while the V3 runtime remains authoritative.
The files here are design and interchange sources for the migration and MUST NOT be treated as proof that the V4 runtime already exists.

## Sources

- [`capabilities.md`](capabilities.md) defines the initial capability inventory and the semantic contract for each capability.
- [`migration-map.md`](migration-map.md) maps current V3 files and responsibilities into V4 destinations.
- [`profiles/`](profiles/) contains representative presets that validate the profile model without changing current execution.
- [`../schemas/capability.schema.json`](../schemas/capability.schema.json) defines capability descriptors.
- [`../schemas/plugin-manifest.schema.json`](../schemas/plugin-manifest.schema.json) defines provider metadata, permissions, context policy, composition, lifecycle, and failure semantics.
- [`../schemas/profile.schema.json`](../schemas/profile.schema.json) defines objectives, constraints, understanding requirements, and context budgets.
- [`../schemas/execution-plan.schema.json`](../schemas/execution-plan.schema.json) defines the inspectable output expected from the future profile compiler.

The architecture decision is recorded in [`docs/decisions/2026-09-15-v4-composable-harness-architecture.md`](../../docs/decisions/2026-09-15-v4-composable-harness-architecture.md).

## Design boundary

V4 separates five concerns that are mixed across several V3 workflow documents.

1. **Kernel invariants** are non-negotiable trust and release rules.
2. **Capabilities** state what result or semantic service is required.
3. **Plugins/providers** state how a capability is supplied and under which permissions, context, host, lifecycle, and failure conditions.
4. **Profiles** state optimization objectives and non-negotiable project constraints.
5. **Runtime substrates** store context metrics, evidence, run events, and durable project state without conflating them.

A profile MAY prefer less explanation, fewer advisory reviews, greater autonomy, or a smaller context budget.
A profile MUST NOT remove a capability that became mandatory through the kernel, risk floor, a Claim, Quality Impact, a MUST Human Check, or project policy.

## Contract versioning

Capability IDs are stable semantic names such as `review.security` or `verification.run`.
Each capability carries an integer contract version.
Providers declare the exact capability version they implement.
Breaking changes create a new capability contract version instead of silently changing old provider expectations.

Schemas use their own `schema_version` field because schema evolution and capability evolution are separate concerns.

## Planned runtime flow

```text
request
  -> classify objective + constraints + impacts
  -> resolve host support
  -> compile profile
  -> validate capability/provider dependencies and conflicts
  -> produce execution plan
  -> execute only selected providers
  -> record bounded run events and context metrics
  -> collect exact evidence separately
  -> evaluate assurance and release readiness
```

The execution plan records why each capability was selected or skipped so that composition is inspectable without replaying the original agent conversation.

## Context rule

V4 treats context as a budgeted resource.
The preferred reduction order is `avoid -> isolate -> summarize -> compact`.
Full provider instructions are loaded on demand after selection.
Raw child-agent and tool output should remain outside the parent context unless a capability contract explicitly requires it.

## Migration status

This initial increment is intentionally non-operative.
The current V3 skills, policies, scripts, and CI remain the source of runtime behavior until later phases wrap them as providers, compare shadow plans, and switch execution only after evaluation.
