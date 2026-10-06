# V5 Architecture Design — Evidence-Driven Supervisor/Worker Split

## Objective

V5 optimizes the correction loop, not a single implementation attempt:

```text
design -> implement -> observe reality -> classify mismatch -> return to the correct layer
```

## Roles

### Supervisor
- clarifies requirements and creates/revises Acceptance Contracts;
- decomposes work and allocates workers/verifiers;
- owns private hold-out cases when useful;
- classifies acceptance failures and chooses integration/release actions.

### Worker
- runs deterministic risk/context preflight;
- implements the bounded task;
- produces evidence through configured adapters;
- returns a compact handoff without claiming independent acceptance.

### Fresh Verifier
- evaluates acceptance without worker narrative;
- checks invariants and Brownfield baseline compatibility;
- uses direct observations and optional hold-out cases;
- returns pass/fail/unknown evidence without editing implementation.

## Evidence model

Configured gates carry an evidence `kind` such as `test`, `static`, `api`, `browser`, `database`, `runtime`, `external`, or `human`. The task may require evidence kinds. A passing command is insufficient when the required kind is absent.

## Contract drift protection

Preflight and verification carry a contract hash. If acceptance criteria, invariants, baseline, constraints, or evidence requirements change, old evidence is invalid.

## Brownfield strategy

Critical current behavior is recorded as `baseline`. V5 does not require full legacy understanding before change; it requires important legacy behavior not to change invisibly.

## Risk-based independence

- GREEN: fresh verifier optional.
- YELLOW: fresh verifier required.
- RED: fresh verifier required; hold-out acceptance evidence is required when practical, otherwise an explicit not-applicable justification is required.

## Failure classes

- `implementation`: design is sound, implementation is wrong.
- `design`: architecture or behavior design must change.
- `requirement`: intended behavior is ambiguous or contradictory.
- `oracle`: verification expectation is wrong or insufficient.
- `environment`: execution environment caused the failure.
- `unknown`: evidence is insufficient.

## Loop Guard

- first low-risk implementation failure may retry once;
- repeated identical implementation failure forces fresh diagnosis;
- RED implementation failure forces fresh diagnosis;
- regression returns to baseline comparison before further change;
- two design changes without convergence force supervisor review.

## Completion states

`HANDOFF_READY` means worker evidence is current for the exact contract. `ACCEPTANCE_READY` means independent acceptance proved the bounded contract, invariants, and baseline. Neither means release-ready.