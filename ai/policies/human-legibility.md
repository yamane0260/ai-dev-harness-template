# Human Legibility Policy

AI autonomy and human understanding are separate concerns. Do not interrupt autonomous work merely to explain it, but do leave enough durable evidence that a human or fresh agent can understand, maintain, and recover the system later.

## Three separate layers

1. **Audit evidence** — raw/tool-level evidence such as verification logs, CI artifacts, traces, and agent/tool telemetry. Keep this out of normal human-facing docs and out of Git when it may contain sensitive/transient data.
2. **Durable knowledge** — concise repository records explaining material changes, decisions, concepts, invariants, and runbooks.
3. **Approval** — only for a real human decision or risk acceptance. Unfamiliarity alone is not an approval trigger.

## Knowledge Impact

Classify independently from Work Mode, Risk, and Quality Impact:

- **NONE** — no new maintainer knowledge; cosmetic/trivial change.
- **LOW** — local change using established project patterns; a short completion/PR breadcrumb is enough.
- **MATERIAL** — introduces a non-obvious concept, dependency, integration, cross-layer behavior, data rule, failure mode, or architectural constraint a future maintainer must understand.
- **CRITICAL** — introduces or changes knowledge needed to safely operate, secure, recover, migrate, or restore an important system under failure or incident conditions.

Knowledge Impact asks: **If the original AI session disappeared, would a future maintainer need new knowledge to safely change or operate this system?**

## Required output by level

| Impact | Durable output | Independent legibility review |
|---|---|---|
| NONE | none | no |
| LOW | short PR/completion Change Record | no |
| MATERIAL | `docs/changes/...` Change Brief; canonical concept/decision only if reusable | yes, fresh context when supported |
| CRITICAL | Change Brief + applicable current-source doc/runbook | yes; readiness gap can block release |

Do not create one document per concept per change. Prefer links to existing canonical docs.

## Rationale provenance

Any statement answering **why** must be labeled when material:

- **RECORDED** — explicitly documented during the work in a spec, issue, decision, or task record.
- **DERIVED** — directly supported by code, tests, configuration, or current project docs.
- **INFERRED** — plausible after-the-fact interpretation. Never present this as historical fact.

Do not expose or store private chain-of-thought. Preserve decisions and evidence, not hidden reasoning traces.

## Human attention

Understanding does not imply interruption:

- **RECORD** — preserve the breadcrumb only.
- **AWARE** — mention the knowledge delta in 1–3 lines at completion.
- **READINESS** — durable docs/runbook must exist because a human may need the knowledge during maintenance or incidents.

`READINESS` is not `APPROVAL`. A technically verifiable change may require readiness documentation without requiring a human go/no-go.

## AI Absence Test

For MATERIAL/CRITICAL changes, a fresh maintainer should be able to determine from durable repository evidence:

1. what changed;
2. why the approach is used, with provenance;
3. what invariants/failure modes must be preserved;
4. where to look for the likely next modification;
5. how to detect, diagnose, and recover if the change fails.

If the answer depends on the original chat/transcript, improve the durable docs. For CRITICAL operational knowledge, a blocking readiness gap prevents release.

## Context efficiency

- Do not paste raw transcripts/logs into Change Briefs.
- Generate human records from the diff, tests, config, recorded decisions, and verification evidence.
- Link to canonical docs instead of repeating tutorials.
- Keep LOW records inline; only MATERIAL/CRITICAL create standalone change docs.
- Specialist legibility review receives the Change Brief + relevant diff/docs, not the original agent history.
