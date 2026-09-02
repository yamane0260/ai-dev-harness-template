# AI Dev Harness Template — Context-efficient V2.3

A tool-portable starter for AI-led software development that balances **quality, trust, context efficiency, and human legibility**.

The repository, not chat history, is the system of record. Codex, Cursor, Claude Code, and future agents should use the same project knowledge, deterministic checks, risk policy, compact task handoffs, and durable change records.

## Core principles

1. One task = one fresh top-level session whenever practical.
2. `develop-feature` is the primary workflow Skill; avoid mechanical Skill chaining.
3. Read only relevant context via `ai/context-map.md`.
4. Delegate broad exploration early; return compact Task Packets, not transcripts.
5. Quality Envelope catches cases where the functional spec can pass but the product/system is still wrong.
6. Raw logs/transcripts stay out of the main context and durable human docs; keep evidence as artifacts/telemetry where appropriate.
7. Human approval and human understanding are separate. Do not interrupt work merely because the implementation uses unfamiliar knowledge.
8. Human Legibility is proportional: LOW leaves a short breadcrumb; MATERIAL/CRITICAL leaves durable evidence a fresh maintainer can use.

## Four independent classifications

- **Work mode** — MICRO / STANDARD / CRITICAL: orchestration/context.
- **Risk** — GREEN / YELLOW / RED: evidence/release controls.
- **Quality Impact** — routes UX/security/data/reliability/etc. checks.
- **Knowledge Impact** — NONE / LOW / MATERIAL / CRITICAL: durable human-understanding requirements.

A small code change may be high-risk; a safe change may still have MATERIAL knowledge impact. Do not conflate the axes.

## Repository layout

```text
AGENTS.md

docs/
  PRODUCT.md
  ARCHITECTURE.md
  SECURITY.md
  DESIGN.md
  UX.md
  RELIABILITY.md
  specs/
  changes/       # historical material Change Briefs
  decisions/     # durable important decisions
  concepts/      # canonical project-specific concepts
  runbooks/      # current operational procedures

.agents/skills/
  bootstrap-project/
  develop-feature/
  spec-gap-preflight/
  review-code/
  review-security/
  review-ux/
  review-design/
  explain-change/
  review-legibility/
  prepare-approval/
  release-change/

ai/
  context-map.md
  quality-envelope.md
  commands.conf
  policies/
    human-legibility.md
  templates/
    task-packet.md
    change-record.md
    change-brief.md
    runbook.md
    approval-packet.md
  evals/

scripts/ai/
  self-test
  classify-risk
  verify
  validate-approval
```

## Normal development flow

```text
request
  -> work/risk/quality routing
  -> focused exploration + Task Packet
  -> implementation
  -> deterministic verification
  -> targeted specialist review when triggered
  -> Knowledge Impact classification
       NONE     -> nothing extra
       LOW      -> short inline Change Record
       MATERIAL -> Change Brief -> fresh legibility review
       CRITICAL -> Change Brief + applicable runbook -> fresh legibility review
  -> approval only if a real human decision remains
```

### Human Legibility

The goal is not to make humans watch the agent work. The goal is to make the system understandable **after** autonomous work completes.

For MATERIAL/CRITICAL changes, `explain-change` generates records from observable evidence: diff, tests, config, recorded decisions, and current docs. Material rationale is labeled:

- `RECORDED` — explicitly captured during the task;
- `DERIVED` — directly supported by durable evidence;
- `INFERRED` — after-the-fact interpretation, never presented as historical fact.

`review-legibility` performs the **AI Absence Test** in a fresh context without the original transcript: can a maintainer explain what changed, why, critical invariants, where to modify it, and how to diagnose/recover? A CRITICAL blocking readiness gap prevents release, but does not automatically create a human approval request.

## Bootstrap

After creating a real project from this template, use `bootstrap-project`. Configure real project commands/docs without inventing dependencies or checks, remove `ai/TEMPLATE_MODE` only when ready, then run:

```sh
./scripts/ai/self-test
./scripts/ai/verify --risk green
```

## Suggested normal prompt

```text
Use develop-feature for this request. Optimize for context efficiency and apply the Quality Envelope. Keep exploration in compact Task Packets. After verification, classify Knowledge Impact under the Human Legibility policy: do not interrupt me for explanation, but leave proportional durable records for material knowledge changes. Do not ask me to approve technical correctness.
```

## Verification and evidence

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
```

Raw verification output belongs under `.ai-artifacts/`; read summaries first. Audit telemetry/transcripts should remain separate from human-facing docs and must not be committed when they may contain sensitive/transient data.

## No-Guess Approval

Approval packets remain only for genuine business/product/risk decisions. `READINESS` is not `APPROVAL`: a change may require a runbook or legibility evidence while needing no human go/no-go.

## Portability

```text
current knowledge   -> docs/ + AGENTS.md
historical knowledge-> docs/changes + docs/decisions
operational knowledge -> docs/runbooks
workflow            -> .agents/skills/
context routing     -> ai/context-map.md + task-packet.md
enforcement         -> scripts/ai/ + CI
quality routing     -> ai/quality-envelope.md
human legibility    -> ai/policies/human-legibility.md
```

The original AI session should be disposable. The repository should remain understandable and operable without it.
