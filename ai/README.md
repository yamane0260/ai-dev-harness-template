# Harness Definition

This directory contains the portable rules and data contracts used by development agents.

| Location | Role | Source status |
|---|---|---|
| `context-map.md` | Routes agents to the smallest relevant context | Maintained source |
| `quality-envelope.md` | Routes material nonfunctional quality concerns | Maintained source |
| `commands.conf` | Adopted product's deterministic commands/N/A reasons | Project-maintained source |
| `harness-commands.conf` | Tests this template's own mechanics | Template-maintained source; never product evidence |
| `policies/` | Risk, gates, assurance, legibility, explanation, and agent-control rules | Maintained source |
| `schemas/` | Interchange contracts for structured records/artifacts | Maintained source; semantic enforcement also lives in scripts |
| `templates/` | Starting files to copy and replace | Maintained examples, not completed project records |
| `evals/` | Regression cases for agent judgment and deterministic behavior | Test source |

Generated evidence or indexes do not belong here; they belong under `.ai-artifacts/`.
