# Harness Commands

Executable source lives here. Run commands from the repository root.

| Command | Purpose | Writes |
|---|---|---|
| `python3 scripts/ai/v4.py init` | Initialize project-local V4 Dashboard config | `.harness/dashboard.json` |
| `python3 scripts/ai/v4.py plan` | Compile a V4 execution plan and start a run ledger | `.ai-artifacts/runs/` |
| `python3 scripts/ai/v4.py event` | Append one sanitized V4 runtime event | `.ai-artifacts/runs/` |
| `python3 scripts/ai/v4.py state --write` | Build the project Dashboard read model | `.ai-artifacts/dashboard/` |
| `python3 scripts/ai/v4.py dashboard` | Serve the project-local self-describing Dashboard | generated state only |
| `self-test` | Validate required harness files, V4 runtime, fixtures, and core behavior | temporary files only |
| `classify-risk` | Calculate the deterministic risk floor | nothing |
| `verify` | Run deterministic gates and record exact-run evidence/readiness | `.ai-artifacts/verification/` |
| `validate-assurance` | Validate Claim relationships and readiness | optional requested JSON |
| `build-project-index` | Derive document/Claim/Evidence/Human Check relationships | `.ai-artifacts/index/` |
| `record-agent-event` | Record sanitized host/tool audit metadata | `.ai-artifacts/traces/` |

V4 reuses deterministic V3-era implementations where they remain valid providers.
Raw command output stays outside normal model context and durable human documentation.
