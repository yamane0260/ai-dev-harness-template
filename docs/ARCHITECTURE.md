# Architecture

> Describe the architecture that actually exists or has been explicitly approved. Prefer enforceable boundaries over aspirational prose.

## System overview

- Runtime(s):
- Client(s):
- Backend/API:
- Data store(s):
- External services:

## Dependency direction

Document allowed dependency directions. Add an architecture check to `ai/commands.conf` whenever this can be tested automatically.

## Data boundaries

- Inputs and validation:
- Trusted vs untrusted boundaries:
- Persistence boundaries:

## Change rules

- Prefer existing abstractions before adding new ones.
- Avoid speculative layers and generic helpers without a current use case.
- New dependencies require a concrete reason and verification that the package/project is real and maintained.
- Architecture exceptions must be documented in the PR and either tested or explicitly approved.

## Open architecture decisions

- None yet.
