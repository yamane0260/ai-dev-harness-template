# V5 Runtime Index

V5 is a Worker Core, not a smaller copy of V4.1.
Its design assumes that a supervisor AI owns coordination and the human-facing layer.

## Runtime path

```text
Task Envelope
  -> deterministic preflight
  -> bounded context references
  -> five-lens Perspective Scan
  -> implementation
  -> deterministic verification
  -> Result Envelope
  -> handoff guard
```

## Files

- `architecture.md`: responsibility model, context budget, state model, non-goals.
- `kernel.md`: non-negotiable worker invariants.
- `context-map.md`: conditional domain routing.
- `migration-from-v4.1.md`: retained/moved/removed V4.1 responsibilities.
- `capsules/*.md`: small domain guidance, loaded only when triggered.
- `schemas/*.schema.json`: supervisor/worker contracts.
- `project/commands.json`: project-local deterministic verification mapping.
- `../../scripts/ai/v5.py`: CLI.
- `../../scripts/ai/lib/v5_core.py`: deterministic runtime core.

The worker receives conclusions, constraints, and bounded references from the supervisor. It should not reconstruct the whole project plan, team culture, or human decision context on every task.
