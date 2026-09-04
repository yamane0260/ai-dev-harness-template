# Project Map

This is the human entry point. Use it before browsing folders at random.

## I want to understand…

| Question | Start here | Source-of-truth role |
|---|---|---|
| What this repository is and how to use it | `README.md` | Harness overview and normal workflow |
| What the product must do | `docs/PRODUCT.md`, `docs/specs/` | Current requirements and acceptance criteria |
| How the system is divided | `docs/ARCHITECTURE.md` | Current architecture and boundaries |
| Why a durable choice was made | `docs/decisions/` | Recorded decisions and tradeoffs |
| What a project-specific concept means | `docs/concepts/` | Current reusable technical knowledge |
| What changed recently | `assurance/current/`, then `docs/changes/` | Active assurance state, then historical explanation |
| Why a change is considered ready | `assurance/` | Claims, evidence requirements, human checks, and uncertainty |
| What a human still must test or decide | active `human-checks.json` files | MUST / SHOULD / OPTIONAL human work |
| How to diagnose or recover | `docs/runbooks/`, `docs/RELIABILITY.md` | Current operational procedure |
| What the AI actually executed | `.ai-artifacts/traces/` | Host-captured audit evidence; generated and not committed |
| What verification actually ran | `.ai-artifacts/verification/` | Exact-revision commands, results, logs, and hashes |

## Folder roles

| Location | Contains | Read when | Authorship |
|---|---|---|---|
| `docs/` | Current knowledge and concise historical briefs | Understanding product, architecture, decisions, or recovery | Human/agent maintained |
| `assurance/` | Human-facing trust boundary: Claims, evidence requirements, human checks | Deciding whether a change is understood and release-ready | Human/agent maintained, schema-validated |
| `ai/` | Policies, schemas, templates, routing, evals; see `ai/README.md` | Changing or applying the harness | Human/agent maintained |
| `.agents/skills/` | Portable task workflows; see `.agents/skills/README.md` | Running a defined development/review workflow | Human/agent maintained |
| `scripts/ai/` | Deterministic validation and derived-index tools; see `scripts/ai/README.md` | Producing or checking evidence | Executable source |
| `.ai-artifacts/` | Raw logs, exact-run evidence, traces, derived graph/index | Investigating a run or failure | Generated; never commit |

## Trust model

A green command, an AI review, a provenance record, and a human review answer different questions. Do not collapse them into one confidence score.

1. Requirements state the intended outcome.
2. Claims state the property that must be true.
3. Evidence requirements state how that property can be checked.
4. Verification records what actually ran on an exact repository state.
5. Human checks isolate judgments or real-device observations that automation cannot establish.
6. Durable docs preserve decisions, invariants, failure modes, and recovery knowledge.
7. Agent traces show actions and control boundaries; they do not prove product correctness.

Run `./scripts/ai/build-project-index` to derive a machine-readable relationship graph under `.ai-artifacts/index/`. The derived index is never the source of truth.
