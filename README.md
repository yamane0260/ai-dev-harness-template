# AI Dev Harness Template — Responsibility-transfer V3.0

A tool-portable starter for AI-led software development that balances **quality, inspectable assurance, context efficiency, and human responsibility**.

The repository, not chat history, is the system of record. Codex, Cursor, Claude Code, and future agents should use the same project knowledge, deterministic checks, Claim/Evidence relationships, explicit Human Checks, risk policy, and durable change records.

For a human trying to find something, start with [`PROJECT_MAP.md`](PROJECT_MAP.md).

## Core principles

1. One task = one fresh top-level session whenever practical.
2. `develop-feature` is the primary workflow Skill; avoid mechanical Skill chaining.
3. Read only relevant context via `ai/context-map.md`.
4. Delegate broad exploration early; return compact Task Packets, not transcripts.
5. Quality Envelope catches cases where the functional spec can pass but the product/system is still wrong.
6. Completion for non-trivial work means code + current evidence + explicit remaining Human Checks + durable knowledge.
7. Raw logs/transcripts stay out of the main context and durable human docs; keep them under `.ai-artifacts/` and retrieve summaries first.
8. Human approval, human verification, and human understanding are separate. Do not interrupt work merely because the implementation uses unfamiliar knowledge.
9. Record compact facts and relationships during work; generate reader-appropriate explanations on demand.
10. Agent traces describe access and actions. They do not prove the generated product is correct.

## Four independent classifications

- **Work mode** — MICRO / STANDARD / CRITICAL: orchestration/context.
- **Risk** — GREEN / YELLOW / RED: evidence/release controls.
- **Quality Impact** — routes UX/security/data/reliability/etc. checks.
- **Knowledge Impact** — NONE / LOW / MATERIAL / CRITICAL: durable human-understanding requirements.

A small code change may be high-risk; a safe change may still have MATERIAL knowledge impact. Do not conflate the axes.

Assurance adds independent facets rather than a fifth score: `MACHINE_VERIFIED`, `AI_REVIEWED`, `HUMAN_REQUIRED`, `HUMAN_VERIFIED`, `UNVERIFIED`, and `N/A`. A single Claim may have more than one facet.

## Repository layout

```text
AGENTS.md
PROJECT_MAP.md             # human entry point

docs/
  README.md
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

assurance/
  README.md
  current/       # active Claim/Evidence/Human Check records
  changes/       # retained historical assurance records

.agents/skills/
  bootstrap-project/
  develop-feature/
  spec-gap-preflight/
  review-code/
  review-security/
  review-ux/
  review-design/
  explain-change/
  explain-system/
  review-assurance/
  review-legibility/
  prepare-approval/
  release-change/

ai/
  context-map.md
  quality-envelope.md
  commands.conf
  policies/
    assurance.md
    adaptive-explanation.md
    agent-control.md
    human-legibility.md
  schemas/
  templates/
    assurance/
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
  validate-assurance
  record-evidence
  build-project-index
  record-agent-event
  validate-agent-trace
  validate-approval
```

## Normal development flow

```text
request
  -> work/risk/quality routing
  -> focused exploration + Task Packet
  -> Requirement -> Claim -> expected Evidence / Human Check
  -> implementation
  -> deterministic verification -> exact-run evidence.json
  -> assurance readiness calculation
  -> targeted specialist review when triggered
  -> Knowledge Impact classification
       NONE     -> nothing extra
       LOW      -> short inline Change Record
       MATERIAL -> Change Brief -> fresh legibility review
       CRITICAL -> Change Brief + applicable runbook -> fresh legibility review
  -> approval only if a real human decision remains
```

### Claim-based assurance

For STANDARD/CRITICAL or YELLOW/RED work, copy `ai/templates/assurance/` into `assurance/current/<change-id>/`. The committed files say what must be true and how it can be established; the verifier records what actually ran.

```sh
./scripts/ai/validate-assurance \
  --manifest assurance/current/<change-id>/manifest.json

./scripts/ai/verify \
  --risk yellow \
  --assurance assurance/current/<change-id>/manifest.json

./scripts/ai/verify \
  --risk yellow \
  --assurance assurance/current/<change-id>/manifest.json \
  --release
```

The release form fails if required evidence is missing/stale/failing or a MUST Human Check is incomplete. An AI review can be required, but never counts as decisive machine proof by itself.

### Human Legibility

The goal is not to make humans watch the agent work. The goal is to make the system understandable **after** autonomous work completes and to expose exactly where automation stops.

For MATERIAL/CRITICAL changes, `explain-change` generates records from observable evidence: diff, tests, config, recorded decisions, and current docs. Material rationale is labeled:

- `RECORDED` — explicitly captured during the task;
- `DERIVED` — directly supported by durable evidence;
- `INFERRED` — after-the-fact interpretation, never presented as historical fact.

`review-legibility` performs the **AI Absence Test** in a fresh context without the original transcript: can a maintainer explain what changed, why, critical invariants, where to modify it, and how to diagnose/recover? A CRITICAL blocking readiness gap prevents release, but does not automatically create a human approval request.

`explain-system` uses the derived relationship index and optional local `.harness-user.json` to explain at the reader's familiarity level. Familiarity changes explanation volume only; it never weakens tests, Claims, or release gates.

### Derived project index and future Explorer UI

```sh
./scripts/ai/build-project-index
```

This creates `.ai-artifacts/index/project-index.json` from docs and assurance records. It supports system → component → Claim → evidence drill-down without making a graph database or UI a second source of truth. A future Harness Explorer should read this index; the initial V3 deliberately establishes reliable data before adding a graphical interface.

### Agent action traces

Hosts or wrappers can emit sanitized events through `scripts/ai/record-agent-event` and validate/summarize them with `scripts/ai/validate-agent-trace`. Coverage is always reported as host/declaration coverage, never assumed complete. Payloads, secrets, chain-of-thought, and full command output are excluded.

## Bootstrap

After creating a real project from this template, use `bootstrap-project`. Configure real project commands/docs without inventing dependencies or checks, confirm Python 3 is available for the standard-library-only assurance utilities, remove `ai/TEMPLATE_MODE` only when ready, then run:

```sh
./scripts/ai/self-test
./scripts/ai/verify --risk green
```

## Suggested normal prompt

```text
Use develop-feature for this request. Optimize for context efficiency and apply the Quality Envelope. For non-trivial work, map requirements to observable Claims, decisive evidence, and explicit Human Checks. Keep exploration in compact Task Packets and store only non-reconstructable knowledge. After exact-revision verification, report assurance readiness and Knowledge Impact. Do not ask me to approve technical correctness.
```

## Verification and evidence

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
./scripts/ai/validate-assurance --manifest assurance/current/<change-id>/manifest.json
./scripts/ai/build-project-index
```

Each real-project verification run writes `summary.md`, `evidence.json`, gate logs, and optional `readiness.json` below `.ai-artifacts/verification/<UTC>/`. Raw verification output and agent traces remain separate from human-facing docs and are not committed.

Maintainers of this template can run its own RED gate set without activating product commands:

```sh
./scripts/ai/verify --harness --risk red
```

`--harness` verifies only the template mechanics. It must never be used as evidence that an adopted product was tested.

## No-Guess Approval

Approval packets remain only for genuine business/product/risk decisions. `READINESS` is not `APPROVAL`: a change may require a runbook or legibility evidence while needing no human go/no-go.

## Portability

```text
current knowledge   -> docs/ + AGENTS.md
historical knowledge-> docs/changes + docs/decisions
operational knowledge -> docs/runbooks
assurance intent    -> assurance/
run evidence        -> .ai-artifacts/verification/
agent audit         -> .ai-artifacts/traces/
derived relationships -> .ai-artifacts/index/
workflow            -> .agents/skills/
context routing     -> ai/context-map.md + task-packet.md
enforcement         -> scripts/ai/ + CI
quality routing     -> ai/quality-envelope.md
human legibility    -> ai/policies/human-legibility.md
assurance semantics -> ai/policies/assurance.md
```

The original AI session should be disposable. The repository should remain understandable and operable without it.
