# AI Development Harness V3

Optimize for correctness, real-world quality, context efficiency, and durable human responsibility transfer. A non-trivial change is complete only when its implementation, assurance state, required human checks, and durable knowledge are discoverable without the original AI session.

## Start here

- New/adopted repo: use `bootstrap-project`.
- Product change: use `develop-feature` as the primary workflow skill.
- Before non-trivial implementation, apply `ai/quality-envelope.md`; use `spec-gap-preflight` when triggered.
- Read `ai/context-map.md` before loading project docs.
- Human entry point: `PROJECT_MAP.md`.
- Assurance policy: `ai/policies/assurance.md`; manifests live under `assurance/`.
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
- Record non-reconstructable facts and relationships during implementation; generate audience-appropriate prose only when it is needed.
- Do not chain Skills mechanically. Specialist review/legibility Skills run only when triggered.

## Hard rules

- Never claim success without fresh verification evidence from the current revision.
- Never use `AI_REVIEWED` as a synonym for `MACHINE_VERIFIED`.
- A declared MUST Claim must have current evidence or an explicitly linked, completed human check. Unverified critical Claims block release.
- A pending or failed MUST Human Check blocks release. Explanation familiarity never relaxes this rule.
- Never weaken/delete/skip a failing check merely to get green status.
- Never invent commands, dependencies, APIs, data, environment variables, product requirements, or historical rationale.
- Functional-spec compliance is insufficient when a material Quality Envelope gap remains.
- Add negative/invariant criteria where failure, cross-user behavior, duplicates/concurrency, compatibility, recovery, or resource limits matter.
- For MATERIAL/CRITICAL Knowledge Impact, leave durable evidence that a fresh maintainer can understand the change without the original AI session.
- Label material rationale `RECORDED`, `DERIVED`, or `INFERRED`; never present post-hoc inference as historical fact.
- Human approval is for desired consequences/tradeoffs, not unfamiliar technology or documentation readiness alone.
- If a blocking unknown or CRITICAL readiness gap remains, do not release.
- Treat runtime agent traces as audit evidence, not as proof that the generated result is correct. Never fabricate host events when instrumentation is unavailable.

## Commands

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
./scripts/ai/validate-assurance --manifest assurance/current/<change>/manifest.json
./scripts/ai/build-project-index
```
