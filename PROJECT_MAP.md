# Project Map

This is the human entry point. Use it before browsing folders at random.

## I want to understand…

| Question | Start here | Source-of-truth role |
|---|---|---|
| What this repository is and how to use it | `README.md`, `AGENTS.md` | V4 overview and runtime entry |
| What the Harness is doing in this project | `python3 scripts/ai/v4.py dashboard` | Derived project-local human view |
| How the V4 Harness is structured | Dashboard 「仕組み」, then `ai/v4/` | Self-description first, contracts second |
| Why a Harness capability/provider was selected | Dashboard 「仕組み」 and current run plan | Structured selection reason |
| Where Harness behavior looks inefficient or unstable | Dashboard 「診断」 | Run events, retry/fallback/context observations |
| What the product must do | `docs/PRODUCT.md`, `docs/specs/` | Current requirements |
| How the product system is divided | `docs/ARCHITECTURE.md` | Current product architecture |
| Why a durable choice was made | `docs/decisions/` | Recorded decisions and tradeoffs |
| What changed recently | `assurance/current/`, then `docs/changes/` | Active assurance and historical explanation |
| Why a change is considered ready | `assurance/` | Claims, evidence requirements, Human Checks, uncertainty |
| What verification actually ran | `.ai-artifacts/verification/` | Exact-run deterministic evidence |
| What Harness run events were recorded | `.ai-artifacts/runs/` | Bounded structured V4 runtime history |
| What the host actually executed | `.ai-artifacts/traces/` | Sanitized host/tool audit metadata |

## Folder roles

| Location | Contains | Role |
|---|---|---|
| `docs/` | Product knowledge, decisions, runbooks, concise change records | Durable human/project authority |
| `assurance/` | Claims, evidence requirements, Human Checks | Trust and readiness boundary |
| `ai/v4/` | Active V4 capability/profile/provider/self-description sources | Harness composition authority |
| `ai/` | Supporting policies, schemas, templates, routing sources | Harness and project contracts |
| `.agents/skills/` | Provider implementations used only when selected | Agent workflow providers |
| `scripts/ai/` | V4 runtime plus deterministic providers | Executable source |
| `.harness/` | Project-local tracked Harness configuration | Project profile/Dashboard configuration |
| `.ai-artifacts/` | Plans, events, Dashboard state, verification, traces, indexes | Generated and uncommitted |

## Trust model

A passing command, an AI review, a runtime trace, a human observation, and a durable explanation answer different questions.
Do not collapse them into one confidence score.

Dashboard status is a projection of structured records.
The underlying evidence and Human Checks remain authoritative for readiness.
