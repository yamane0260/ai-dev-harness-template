# V4.1 -> V5 Responsibility Map

V5 is a separate Evidence-Driven Worker Core architecture.

| V4.1 responsibility | V5 disposition |
|---|---|
| profile.resolve | moved to supervisor; Worker receives an Acceptance Contract |
| risk.floor | retained as deterministic floor |
| context.select | retained as bounded references |
| project.explore | moved to supervisor/isolated exploration |
| quality.preflight | five-lens Perspective Scan + domain triggers |
| change.implement | retained |
| debug.diagnose | local; repeated failure triggers fresh diagnosis |
| verification.run | retained as evidence adapters with evidence kinds |
| specialist reviews | conditional capsules or independent verifier tasks |
| assurance.evaluate | split into worker handoff guard + independent acceptance guard |
| human approval/release | supervisor/human layer |
| project index/dashboard/provider composition | outside Worker Core |
| long-lived run ledger | removed; compact contract/evidence only |
| acceptance oracle | formalized as verifier verdict |
| retry policy | failure classification + Loop Guard |
| Brownfield compatibility | baseline assertions |

V4.1 remains independently usable on its existing branch. V5 does not depend on V4 runtime files.