# AI Dev Harness Template — Context-efficient V2

A tool-portable starter for AI-led software development that balances **quality, trust, and context efficiency**.

The repository, not the chat history, is the system of record. Codex, Cursor, Claude Code, and future agents should use the same project knowledge, deterministic checks, risk policy, and compact task handoffs.

## V2 principles

1. **One task = one fresh top-level session** whenever practical.
2. **One primary workflow Skill** (`develop-feature`) for normal product work; avoid mechanical Skill chaining.
3. **Read only relevant context.** `ai/context-map.md` routes tasks to the smallest useful set of docs.
4. **Delegate exploration early, not only testing.** STANDARD/CRITICAL work should move broad read-only exploration to a fresh subagent/context when supported.
5. **Return compact Task Packets, not transcripts.** `ai/templates/task-packet.md` is the handoff contract.
6. **Keep raw logs/artifacts out of the main context.** Deterministic scripts write evidence to files and return concise summaries.
7. **Use specialist reviewers only when triggered.** Security/design/code review is not ceremony for trivial work.
8. **Human approval remains No-Guess Approval.** Humans judge consequences/tradeoffs, not technical claims they cannot verify.

## Two separate classifications

### Work mode — controls orchestration/context

- **MICRO**: obvious local, reversible change. Main agent may explore/implement directly; no ceremonial spec or independent review.
- **STANDARD**: normal feature/behavior change. Prefer early delegated exploration and a compact Task Packet.
- **CRITICAL**: security/data/production/high-consequence work. Use fresh-context exploration plus independent specialist review where supported.

### Risk — controls evidence/release requirements

- **GREEN**: low-impact/reversible.
- **YELLOW**: user-visible/contracts/data/dependencies/integrations.
- **RED**: auth/security boundaries, destructive data, payments, production, personal data, high-impact side effects, or harness enforcement changes.

Work mode and risk are related but not identical. A small auth change may be MICRO in code size but CRITICAL/RED in consequence.

## Repository layout

```text
AGENTS.md                  # short map + hard rules
CLAUDE.md                  # thin adapter importing AGENTS.md

docs/                      # project sources of truth
  PRODUCT.md
  ARCHITECTURE.md
  SECURITY.md
  DESIGN.md
  RELIABILITY.md
  specs/

.agents/skills/            # portable Agent Skills
  bootstrap-project/
  develop-feature/
  verify-work/
  debug-systematically/
  review-code/
  review-security/
  review-design/
  prepare-approval/
  release-change/

ai/
  context-map.md            # what to read for each area
  commands.conf             # real project verification commands
  policies/
  templates/
    task-packet.md          # compact agent-to-agent handoff
    approval-packet.md
  evals/

scripts/ai/
  self-test
  classify-risk
  verify
  validate-approval
```

## Bootstrap a real project

After creating a project from this template, ask the agent:

```text
Use bootstrap-project. Inspect the actual repository and configure this harness without inventing commands or dependencies. Keep project docs concise, adapt ai/context-map.md only where the real codebase needs project-specific routing, configure ai/commands.conf, remove ai/TEMPLATE_MODE only when ready, then run ./scripts/ai/self-test and ./scripts/ai/verify --risk green. Do not implement product features in this task.
```

## Normal development prompt

```text
Use develop-feature for this request. Optimize for context efficiency: classify MICRO/STANDARD/CRITICAL, use ai/context-map.md, delegate broad read-only exploration before implementation when useful, and keep parent context to a compact Task Packet plus final evidence. Run deterministic verification before completion. Do not ask me to approve technical correctness.
```

### Expected flow

```text
User request
    |
    v
Thin main/coordinator
    |
    +-- MICRO ----> focused edit -> deterministic verify
    |
    +-- STANDARD -> explorer -> compact Task Packet -> implement -> verify
    |
    +-- CRITICAL -> explorer -> Task Packet -> implement -> verify
                                      |              |
                                      +--> fresh specialist review(s)
                                                     |
                                                approval if real
                                                human judgment remains
```

## Cursor

Open the repository as the workspace. Cursor can discover repository instructions/Skills; use built-in or custom subagents primarily for **broad exploration and independent review**, not merely for running test commands.

Recommended operating pattern:

- start a fresh chat for each task;
- for STANDARD/CRITICAL work, ask an Explore subagent to return only the Task Packet;
- let the implementer open only the files listed in that packet;
- run `./scripts/ai/verify` directly for deterministic checks;
- use a fresh reviewer only when the change warrants independent reasoning;
- inspect Cursor's context-usage UI periodically to verify that Rules/Skills/MCP/subagents are not dominating context.

## Codex

Start from the repository root and prefer a fresh task/session (and branch/worktree for meaningful work). `AGENTS.md` stays intentionally small; project Skills live under `.agents/skills/`.

Recommended operating pattern:

- one task per fresh Codex session whenever practical;
- avoid growing a long parent session and then spawning many children from it;
- use delegation for context-heavy read-only exploration when supported, but pass compact Task Packets between contexts;
- for independent review, a fresh session/worktree is often preferable to inheriting a very large parent history;
- run the same deterministic `scripts/ai/*` checks regardless of which agent performed the implementation.

## Deterministic verification

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
```

Raw command output is stored under `.ai-artifacts/verification/`; agents should read the generated summary first and inspect raw logs only for targeted failures.

## No-Guess Approval

Human approval must state the exact business/product/risk decision, why human judgment is required, minimum background, verified evidence, assumptions/unknowns, worst case, rollback, alternatives, recommendation, and strongest argument against it.

If a blocking unknown remains, do not release. If a reviewer would need specialist expertise they do not have, do not turn that uncertainty into a cosmetic approval.

## Portability

Treat AI products as replaceable adapters:

```text
knowledge       -> docs/, AGENTS.md
workflow        -> .agents/skills/
context routing -> ai/context-map.md + task-packet.md
enforcement     -> scripts/ai/ + CI
risk policy     -> ai/policies/
evaluation      -> ai/evals/
```

The goal is to change AI tools without rewriting the development contract or losing quality controls.
