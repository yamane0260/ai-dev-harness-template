# V4.1 -> V5 Responsibility Map

V5 is not a compatibility upgrade to the V4 runtime. It is a separate Worker Core architecture.

| V4.1 responsibility | V5 disposition |
|---|---|
| `profile.resolve` | moved to supervisor; Worker receives a Task Envelope |
| `risk.floor` | retained and simplified as deterministic Worker floor |
| `context.select` | retained and simplified to bounded references |
| `project.explore` | moved to supervisor/isolated exploration; Worker may do targeted local reads |
| `quality.preflight` | replaced by five-lens Perspective Scan + domain triggers |
| `change.implement` | retained as Worker core responsibility |
| `debug.diagnose` | local behavior, not a separate always-loaded capability |
| `verification.run` | retained and simplified |
| specialist reviews | conditional capsules or supervisor-assigned independent tasks |
| `assurance.evaluate` | reduced to Worker handoff guard only |
| human approval | moved to supervisor/human layer |
| release evaluation | moved to supervisor/CI/release layer |
| human/system explanations | moved to supervisor |
| human legibility | moved to supervisor/integration policy |
| project index | moved to supervisor/shared knowledge layer |
| subagent delegation | moved to supervisor |
| Dashboard/read model | removed from Worker |
| self-description UI metadata | removed from Worker |
| team compatibility observation | moved to supervisor/sidecar service |
| PR/commit surface adaptation | moved to supervisor/collaboration layer |
| long-lived run ledger | removed by default; compact handoff/evidence only |

V4.1 remains independently usable on its existing branch. V5 must not require V4 runtime files, V4 schemas, Dashboard code, or V4 provider registry to execute.
