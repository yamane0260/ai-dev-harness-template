# Harness Commands

Executable source lives here. Run commands from the repository root.

| Command | Purpose | Writes |
|---|---|---|
| `self-test` | Validate required harness files, scripts, fixtures, and core behavior | Temporary files only |
| `classify-risk` | Calculate a deterministic risk floor from committed + working-tree change | Nothing |
| `verify` | Run risk gates and record exact-run evidence/readiness | `.ai-artifacts/verification/` |
| `validate-assurance` | Validate Claim relationships and optionally evaluate current readiness | Optional requested JSON output |
| `record-evidence` | Internal conversion from gate records to hashed evidence | Requested artifact path |
| `build-project-index` | Derive document/Claim/Evidence/Human Check graph | `.ai-artifacts/index/` by default |
| `record-agent-event` | Adapter for one sanitized host/tool event | `.ai-artifacts/traces/` by default |
| `validate-agent-trace` | Validate events and optionally create a compact coverage summary | Optional requested summary |
| `validate-approval` | Validate No-Guess Approval packet structure | Nothing |

`lib/` is internal standard-library Python code. `tests/` holds deterministic regression tests. Raw command output is generated evidence, not maintained documentation; do not commit it.
