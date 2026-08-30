---
name: bootstrap-project
description: Adopt and configure this AI development harness for a new or existing software repository. Use when the template is first copied, ai/TEMPLATE_MODE exists, ai/commands.conf is unconfigured, or a project needs its product/architecture/security/design/reliability sources of truth initialized before agent-led development.
---

# Bootstrap Project

1. Read `AGENTS.md`, the existing repository structure, build/test configuration, and relevant existing docs.
2. Identify the real stack and real commands. Do not invent package scripts, scanners, services, environment variables, or dependencies.
3. Update `docs/PRODUCT.md`, `ARCHITECTURE.md`, `SECURITY.md`, `DESIGN.md`, and `RELIABILITY.md` with verified facts. Keep unresolved product decisions under `Open decisions` instead of guessing.
4. Configure every field in `ai/commands.conf` required by the project. For a genuinely inapplicable gate, set a specific `_NA_REASON`. Do not use N/A merely because a check is inconvenient to set up.
5. Set `PROJECT_READY=true` only after the commands and N/A decisions are accurate.
6. Add missing deterministic checks when a critical invariant is currently prose-only and can reasonably be automated.
7. Run `./scripts/ai/self-test` while `ai/TEMPLATE_MODE` is still present.
8. Remove `ai/TEMPLATE_MODE`, then run `./scripts/ai/verify --risk green`.
9. If verification fails, fix the harness/project configuration before product feature work begins.
10. Summarize what is enforced automatically, what remains human judgment, and any blocking unknowns.

Do not implement unrelated product features during bootstrap.
