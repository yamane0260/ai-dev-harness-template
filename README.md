# AI Development Harness V5 — Worker Core

This branch is the V5 redesign of `ai-dev-harness-template`.
It is intentionally managed separately from V4/V4.1 and targets a different operating model:

```text
Human <-> Supervisor AI <-> V5 Worker Harness <-> Implementation AI
```

V4.1 is a human-facing full harness. V5 is a supervisor-facing worker harness.
V5 removes the dashboard, human explanation layer, release approval workflow, long-lived run ledger, and worker-side orchestration. It keeps a small deterministic safety floor, selective context routing, a five-lens quality scan, exact-state verification, and a compact handoff contract.

## Start

```sh
python3 scripts/ai/v5.py validate-task --task ai/v5/examples/task.json
python3 scripts/ai/v5.py preflight --task ai/v5/examples/task.json
python3 scripts/ai/v5.py validate-scan --scan ai/v5/examples/scan.json
```

See `ai/v5/README.md` for architecture and `ai/v5/migration-from-v4.1.md` for the responsibility split.
