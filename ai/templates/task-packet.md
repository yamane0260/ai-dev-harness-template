# Task Packet

Use this format when handing context from an explorer/coordinator/preflight to an implementer or reviewer. Keep it compact; normally 15–30 lines plus file paths.

## Goal
One sentence describing the requested outcome.

## Observable acceptance criteria
- Positive behavior: ...
- Negative/invariant criteria only where material: ...

## Relevant files
- `path`: why it matters

## Relevant constraints
- Only constraints that materially affect this task.

## Quality Impact Vector
- UX: NONE / LOW / MATERIAL / CRITICAL
- Security: ...
- Data integrity: ...
- Compatibility/migration: ...
- Reliability: ...
- Operability: ...
- Performance/cost/quota: ...
- Privacy: ...
- Architecture/maintainability: ...
- Accessibility: ...
- Supply chain: ...
- UI Impact: NONE / COSMETIC / INTERACTION / STRUCTURAL

Omit explanation for `NONE`; give one short reason for MATERIAL/CRITICAL entries.

## Existing pattern to follow
- Existing implementation/reference path, if any.

## Work mode / risk
- Mode: MICRO / STANDARD / CRITICAL
- Risk floor: GREEN / YELLOW / RED / not yet available
- Reason: ...

## Unknowns / decisions
- `None`, or only unresolved items that can change the result.

## Recommended next action
One short instruction to the receiving agent.

Do not include broad search transcripts, full file contents, raw test logs, screenshots, or general repository history. The receiving agent should open only the listed files and expand context only when evidence requires it.
