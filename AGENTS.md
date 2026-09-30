# AI Development Harness V4

Optimize for correctness, context efficiency, inspectable composition, durable human understanding, and explicit responsibility transfer.

V4 is the authoritative runtime model. Existing V3 verification, assurance, review, and knowledge assets remain available as V4 providers where they preserve useful behavior.

## Start here

- New/adopted repository: use `bootstrap-project`.
- Product change: use `develop-feature`.
- Human project view: run `python3 scripts/ai/v4.py dashboard`.
- V4 contracts and architecture: `ai/v4/`.
- Human repository map: `PROJECT_MAP.md`.
- Deterministic verification: `scripts/ai/verify`.
- Assurance state: `assurance/`.

## V4 composition rule

For non-trivial work, compile a V4 execution plan before implementation.

```sh
python3 scripts/ai/v4.py plan --task implement
```

Add only the material routing inputs that actually apply, for example:

```sh
python3 scripts/ai/v4.py plan \
  --task implement \
  --quality security \
  --knowledge-impact MATERIAL
```

The execution plan selects semantic capabilities first and concrete providers second.
Load provider instructions only after selection.
Do not mechanically run every available Skill.

## Independent inputs

Keep these inputs separate.

- **Risk**: GREEN / YELLOW / RED. Deterministic minimum safety and evidence floor.
- **Quality Impact**: only domains materially affected by the task.
- **Knowledge Impact**: NONE / LOW / MATERIAL / CRITICAL.
- **Profile**: optimization preferences such as rapid, balanced, understanding, or high-assurance.
- **Human Understanding Requirement**: what the responsible maintainer must be able to understand.

A profile may optimize speed, autonomy, explanation depth, or context use.
It may not weaken a required risk, security, Claim, Evidence, Human Check, or release constraint.

## Context rules

- Prefer one task per fresh top-level session.
- Use the execution plan and `ai/context-map.md` to load only relevant sources.
- Keep broad exploration isolated when possible and return bounded structured results.
- Keep raw logs, transcripts, screenshots, large tool output, and private reasoning outside parent context.
- Load full provider instructions only for selected providers.
- Preserve non-reconstructable decisions, invariants, and failure/recovery knowledge in durable project records.

## Hard rules

- Never report successful completion without current-revision support.
- Never silently omit or downgrade a required capability after provider failure.
- Keep `AI_REVIEWED` distinct from `MACHINE_VERIFIED`.
- A pending or failed MUST Human Check blocks readiness when that check is required.
- Never weaken tests, requirements, or gates merely to obtain green status.
- Never invent commands, dependencies, APIs, observations, requirements, or historical rationale.
- Treat traces as action/audit evidence, not proof of product correctness.
- Do not persist raw prompts, raw completions, secrets, credentials, or private reasoning in the V4 run ledger.
- Human approval is reserved for decisions that technical verification cannot determine.

## Runtime records

V4 separates:

- execution plan and provider selection;
- append-only run events;
- deterministic evidence;
- structured reviews;
- Human Checks;
- durable project knowledge;
- Dashboard read models.

Dashboard data must be derived from structured runtime records.
Dashboard rendering must not require an LLM.

## Commands

```sh
python3 scripts/ai/v4.py init
python3 scripts/ai/v4.py plan --task implement
python3 scripts/ai/v4.py state --write
python3 scripts/ai/v4.py dashboard

./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/validate-assurance --manifest assurance/current/<change>/manifest.json
```

Apply `ai/policies/mutual-verification.md` when humans and agents disagree materially.
Resolve disagreements through requirements, implementation, tests, or observations rather than defaulting to documentation repair.
