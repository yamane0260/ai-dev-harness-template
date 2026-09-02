# AI Development Harness

Optimize for correctness, real-world quality, and context efficiency. Keep the main agent focused on intent, decisions, a compact task packet, and final evidence.

## Start here

- New/adopted repo: use `bootstrap-project`.
- Product change: use `develop-feature` as the primary workflow skill.
- Before non-trivial implementation, apply the Quality Envelope in `ai/quality-envelope.md`; use `spec-gap-preflight` when triggered.
- Read `ai/context-map.md` before loading project docs. Load only docs relevant to the touched area and Quality Impact Vector.
- Deterministic checks live in `scripts/ai/`; project commands live in `ai/commands.conf`.

## Work modes

- **MICRO**: local, reversible, low-risk change. Main agent may explore/implement directly. No ceremonial spec or independent review.
- **STANDARD**: normal feature/behavior change. Delegate context-heavy read-only exploration when supported; return a compact Task Packet, then implement.
- **CRITICAL**: security/data/production/high-consequence change. Use fresh-context exploration and independent specialist review where supported.

Risk (`GREEN/YELLOW/RED`) controls evidence. Work mode controls context/orchestration. Quality Impact controls which nonfunctional domains must be considered.

## Context rules

- Prefer one task per fresh top-level session.
- Do not read all docs by default; use `ai/context-map.md` and the Quality Impact Vector.
- Delegate broad exploration before implementation when it would pollute the main context.
- Explorer/preflight output should be compact: goal, criteria, relevant files, relevant quality domains, constraints, risk/unknowns, next action.
- Keep raw logs, broad search results, screenshots, and large file dumps out of the main context. Persist evidence and return paths plus concise summaries.
- Do not chain Skills mechanically. Invoke specialist review only when its trigger applies.

## Hard rules

- Never claim success without fresh verification evidence from the current revision.
- Never weaken/delete/skip a failing check merely to get green status.
- Never invent commands, dependencies, APIs, data, environment variables, or product requirements.
- Functional-spec compliance is not sufficient when a material UX, security, data, compatibility, reliability, operability, performance/cost, privacy, architecture, accessibility, or supply-chain risk remains.
- Add negative/invariant criteria for material cases: what must never happen, failure behavior, cross-user behavior, duplicates/concurrency, compatibility, recovery, and resource limits.
- Prefer the smallest change that satisfies observable acceptance criteria and the relevant Quality Envelope.
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
