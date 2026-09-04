# Assurance

This directory answers: **what must be true, what proves it, what remains uncertain, and what only a human can check?**

It is a human-facing source of truth. Raw run output remains under `.ai-artifacts/`.

## Layout

```text
assurance/
  current/                 # active change manifests and human checks
    <change-id>/
      manifest.json
      human-checks.json
  changes/                 # retained/released assurance records when useful
    <change-id>/
      manifest.json
      human-checks.json
```

Use `ai/templates/assurance/` to start a record. Validate it with:

```sh
./scripts/ai/validate-assurance --manifest assurance/current/<change-id>/manifest.json
```

Run verification and calculate readiness together with:

```sh
./scripts/ai/verify --risk yellow --assurance assurance/current/<change-id>/manifest.json
```

For a release decision, add `--release`. This fails closed when a MUST Claim lacks current evidence, when required AI review records are absent, or when a MUST Human Check is pending/failed.

If the manifest requires agent event coverage, first validate the JSONL trace with `validate-agent-trace --summary <path>`, then pass that path through `verify --agent-trace-summary <path>`. A summary proves only the coverage its capture source can actually claim.

## Sources and derived data

- Committed manifest: intent, Claim relationships, evidence requirements, Human Checks, and residual uncertainty.
- Generated evidence: exact revision, command, exit code, log path/hash, and environment under `.ai-artifacts/verification/`.
- Derived readiness: calculated from the committed manifest plus current generated evidence.

Never commit a transient PASS merely because an agent said a check succeeded. The executable verifier owns run status.
