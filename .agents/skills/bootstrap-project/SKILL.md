---
name: bootstrap-project
description: Adopt and configure the V4 AI development harness for a new or existing software repository. Use when the template is first copied, ai/TEMPLATE_MODE exists, commands are unconfigured, or project-specific V4 profile/dashboard configuration needs initialization.
---

# Bootstrap Project

1. Inspect repository structure, real build/test configuration, and existing authoritative docs. Avoid exhaustive application-code reading when metadata and configuration are enough.
2. Identify the real stack and commands. Do not invent scripts, scanners, services, environment variables, or dependencies.
3. Update concise project sources of truth and `PROJECT_MAP.md` only where the adopted project differs materially from the template.
4. Configure `ai/commands.conf`. Use explicit N/A reasons only for genuinely inapplicable gates.
5. Initialize the project-local V4 Dashboard configuration:
   ```sh
   python3 scripts/ai/v4.py init
   ```
   Edit `.harness/dashboard.json` to set the stable project id, human-facing name, locale, and default profile.
6. Confirm the chosen V4 profile matches project goals. Profile preferences may not weaken mandatory constraints.
7. Set `PROJECT_READY=true` only when project commands and N/A decisions are accurate.
8. Confirm Python 3 is available. V4 runtime and Dashboard use the standard library and should not introduce a third-party runtime dependency merely for the harness.
9. Run `./scripts/ai/self-test`. Remove `ai/TEMPLATE_MODE` only when the adopted project is ready, then run `./scripts/ai/verify --risk green`.
10. Compile one representative V4 plan and open the Dashboard to verify project-local operation:
    ```sh
    python3 scripts/ai/v4.py plan --task implement --risk GREEN
    python3 scripts/ai/v4.py dashboard
    ```
11. Summarize configured verification, selected profile, known host limitations, remaining Human Checks, and unresolved blocking unknowns.

Do not implement unrelated product features during bootstrap.
