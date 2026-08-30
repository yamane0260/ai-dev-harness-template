# AI Development Harness

Optimize for correctness **and context efficiency**. Keep the main agent focused on intent, decisions, a small task packet, and final evidence.

## Start here

- New/adopted repo: use `bootstrap-project`.
- Product change: use `develop-feature` as the primary workflow skill.
- Read `ai/context-map.md` before loading project docs. Load only docs relevant to the touched area.
- Deterministic checks live in `scripts/ai/`; project commands live in `ai/commands.conf`.

## Work modes

- **MICRO**: local, reversible, low-risk change. Main agent may explore/implement directly. No ceremonial spec or independent review.
- **STANDARD**: normal feature/behavior change. Delegate context-heavy read-only exploration when supported; return a compact Task Packet, then implement.
- **CRITICAL**: security/data/production/high-consequence change. Use fresh-context exploration and independent specialist review where supported.

Risk (`GREEN/YELLOW/RED`) and work mode are separate: risk controls evidence; work mode controls context/orchestration.

## Context rules

- Prefer one task per fresh top-level session.
- Do not read all docs by default; use `ai/context-map.md`.
- Delegate broad codebase exploration before implementation when it would pollute the main context.
- Subagent/explorer output to the parent should normally be a compact Task Packet: goal, criteria, relevant files, constraints, risk/unknowns, and recommended next action.
- Keep raw logs, broad search results, and large file dumps out of the main context. Persist evidence to files/artifacts and return paths plus concise summaries.
- Do not chain Skills mechanically. `develop-feature` owns the normal workflow; invoke specialist review/approval Skills only when their trigger applies.

## Hard rules

- Never claim success without fresh verification evidence from the current revision.
- Never weaken/delete/skip a failing check merely to get green status.
- Never invent commands, dependencies, APIs, data, environment variables, or product requirements.
- Prefer the smallest change that satisfies observable acceptance criteria.
- Human approval is for desired consequences and real tradeoffs, not for guessing about technical correctness.
- If a blocking unknown remains, do not release.

## Commands

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
```
