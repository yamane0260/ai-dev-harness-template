---
name: bootstrap-project
description: Adopt and configure this AI development harness for a new or existing software repository. Use when the template is first copied, ai/TEMPLATE_MODE exists, commands are unconfigured, or project-specific sources of truth/context routing need initialization before agent-led development.
---

# Bootstrap Project

1. Inspect the repository structure, real build/test configuration, and existing docs. Do not exhaustively read application code when metadata/config is enough.
2. Identify the real stack and commands. Do not invent scripts, scanners, services, env vars, or dependencies.
3. Update project docs with verified facts, keeping them concise. Record unresolved decisions instead of guessing.
4. Update `ai/context-map.md` only where project-specific paths/domains differ materially from the generic map. The goal is to prevent agents from reading all docs for every task.
5. Configure required fields in `ai/commands.conf`; use specific `_NA_REASON` only for genuinely inapplicable gates.
6. Set `PROJECT_READY=true` only when commands/N/A decisions are accurate. Add deterministic checks for critical prose-only invariants when practical.
7. Run `./scripts/ai/self-test` while `ai/TEMPLATE_MODE` exists. Remove the marker only when ready, then run `./scripts/ai/verify --risk green`.
8. Summarize enforced checks, context-routing decisions, remaining human judgment, and blocking unknowns. Keep the summary compact.

Do not implement unrelated product features during bootstrap.
