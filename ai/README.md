# Harness Definition

This directory contains the authoritative V4 contracts, policies, schemas, templates, and provider metadata used by development agents.

| Location | Role |
|---|---|
| `v4/` | Active V4 architecture, capability inventory, profiles, provider registry, self-description |
| `schemas/` | Structured contracts for V4 composition plus assurance/evidence records |
| `policies/` | Trust, risk, assurance, quality, human-legibility, and agent-control rules retained by V4 |
| `context-map.md` | Bounded project-context routing source used by V4 providers |
| `quality-envelope.md` | Quality Impact taxonomy and preflight source |
| `commands.conf` | Adopted project's deterministic verification commands |
| `harness-commands.conf` | Template-maintainer verification commands |
| `templates/` | Starting records and project configuration templates |
| `evals/` | Regression cases |

Generated plans, run events, Dashboard state, evidence, indexes, reviews, and traces belong under `.ai-artifacts/`.

## Runtime status

V4 is the authoritative composition model.

Existing V3 scripts and Skills that still provide useful deterministic or review behavior are retained as V4 providers.
Their old fixed routing role is no longer authoritative.

Start with `v4/README.md`, `AGENTS.md`, and the architecture decision in `docs/decisions/2026-09-15-v4-composable-harness-architecture.md`.
