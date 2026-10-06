# V5 Runtime Index

V5 is an Evidence-Driven Worker Core.

```text
Acceptance Contract
  -> preflight
  -> bounded context
  -> Perspective Scan
  -> implementation
  -> evidence adapters
  -> worker handoff guard
  -> fresh Verifier Packet
  -> independent acceptance
  -> PASS or classified FAIL
  -> bounded next action
```

## Acceptance Contract

- `goal`: intended outcome
- `acceptance`: observable success conditions
- `invariants`: conditions that must remain true
- `baseline`: existing behavior to preserve, especially for Brownfield work
- `evidenceKinds`: independent evidence categories required for worker handoff

A deterministic contract hash binds preflight and verification to the exact contract. Changing the contract invalidates old evidence.

## Independent acceptance

Worker verification is not final acceptance. For YELLOW/RED tasks, use a fresh verifier context. The verifier receives the contract, repository fingerprint, and compact worker evidence, but not the worker reasoning transcript.

## Failure classification and Loop Guard

Failed acceptance is classified as implementation, design, requirement, oracle, environment, or unknown. The class determines which layer changes next. Repeated identical failures or design oscillation force fresh diagnosis or supervisor review.

## Files

- `architecture.md`: evidence-loop architecture
- `kernel.md`: non-negotiable invariants
- `context-map.md`: conditional domain routing
- `schemas/*.schema.json`: task, evidence, verifier, and failure contracts
- `project/commands.json`: evidence adapter mapping
- `../../scripts/ai/v5.py`: CLI
- `../../scripts/ai/lib/v5_core.py`: deterministic core