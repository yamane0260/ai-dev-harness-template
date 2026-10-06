# V5 Architecture Design — Supervisor/Worker Split

## 1. Problem statement

V4.1 was designed around a human directly operating an implementation AI. That justified Dashboard views, human-legibility records, approval packets, long-lived project explanation, provider composition, and team-visible surface adaptation inside the harness.

V5 assumes a different environment: a supervisor AI coordinates one or more implementation workers. Repeating supervisor responsibilities inside every worker wastes context and model budget and can reduce implementation quality by crowding out task-relevant reasoning.

## 2. Responsibility boundary

### Supervisor AI owns

- dialogue with humans;
- requirement clarification and decomposition;
- cross-task planning and dependency management;
- allocation of work to workers;
- team convention discovery and collaboration-surface wording;
- project-wide memory/indexing;
- human-facing status, dashboard, and explanations;
- approval preparation and final release/integration decisions;
- reconciliation of conflicting worker results.

### V5 Worker owns

- validating the Task Envelope;
- deterministic minimum risk detection;
- loading only task-relevant context;
- examining correctness, boundaries, failure modes, work fit, and simplicity;
- implementing the bounded task;
- running configured deterministic verification;
- returning compact decisions, assumptions, residual risks, and escalation state.

## 3. Stateless-by-default runtime

V5 does not maintain a long-lived run ledger by default. The repository, CI, supervisor state, and Result Envelope are the durable sources. Verification output is a bounded artifact containing hashes and pass/fail state, not raw logs.

This reduces duplicated state and prevents worker history from becoming another context source that must be continuously loaded.

## 4. Safety model

Safety is split into two layers:

1. **Deterministic floor** — path/hint based risk escalation, required gate routing, schema validation, exact-repository evidence freshness, and completion guard.
2. **Reasoning layer** — the five-lens Perspective Scan and conditional domain capsules.

A worker may always escalate above the floor. It cannot downgrade it.

## 5. Context budget model

V5 treats context as a budgeted runtime resource.

Default target:

- always-loaded `AGENTS.md`: approximately 1k tokens or less;
- Task Envelope: approximately 800 tokens or less;
- preflight result: a few hundred tokens;
- each triggered domain capsule: approximately 300-600 tokens;
- raw logs and broad repository exploration stay outside normal parent context.

The runtime returns file references, not copied bodies. The implementation agent reads only those references that are actually needed.

## 6. Perspective Scan

The scan is intentionally smaller than the V4 Quality Envelope. It uses five stable questions that catch the majority of "it works, but it is not good professional work" failures:

- Correctness
- Boundary
- Failure
- Work fit
- Simplicity

A finding may trigger one of five optional capsules: security, UX, data, reliability, architecture.

## 7. Completion semantics

V5 never calculates universal or release readiness. Its strongest positive state is `implemented`:

> The assigned worker task is implemented and all gates required by the current Worker Core preflight passed on the current repository state, with no unresolved worker escalation.

Integration, acceptance, rollout, human judgment, and release remain outside this claim.

## 8. Non-goals

V5 deliberately does not provide:

- Dashboard UI;
- provider marketplace/composition engine;
- human approval packet generation;
- human-legibility documentation generation;
- long-running orchestration or worker delegation;
- team culture inference;
- PR/commit wording adaptation;
- project-wide knowledge index;
- release readiness calculation.

Those can exist in a supervisor layer without consuming Worker context.
