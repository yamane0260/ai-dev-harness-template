# V4 Capability Inventory and Contracts

This document defines the initial semantic capability set for V4.
A capability describes the result the harness needs without naming a concrete model, tool, or host.
Providers implement these contracts.

## Contract conventions

Each capability has:

- **ID**: stable semantic name;
- **version**: integer contract version;
- **purpose**: responsibility owned by the capability;
- **inputs**: required or optional structured inputs;
- **outputs**: structured results returned to the runtime;
- **selection**: conditions that make the capability required or useful;
- **evidence semantics**: whether the output is decisive evidence, advisory review, durable knowledge, routing state, or audit state;
- **context rule**: what may enter the parent model context;
- **failure rule**: default runtime treatment when no provider succeeds.

A capability contract does not prescribe the provider implementation.

## Core composition capabilities

### `profile.resolve@1`

**Purpose**

Compile request intent, project profile, kernel constraints, impacts, and host support into an inspectable execution plan.

**Inputs**

- user request summary;
- project profile;
- optional preset;
- deterministic risk floor;
- Quality Impact state;
- Knowledge Impact state;
- Human Understanding Requirement;
- host capability report;
- available provider manifests.

**Outputs**

- execution plan;
- selected providers with reasons;
- skipped capabilities with reasons;
- unresolved dependency/conflict errors;
- effective context budget;
- composition identity inputs.

**Selection**

Required for every V4 task.

**Evidence semantics**

Routing state only.
It is not evidence that implementation is correct.

**Context rule**

The compiler should operate primarily on structured metadata and should not require full provider instructions.

**Failure rule**

`block`.
An invalid composition must not execute.

### `risk.floor@1`

**Purpose**

Calculate a deterministic minimum risk classification from the current repository change.

**Inputs**

- base revision;
- current revision;
- working-tree state when applicable;
- changed paths and diff.

**Outputs**

- `GREEN`, `YELLOW`, or `RED` floor;
- machine-readable reasons;
- classifier version.

**Selection**

Required for non-empty code or harness changes.

**Evidence semantics**

Constraint state.
It sets a floor but does not prove correctness.

**Context rule**

Return the classification and concise reasons.
Do not return the full diff unless another selected capability requires it.

**Failure rule**

`block` for release-oriented work.

### `context.select@1`

**Purpose**

Select the smallest authoritative project context needed by the active execution plan.

**Inputs**

- execution plan;
- project index or repository metadata;
- changed paths;
- capability context requirements;
- context budget.

**Outputs**

- selected context references;
- provenance class per reference;
- exclusion reasons for high-cost candidates when useful;
- estimated parent-context cost.

**Selection**

Required when project-local context is needed beyond the request and changed files.

**Evidence semantics**

Routing state only.

**Context rule**

This capability exists to prevent broad eager loading.
The result is a bounded reference set, not copied document bodies.

**Failure rule**

`fallback` to a conservative bounded selector when available, otherwise `block` if required project authority cannot be located.

## Development capabilities

### `project.explore@1`

**Purpose**

Explore the repository to identify relevant components, likely change points, tests, constraints, and unknowns.

**Inputs**

- task summary;
- selected project context references;
- changed paths if work is already in progress;
- exploration budget.

**Outputs**

- relevant files or symbols;
- component summary;
- likely modification points;
- relevant tests and commands;
- important unknowns;
- optional structured Task Packet.

**Selection**

Useful for unfamiliar, cross-cutting, or non-trivial work.
May be skipped for obvious local changes.

**Evidence semantics**

Derived routing and planning information.
It is not proof of product behavior.

**Context rule**

Broad reads should occur in isolated execution when supported.
The parent receives a structured bounded result rather than raw transcripts.

**Failure rule**

`fallback` to local bounded exploration when available.

### `quality.preflight@1`

**Purpose**

Identify missing requirements, negative criteria, quality risks, or system constraints that can make a change unacceptable even when the explicit functional request appears satisfied.

**Inputs**

- task summary;
- relevant requirements;
- changed surface;
- Quality Impact state;
- project quality policies.

**Outputs**

- material quality concerns by domain;
- required negative or invariant criteria;
- unresolved specification gaps;
- recommended capability escalations.

**Selection**

Required when a material Quality Impact or specification ambiguity is detected.
Optional for obvious low-impact work.

**Evidence semantics**

Advisory planning state unless a project policy promotes a finding into a blocking constraint.

**Context rule**

Load only impacted quality-domain guidance.

**Failure rule**

`block` when the task contains a blocking specification gap; otherwise `advisory`.

### `change.implement@1`

**Purpose**

Produce the requested repository change within the compiled constraints.

**Inputs**

- execution plan;
- bounded task context;
- acceptance criteria;
- active constraints;
- approved modification scope.

**Outputs**

- changed paths;
- implementation summary;
- new or changed tests;
- discovered risk or quality escalations;
- unresolved implementation unknowns.

**Selection**

Required for implementation tasks.

**Evidence semantics**

Implementation output only.
A successful provider response does not establish correctness.

**Context rule**

Provider context should contain only the selected instructions, task context, and necessary repository material.

**Failure rule**

`block`.

### `debug.diagnose@1`

**Purpose**

Diagnose a failure with discriminating observations and identify the smallest supported cause or next experiment.

**Inputs**

- observed failure;
- relevant code and configuration;
- targeted logs or evidence;
- known recent changes.

**Outputs**

- supported hypotheses;
- observations that distinguish them;
- probable cause when evidence supports it;
- proposed fix or next diagnostic step;
- residual uncertainty.

**Selection**

Required for explicit debugging tasks or when verification fails unexpectedly.

**Evidence semantics**

Derived diagnosis.
The diagnosis becomes decisive only when supported by discriminating evidence.

**Context rule**

Read targeted failure sections and avoid wholesale raw logs.

**Failure rule**

`advisory` unless diagnosis is required for a release-blocking failure.

## Verification and review capabilities

### `verification.run@1`

**Purpose**

Execute deterministic gates and record exact-revision machine evidence.

**Inputs**

- repository revision and working-tree fingerprint;
- required gate set;
- project command configuration;
- execution environment metadata.

**Outputs**

- gate results;
- machine-readable evidence record;
- artifact references and hashes;
- verification summary.

**Selection**

Required whenever the kernel, risk baseline, Quality Impact, Claim, or project policy requires machine verification.

**Evidence semantics**

`MACHINE_VERIFIED` only for Claims whose declared evidence requirements are actually satisfied by the current evidence.

**Context rule**

Return summaries and references first.
Raw logs remain outside normal model context.

**Failure rule**

`block` when any required gate fails, is stale, or is unconfigured without an accepted N/A reason.

### `review.verification@1`

**Purpose**

Perform an independent fresh-context check of whether current evidence and implementation support the requested outcome.

**Inputs**

- Task Packet;
- changed paths or diff;
- acceptance criteria;
- verification summary;
- Claim/Evidence relationships when present.

**Outputs**

- material findings;
- unsupported or contradicted Claims;
- residual uncertainty;
- Human Checks that remain necessary.

**Selection**

Useful for critical, suspicious, or pre-release work.

**Evidence semantics**

`AI_REVIEWED` or equivalent advisory review state.
Never decisive machine proof by itself.

**Context rule**

Prefer a fresh isolated context and targeted artifacts.

**Failure rule**

`block` only when the execution plan marks this review as required.

### `review.code@1`

**Purpose**

Review implementation quality, correctness risks, maintainability, and unintended behavior.

**Inputs**

- task and acceptance criteria;
- diff or changed paths;
- relevant architecture context;
- verification summary.

**Outputs**

- structured findings with severity;
- affected paths or symbols;
- residual uncertainty;
- verdict.

**Selection**

Triggered by change complexity, criticality, project policy, or explicit request.

**Evidence semantics**

Advisory AI review unless a project policy defines a different human review source.

**Context rule**

Review only relevant files plus bounded supporting context.

**Failure rule**

`block` if required; otherwise `advisory`.

### `review.security@1`

**Purpose**

Review security-relevant behavior and identify exploitable or policy-breaking conditions.

**Inputs**

- changed security surface;
- security requirements;
- diff or changed paths;
- verification evidence;
- relevant threat or data-flow context.

**Outputs**

- structured security findings;
- affected assets and paths;
- exploit or failure conditions when supportable;
- residual uncertainty;
- verdict.

**Selection**

Required when security, authentication, authorization, sensitive data, production control, or project policy makes the domain material.

**Evidence semantics**

AI review unless paired with deterministic security evidence.

**Context rule**

Load only relevant security policies and affected flows.

**Failure rule**

`block` when required.

### `review.ux@1`

**Purpose**

Review user interaction, discoverability, state transitions, accessibility-relevant interaction, error handling, and consistency with the UX contract.

**Inputs**

- user-facing change surface;
- UX requirements or contract;
- screenshots or runtime observations when available;
- changed paths;
- relevant Human Checks.

**Outputs**

- structured UX findings;
- interaction risks;
- required human or real-device observations;
- verdict.

**Selection**

Triggered by material user-facing behavior or explicit UX requirements.

**Evidence semantics**

Advisory AI review plus explicit Human Checks for observations automation cannot establish.

**Context rule**

Load UX guidance only for user-facing work.

**Failure rule**

`block` if required by policy or Claim; otherwise `advisory`.

### `review.design@1`

**Purpose**

Review visual and product-design consistency when design quality is material.

**Inputs**

- design requirements;
- screenshots or visual artifacts;
- changed UI surface;
- relevant project design guidance.

**Outputs**

- structured design findings;
- consistency and accessibility concerns;
- unresolved subjective tradeoffs.

**Selection**

Triggered by material visual design changes or explicit project policy.

**Evidence semantics**

Advisory review.

**Context rule**

Load design guidance only when selected.

**Failure rule**

`block` if explicitly required; otherwise `advisory`.

## Assurance and human-decision capabilities

### `assurance.evaluate@1`

**Purpose**

Evaluate Claim, Evidence Requirement, AI review, Human Check, and uncertainty relationships and calculate scoped readiness.

**Inputs**

- assurance manifest;
- exact-revision evidence;
- structured review records;
- Human Check records;
- current repository fingerprint.

**Outputs**

- readiness state;
- unsupported or stale Claims;
- pending human work;
- blocking validation errors;
- scoped uncertainty summary.

**Selection**

Required whenever an assurance manifest or release policy requires Claim-based readiness.

**Evidence semantics**

Readiness calculation over declared Claims.
It does not claim universal system correctness.

**Context rule**

Operate on structured records and references rather than raw logs.

**Failure rule**

`block` for release evaluation.

### `human.approval.prepare@1`

**Purpose**

Prepare a bounded decision packet only when a genuine non-automatable human judgment remains.

**Inputs**

- exact decision required;
- relevant evidence and uncertainty;
- user or business consequences;
- alternatives;
- rollback or recovery information.

**Outputs**

- validated approval packet;
- required expertise statement;
- decision options;
- strongest argument against the recommended option.

**Selection**

Only when a real human decision remains after technical verification.

**Evidence semantics**

Decision support, not technical proof.

**Context rule**

Use concise summaries and evidence references.

**Failure rule**

`block` if the release policy requires approval.

### `release.evaluate@1`

**Purpose**

Evaluate whether all release constraints for the scoped change are satisfied.

**Inputs**

- risk state;
- required capabilities and results;
- assurance readiness;
- required Human Checks;
- required approval state;
- rollback/recovery requirements.

**Outputs**

- `READY`, `ACTION_REQUIRED`, or `BLOCKED`;
- blocking reasons;
- pending actions.

**Selection**

Required for release-oriented flows.

**Evidence semantics**

Scoped release state only.

**Context rule**

Use structured summaries and references.

**Failure rule**

`block`.

## Knowledge and understanding capabilities

### `knowledge.explain-change@1`

**Purpose**

Generate a durable explanation of a material change from observable repository evidence.

**Inputs**

- diff and changed paths;
- verification summary;
- recorded decisions;
- relevant current docs;
- rationale provenance.

**Outputs**

- Change Brief or compact Change Record;
- affected components;
- invariants and failure modes;
- modification and diagnosis guidance;
- rationale labels `RECORDED`, `DERIVED`, or `INFERRED`.

**Selection**

Triggered by Knowledge Impact, Human Understanding Requirement, project handoff policy, or explicit request.

**Evidence semantics**

Durable knowledge, not proof of correctness.

**Context rule**

Generate from evidence references instead of copying raw transcripts.

**Failure rule**

`block` only when durable explanation is a release constraint.

### `knowledge.explain-system@1`

**Purpose**

Explain the current system at a requested zoom level using project-authoritative sources and derived relationships.

**Inputs**

- user question;
- project index;
- relevant canonical docs;
- optional familiarity preferences.

**Outputs**

- reader-appropriate explanation;
- source references;
- unresolved uncertainty.

**Selection**

On demand or when Human Understanding Requirement needs broader system context.

**Evidence semantics**

Explanation only.

**Context rule**

Use progressive drill-down and load only needed sources.

**Failure rule**

`advisory`.

### `knowledge.legibility@1`

**Purpose**

Perform the AI Absence Test in a fresh context and determine whether a maintainer can understand and operate the change without the original conversation.

**Inputs**

- durable docs;
- assurance state;
- project map/index;
- relevant code and runbooks;
- Knowledge Impact.

**Outputs**

- legibility findings;
- missing durable knowledge;
- diagnosis or recovery gaps;
- verdict.

**Selection**

Required for configured MATERIAL or CRITICAL Knowledge Impact or handoff constraints.

**Evidence semantics**

Independent legibility review.

**Context rule**

Fresh context is preferred or required by the plan.
The original task transcript should not be provided.

**Failure rule**

`block` when the plan makes legibility a release constraint.

## Project and runtime-support capabilities

### `project.index@1`

**Purpose**

Derive a machine-readable relationship graph from authoritative docs, assurance records, and project structure.

**Inputs**

- project docs;
- assurance records;
- repository metadata.

**Outputs**

- project index artifact;
- source references;
- derivation version.

**Selection**

On bootstrap, after material structural change, or on demand.

**Evidence semantics**

Derived index only.
It is never the source of truth.

**Context rule**

Store the full index outside normal context and query targeted portions.

**Failure rule**

`advisory` unless another required capability depends on it.

### `subagent.delegate@1`

**Purpose**

Run self-contained work in an isolated child context and return a bounded result to the parent.

**Inputs**

- child task;
- allowed tools and permissions;
- context budget;
- output schema;
- continuation policy.

**Outputs**

- structured child result;
- child run reference;
- child context/cost metrics;
- failure state.

**Selection**

Useful for broad exploration, independent review, or other work that would pollute the parent context.

**Evidence semantics**

Depends on the delegated capability.
Subagent existence itself is not evidence of correctness.

**Context rule**

Raw child reasoning and tool activity do not enter the parent context.

**Failure rule**

Inherited from the delegated capability.

### `context.compact@1`

**Purpose**

Condense older model-visible history after avoidance and isolation are insufficient.

**Inputs**

- active model context pressure;
- protected recent context;
- provenance-aware history;
- compaction policy.

**Outputs**

- compacted checkpoint;
- retained range;
- estimated tokens removed;
- compaction event.

**Selection**

Triggered by configured pressure or explicit request.

**Evidence semantics**

Runtime context state only.

**Context rule**

Compaction must not be used as a substitute for loading fewer irrelevant instructions and artifacts.

**Failure rule**

`fallback` to un-compacted execution while within model limits; `block` only when the task cannot continue within context limits.

### `trace.capture@1`

**Purpose**

Capture sanitized host/tool action metadata and coverage without representing traces as product proof.

**Inputs**

- host events;
- declared observation coverage;
- redaction policy.

**Outputs**

- append-only sanitized run events;
- trace coverage summary;
- validation errors.

**Selection**

Enabled when the host can expose useful events and project policy requests traceability.

**Evidence semantics**

Audit state only.

**Context rule**

Trace artifacts remain outside normal model context unless targeted investigation requires them.

**Failure rule**

`advisory` unless trace coverage is an explicit project constraint.

## Initial selection rules

The first profile compiler should implement conservative rules before attempting cost-based optimization.

- Kernel-required capabilities are always selected.
- A deterministic risk floor can add capabilities but cannot remove them.
- Material Quality Impact selects the corresponding specialist capability or requires an explicit supported N/A reason.
- Claims add the capabilities needed to satisfy declared evidence requirements.
- Knowledge Impact controls durable knowledge requirements.
- Human Understanding Requirement controls how much current-delivery explanation and walkthrough is required.
- Objectives tune optional providers, context budgets, explanation depth, and autonomy only after constraints are satisfied.
- Provider fallback must preserve the capability contract and required constraints.

Future optimization may minimize context, model calls, wall time, or human attention among valid compositions, but correctness constraints take precedence.
