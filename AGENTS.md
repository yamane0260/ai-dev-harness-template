# AI Development Harness

Optimize for correctness, real-world quality, context efficiency, and durable human understanding. Keep the main agent focused on intent, decisions, a compact task packet, and final evidence.

## Start here

- New/adopted repo: use `bootstrap-project`.
- Product change: use `develop-feature` as the primary workflow skill.
- Before non-trivial implementation, apply `ai/quality-envelope.md`; use `spec-gap-preflight` when triggered.
- Read `ai/context-map.md` before loading project docs.
- Human understanding policy: `ai/policies/human-legibility.md`.
- Deterministic checks live in `scripts/ai/`; project commands live in `ai/commands.conf`.

## Independent classifications

- **Work mode** — MICRO / STANDARD / CRITICAL: controls context/orchestration.
- **Risk** — GREEN / YELLOW / RED: controls evidence/release requirements.
- **Quality Impact** — routes only relevant nonfunctional domains.
- **Knowledge Impact** — NONE / LOW / MATERIAL / CRITICAL: controls durable human-understanding records.

Do not raise one classification merely because another is high; use its own definition.

## Context rules

- Prefer one task per fresh top-level session.
- Load only docs relevant to touched paths and material quality/knowledge impacts.
- Delegate broad exploration before implementation when it would pollute the main context.
- Keep raw logs, transcripts, screenshots, and large dumps out of the main context and durable human docs; persist evidence separately and return concise summaries/paths.
- Do not chain Skills mechanically. Specialist review/legibility Skills run only when triggered.

## Hard rules

- Never claim success without fresh verification evidence from the current revision.
- Never weaken/delete/skip a failing check merely to get green status.
- Never invent commands, dependencies, APIs, data, environment variables, product requirements, or historical rationale.
- Functional-spec compliance is insufficient when a material Quality Envelope gap remains.
- Add negative/invariant criteria where failure, cross-user behavior, duplicates/concurrency, compatibility, recovery, or resource limits matter.
- For MATERIAL/CRITICAL Knowledge Impact, leave durable evidence that a fresh maintainer can understand the change without the original AI session.
- Label material rationale `RECORDED`, `DERIVED`, or `INFERRED`; never present post-hoc inference as historical fact.
- Human approval is for desired consequences/tradeoffs, not unfamiliar technology or documentation readiness alone.
- If a blocking unknown or CRITICAL readiness gap remains, do not release.

## Commands

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
```
