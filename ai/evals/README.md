# Harness Evals

Store small regression cases here when the agent or harness makes a recurring mistake.

A useful case contains:

- `prompt.md`: realistic task/request;
- `expected.md`: required behaviors, forbidden behaviors, and expected risk level;
- optional fixtures/logs/diffs.

Prefer adding an eval when a failure depends on agent judgment. Prefer a deterministic test/lint rule when the failure can be checked mechanically.
