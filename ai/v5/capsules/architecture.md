# Architecture Capsule

Load for cross-layer changes, shared abstractions, new dependencies, or harness/core modifications.

Check:

- reuse established project boundaries before creating a new abstraction;
- keep the change local unless cross-cutting behavior truly requires a shared layer;
- avoid coupling unrelated domains for convenience;
- dependencies must justify lifecycle, security, size, and maintenance cost;
- public contracts should not leak temporary implementation details;
- choose the smallest design that remains clear under likely change, not hypothetical flexibility.

A clever implementation that increases future reasoning cost is a regression unless it buys a concrete requirement.
