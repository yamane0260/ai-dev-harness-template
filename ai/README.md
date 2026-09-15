# Harness Definition

This directory contains the portable rules and data contracts used by development agents.

| Location | Role | Source status |
|---|---|---|
| `context-map.md` | Routes agents to the smallest relevant context | Maintained V3 source |
| `quality-envelope.md` | Routes material nonfunctional quality concerns | Maintained V3 source |
| `commands.conf` | Adopted product's deterministic commands/N/A reasons | Project-maintained source |
| `harness-commands.conf` | Tests this template's own mechanics | Template-maintained source; never product evidence |
| `policies/` | Risk, gates, mutual verification, legibility, explanation, and agent-control rules | Maintained V3 source and V4 migration input |
| `schemas/` | Interchange contracts for structured records/artifacts | Maintained source; semantic enforcement also lives in scripts |
| `templates/` | Starting files for tasks, assurance, Human Checks, and structured reviews | Maintained examples, not completed project records |
| `evals/` | Regression cases for agent judgment and deterministic behavior | Test source |
| `v4/` | Contract-first V4 architecture, capability inventory, presets, and V3-to-V4 migration map | Proposed migration source; not yet the active runtime |

Generated evidence or indexes do not belong here; they belong under `.ai-artifacts/`.

## V4 migration status

The current V3 workflow remains authoritative.
The `v4/` directory defines the target composable architecture before runtime cutover so later changes can be evaluated against explicit contracts instead of evolving the workflow piecemeal.

Start with [`v4/README.md`](v4/README.md) and the architecture decision in [`docs/decisions/2026-09-15-v4-composable-harness-architecture.md`](../docs/decisions/2026-09-15-v4-composable-harness-architecture.md).
