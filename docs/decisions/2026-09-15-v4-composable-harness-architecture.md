# V4 Composable Harness Architecture

Status: proposed architecture contract for the V3 to V4 migration.

This decision defines the target architecture before runtime behavior is migrated.
The current V3 workflow remains authoritative until the migration phases described below are completed and verified.

## Purpose

V4 preserves the existing responsibility-transfer model while changing how development behavior is composed.
The target is a small constitutional kernel plus capability contracts, swappable providers, project and task profiles, host adapters, and explicit runtime substrates for context, evidence, traces, and cost accounting.

The design separates two kinds of input that V3 sometimes handles in the same workflow.
Objectives describe what the project wants to optimize, such as delivery speed, autonomy, human understanding, handoff depth, human attention, and context efficiency.
Constraints describe requirements that optimization cannot weaken, such as the deterministic risk floor, required evidence, security requirements, MUST Human Checks, release policy, and project-specific restrictions.

The profile compiler MUST satisfy constraints first and optimize objectives only among valid compositions.

## Constitutional kernel

The kernel owns invariants that profiles and plugins cannot weaken.
These invariants should be enforced mechanically where practical so that the model-facing kernel stays small.

The initial kernel invariants are:

- do not report successful completion without current-revision support;
- bind decisive evidence to the repository state on which it was produced;
- do not lower the deterministic risk floor without an explicit authorized decision;
- do not allow a profile or provider fallback to remove a required constraint;
- keep `AI_REVIEWED` distinct from `MACHINE_VERIFIED`;
- keep traces distinct from evidence of product correctness;
- block readiness while a required MUST Human Check is incomplete or failed;
- block release on a material blocking unknown;
- do not weaken tests, gates, or requirements merely to obtain a passing result;
- do not invent requirements, dependencies, APIs, commands, rationale, or successful observations;
- fail closed when a required capability has no valid provider;
- treat human and agent conclusions as revisable and resolve material disagreement with discriminating evidence;
- do not persist private chain-of-thought, secrets, full file contents, or unredacted large command output in the run ledger.

## Architectural layers

V4 uses the following layers.

1. The constitutional kernel defines non-negotiable invariants and trust semantics.
2. Capability contracts define what the harness can ask for without naming a concrete tool or model.
3. Plugins or providers implement capability contracts.
4. Host adapters expose what Codex, Claude Code, Cursor, DeepSeek Harness, or a future host can actually provide.
5. Profiles express optimization objectives and project constraints.
6. The profile compiler resolves objectives, constraints, impacts, available providers, and host support into an execution plan.
7. The workflow runtime executes the plan with dependency, ordering, failure, and permission rules.

Four cross-cutting substrates support every layer: the context manager, evidence store, run ledger, and cost/context meter.

## Composition model

The compiler resolves the active composition from:

```text
user request
+ project profile
+ optional preset
+ deterministic risk floor
+ quality impact
+ knowledge impact
+ human understanding requirement
+ host capability report
= execution plan
```

Profiles are presets and policy inputs, not hard-coded workflows.
A `rapid` preset can prefer high autonomy and low explanation overhead, but it cannot disable a review or gate made mandatory by risk, quality impact, a Claim, or project policy.

The execution plan records both selected and skipped capabilities with reasons.
This makes the harness composition inspectable without requiring the original agent conversation.

## Capability and provider boundary

A capability states semantics, inputs, outputs, evidence meaning, and composition requirements.
A provider states how that capability is implemented on a particular runtime.

For example, `review.security@1` is a capability.
`review-security-codex`, `review-security-claude`, and a host-native security reviewer can all implement that same contract.
The consumer requests the capability and should not depend on the concrete provider unless a project constraint explicitly requires one.

Provider fallback is allowed only when the fallback satisfies the same required capability contract and constraints.
A failed required provider must never silently downgrade into an omitted check.

## Context model

Context is a budgeted runtime resource.
The default reduction order is:

```text
avoid loading
-> isolate intermediate work
-> return structured summaries
-> compact old history only when needed
```

Each plugin declares how its instructions, project context, tool output, and child-agent output may enter the parent context.
Discovery should expose catalog metadata first and load full provider instructions only after selection.

The context manager tracks provenance classes such as `POLICY`, `AUTHORITATIVE_PROJECT`, `VERIFIED_ARTIFACT`, `DERIVED`, `AGENT_GENERATED`, and `EXTERNAL_UNTRUSTED`.
External or generated material cannot become kernel policy merely because it appears in context.

## Human understanding

V4 keeps Knowledge Impact and introduces a separate Human Understanding Requirement.
Knowledge Impact asks what durable knowledge future maintainers need if the original session disappears.
Human Understanding Requirement asks what the responsible person must be able to understand or explain for the current delivery.

The initial levels are `NONE`, `WORKING`, `MAINTAINER`, and `EXPLAINABLE`.
An `EXPLAINABLE` requirement should normally cover component responsibility, important data flow, changed areas, failure modes, diagnosis, and likely modification points.
It does not imply line-by-line memorization of the codebase.

## Risk, quality, and verification

Risk remains an independent constraint axis.
Quality Impact remains a routing input.
Knowledge Impact remains a durable-knowledge input.
The V3 Work Mode classification is demoted from a top-level workflow selector to a derived execution-cost hint.

The fixed V3 risk gate bundles are a migration target rather than a permanent V4 rule.
The V4 target computes required gates from:

```text
minimum baseline for risk
+ material quality-impact requirements
+ Claim-specific evidence requirements
+ project policy
```

This preserves a risk floor while avoiding unrelated gates when they add no evidence for the current change.

## Runtime records

The run ledger records what the harness executed.
The evidence store records observations that can support Claims.
Durable project knowledge records facts, decisions, invariants, failure modes, and recovery knowledge for later maintainers.
These records answer different questions and remain separate.

A V4 run should record the repository revision plus a composition identity derived from the kernel version, compiler version, profile, capability versions, provider versions, and host adapter version.
This composition identity prevents two materially different harness configurations from appearing equivalent merely because they ran on the same source commit.

## Provider permissions and lifecycle

Every provider declares file, shell, network, credential, git-push, deployment, and external-side-effect permissions.
The host adapter reports which declarations it can actually enforce.
Partial enforcement must be reported rather than presented as complete isolation.

Temporary provider state should be reversible when practical.
Providers that create worktrees, temporary configuration, local services, environment overrides, or transient installations must define teardown behavior or explicitly declare persistent state.

## Failure semantics

Every provider declares one of the supported failure modes: `block`, `fallback`, `retry`, or `advisory`.
Fallback targets are explicit and must satisfy the same required capability and constraints.
Retry limits are bounded.
A required capability with no valid provider makes the execution plan invalid or blocks execution.

## Migration strategy

V4 is introduced without a big-bang rewrite.

1. Define contracts, schemas, presets, and the migration map while V3 remains authoritative.
2. Wrap existing V3 skills and scripts as candidate V4 providers without changing their internal behavior.
3. Add a shadow profile compiler that reports the composition V4 would choose while V3 still executes the task.
4. Compare V3 routing with V4 composition on reference tasks and fix unsafe or wasteful differences.
5. Switch `develop-feature` into a thin adapter that executes a compiled plan.
6. Add progressive disclosure, bounded parent outputs, context metrics, and isolated child work where host support exists.
7. Split monolithic executors such as `scripts/ai/verify` into capability providers after behavior is covered by contract tests.
8. Remove legacy routing only after V4 preserves or improves quality while reducing context and human overhead on the evaluation suite.

## Decision

V4 will evolve the repository from an instruction-oriented workflow into a composition-oriented harness.
V3 assurance, mutual-verification, quality, and human-legibility semantics remain source material for V4 rather than being discarded.
The first implementation increment is contract-first and non-operative: it adds the V4 architecture, capability inventory, schemas, presets, and migration map without changing the current V3 execution path.
