---
name: explain-change
description: Create or update evidence-grounded human-facing records of an AI-implemented software change. Use when a completed change has LOW/MATERIAL/CRITICAL Knowledge Impact, when the user asks what the agent changed or introduced, or when maintainers need a durable Change Record/Brief without reading the original agent transcript.
---

# Explain Change

Create durable project knowledge from observable evidence, without slowing implementation or inventing rationale.

1. Read `ai/policies/human-legibility.md`, the active assurance manifest when present, and the applicable change-record/change-brief template. Read only the changed diff, evidence summary, config, recorded decisions, and current project docs needed to explain the change.
2. Classify Knowledge Impact: `NONE`, `LOW`, `MATERIAL`, or `CRITICAL`.
3. For `LOW`, create a short inline Change Record in the PR/completion note; do not create a standalone file solely for ceremony. For `MATERIAL`/`CRITICAL`, create a Change Brief under `docs/changes/`; update a canonical `docs/concepts/`, `docs/decisions/`, or `docs/runbooks/` document only when the knowledge is reusable or operationally necessary.
4. Separate rationale provenance:
   - `RECORDED`: explicitly captured during the task in a decision/spec/issue.
   - `DERIVED`: directly supported by diff, tests, config, or current docs.
   - `INFERRED`: a plausible after-the-fact interpretation. Label it as inference; never present it as historical fact.
5. Explain project-specific meaning: what changed, what new concept a maintainer must know, where it lives, important invariants/failure behavior, which Claims are supported by which evidence/Human Checks, and what to watch when modifying it later.
6. Do not copy raw agent transcripts, chain-of-thought, large logs, secrets, or broad code dumps into documentation. Link to durable evidence paths instead.
7. Avoid duplicate tutorials. Reuse/link an existing canonical concept or decision record when one exists.
8. Keep the human-facing completion note short: knowledge impact, one-sentence knowledge delta, record path if any, and whether any human action is actually required.

Generate audience-specific teaching prose on demand through `explain-system`; do not expand every Change Brief for every possible experience level.

Human understanding is independent from approval. Do not ask for approval merely because a change introduces unfamiliar technology.
