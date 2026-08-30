# Quality Gates

The executable gate list is implemented by `scripts/ai/verify`. Project-specific commands are configured in `ai/commands.conf`.

A required gate may be marked not applicable only with an explicit `_NA_REASON`. Never leave a required gate silently empty.

## Always

- Harness self-test
- `git diff --check`

## GREEN

- lint
- unit

## YELLOW

- typecheck
- lint
- unit
- integration
- build
- security
- architecture

## RED

- typecheck
- lint
- unit
- integration
- e2e
- build
- security
- dependency
- architecture
- visual

Project-specific policies may add stricter checks. They should not remove checks merely for convenience.
