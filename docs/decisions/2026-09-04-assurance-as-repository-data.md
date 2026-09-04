# Decision: Assurance as repository data with a derived read model

- Date: 2026-09-04
- Status: accepted
- Supersedes: none

## Context

The V2.3 harness preserves human-readable Change Briefs and deterministic gate results, but a passing gate does not state which property it establishes. File hierarchy alone also cannot support change-, risk-, component-, evidence-, and learning-oriented navigation at the same time.

## Decision

Store compact Requirement, Claim, evidence requirement, Human Check, scope, uncertainty, and knowledge-reference relationships as committed JSON under `assurance/`. Keep exact-run evidence and traces under ignored `.ai-artifacts/`. Derive a local relationship index from both repository docs and assurance records.

Use JSON plus Python's standard library. Do not introduce a graph database or third-party schema/parser dependency for the foundation.

## Provenance

- `RECORDED`: the project owner requested that a completed AI implementation include human-understandable information, explicit AI-vs-human verification boundaries, and context-efficient relationship memory.
- `RECORDED`: the accepted V3 direction prioritizes Assurance data and `PROJECT_MAP.md` before building a dedicated UI.
- `DERIVED`: the existing repository already separates durable docs from ignored raw artifacts and uses shell-based deterministic gates.

## Consequences

- A manifest describes proof obligations; it cannot self-assert a current PASS.
- `verify` can produce exact-run evidence and join it to a manifest without committing logs.
- Human checks become searchable first-class work instead of prose buried in a Change Brief.
- The future Explorer can be replaced or rebuilt because it consumes a derived index.
- Python 3 becomes a documented harness prerequisite, but no third-party package is added.
- Trace completeness still depends on the execution host and must be disclosed.

## Rejected alternatives

- **Graph database as source of truth:** rejected because synchronization with Git would create a second consistency problem.
- **Long prose for every function/line:** rejected because most explanation is reconstructable and would consume maintainer/model attention.
- **One trust score:** rejected because provenance, verification, human judgment, legibility, and agent control answer different questions.
- **Build the UI first:** rejected because an attractive UI over ambiguous data would not improve assurance.
