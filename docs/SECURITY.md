# Security

> Record project-specific security facts and controls. Security-sensitive behavior should be enforced by code, tests, configuration, and scanners wherever possible.

## Authentication

- Provider/mechanism:
- Session/token handling:

## Authorization

- Authorization model:
- Server-side enforcement point:
- Cross-user / cross-tenant tests:

## Data classification

- Personal data:
- Sensitive business data:
- Secrets:

## Input and output boundaries

- Validation approach:
- File upload policy:
- External URL / SSRF policy:
- HTML / script injection policy:

## Dependencies

- Lockfile:
- Vulnerability scanning command:
- New dependency review expectation:

## Security invariants

- Never rely on client-side authorization alone.
- Never commit secrets.
- Never disable a security test or scanner merely to make CI pass.
- Security-critical code and its tests should not rely solely on the same implementation agent's judgment.

## Open security decisions

- None yet.
