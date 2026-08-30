# AI Dev Harness Template

A tool-portable starter repository for AI-led software development with high automation, machine-verifiable quality gates, explicit risk classification, and human approval that does not depend on guesswork.

The core is intentionally independent of a particular coding agent. Codex, Cursor, Claude Code, and future agents should all read the same repository policy and run the same scripts.

## What this repository provides

- `AGENTS.md`: short repository map and non-negotiable rules.
- `.agents/skills/`: portable Agent Skills for project bootstrap, implementation, debugging, verification, code/security/design review, approval preparation, and release.
- `docs/`: project-specific product, architecture, security, design, and reliability sources of truth.
- `ai/policies/`: risk and quality-gate policy.
- `ai/commands.conf`: project-specific deterministic verification commands.
- `scripts/ai/`: portable shell entry points that agents and CI run.
- `.github/workflows/verify.yml`: CI enforcement.
- `.github/pull_request_template.md`: evidence-first PR structure.

## Core model

```text
Human intent / business judgment / visual taste
                     |
                     v
              Agent implementation
                     |
                     v
        Deterministic verification evidence
                     |
          +----------+----------+
          |                     |
     Independent review     Risk review
          |                     |
          +----------+----------+
                     |
                     v
             Human-ready approval
              only when needed
```

## Start a new project

1. Create a new private repository from this template, or copy this repository into an existing project.
2. Ask the agent to run the `bootstrap-project` skill.
3. The agent must inspect the actual stack and fill `ai/commands.conf` with commands that really exist. It must not invent commands.
4. Fill or refine the files under `docs/`.
5. Remove `ai/TEMPLATE_MODE` only when the project verification configuration is ready.
6. Run:

```sh
./scripts/ai/self-test
./scripts/ai/verify --risk green
```

The project is not considered adopted until both commands pass.

## Daily feature workflow

```text
request
  -> develop-feature
  -> acceptance criteria
  -> risk classification
  -> implementation + tests
  -> verify-work
  -> independent review where required
  -> prepare-approval only if human judgment remains
  -> release-change
```

## Risk levels

- **GREEN**: low-impact, reversible work that is well covered by deterministic checks. May be agent-only after gates pass.
- **YELLOW**: user-visible or contract/data/dependency changes. Requires stronger automated evidence and usually independent AI review. Human approval is required only for remaining business/UX consequences.
- **RED**: security boundaries, auth/permissions, destructive data operations, payments, production infrastructure, personal data, bulk external side effects, or policy/harness changes. Requires the full gate set and a human-ready approval packet before irreversible action or release.

See `ai/policies/risk-policy.md` for the complete policy.

## Human approval rule: No-Guess Approval

A human must never be asked to approve something they would have to guess about.

Before requesting approval, the agent must explain:

- the exact decision the human is being asked to make;
- why human judgment is necessary;
- the minimum background knowledge required;
- user/business consequences in plain language;
- deterministic evidence already collected;
- assumptions and unknowns;
- worst-case impact;
- rollback/recovery;
- alternatives;
- the strongest argument against the agent's recommendation.

Use `ai/templates/approval-packet.md` and the `prepare-approval` skill.

## Cursor

Cursor supports root/nested `AGENTS.md` and discovers project Agent Skills under `.agents/skills/`. Open the repository as a trusted workspace; the rules and skills are then available to Agent.

First adoption prompt:

```text
Use the bootstrap-project skill. Inspect this repository and configure the AI development harness for the actual stack. Do not invent commands or dependencies. Populate the project docs with evidence from the repo, configure ai/commands.conf, remove ai/TEMPLATE_MODE only when ready, then run ./scripts/ai/self-test and ./scripts/ai/verify --risk green. Do not implement product features in this task.
```

For ordinary work:

```text
Use develop-feature for this request. Follow the repository risk policy, run fresh verification, and do not ask me to approve technical correctness. If human judgment is needed, produce a No-Guess Approval Packet.
```

Cursor can invoke a skill explicitly from the Agent UI by typing `/` and selecting the skill name.

Official references:
- https://cursor.com/docs/skills
- https://cursor.com/docs/rules
- https://cursor.com/docs/hooks

## Codex

Install the Codex CLI if needed:

```sh
npm install -g @openai/codex
```

Then start Codex from the repository root:

```sh
cd /path/to/project
codex
```

Codex reads hierarchical `AGENTS.md` instructions and repository skills under `.agents/skills/`. Use the same bootstrap prompt shown above. Skills may be selected explicitly from Codex's skill selector or triggered by their descriptions.

For long agent-led tasks, prefer a branch/worktree and require `./scripts/ai/verify` before asking to merge.

Official references:
- https://openai.com/codex/
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://github.com/openai/codex

## GitHub settings to enable after creating a real project

Recommended baseline for `main`:

- block direct agent pushes to `main`;
- require pull requests for YELLOW/RED work;
- require the `verify` GitHub Actions check;
- keep deployment secrets in GitHub Environments or the deployment platform, not in the repository;
- require a human approval step for irreversible RED production actions.

Do not create approval bureaucracy for GREEN work that is already machine-verifiable.

## Portability principle

Treat AI products as replaceable adapters. Keep durable assets in the repository:

```text
Portable knowledge     -> docs/, AGENTS.md
Portable workflows     -> .agents/skills/
Portable enforcement   -> scripts/ai/, CI
Portable risk policy   -> ai/policies/
Portable evaluation    -> ai/evals/
Tool-specific adapters -> .cursor/, .codex/, .claude/ only when needed
```

When adopting a new agent in the future, first connect it to these repository assets rather than rewriting the development process for that agent.
