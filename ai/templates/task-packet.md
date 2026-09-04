# Task Packet

Use when handing context from an explorer/coordinator/preflight to an implementer or reviewer. Keep it compact; normally 15–30 lines plus paths.

## Goal
One sentence describing the requested outcome.

## Observable acceptance criteria
- Positive behavior: ...
- Negative/invariant criteria only where material: ...

## Assurance Claims (STANDARD/CRITICAL or YELLOW/RED)
- Requirement -> observable Claim IDs; omit only when the change is genuinely MICRO/GREEN/LOW.
- Decisive machine gate or Human Check expected for each MUST Claim.

## Relevant files
- `path`: why it matters

## Relevant constraints
- Only constraints that materially affect this task.

## Quality Impact Vector
List only MATERIAL/CRITICAL domains with one short reason. UI Impact: NONE / COSMETIC / INTERACTION / STRUCTURAL.

## Knowledge Impact (provisional)
- NONE / LOW / MATERIAL / CRITICAL
- Reason only for MATERIAL/CRITICAL: what new knowledge a future maintainer may need.

Final Knowledge Impact is confirmed after implementation; do not create docs from a speculative provisional classification.

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

Do not include broad search transcripts, full files, raw logs/screenshots, hidden reasoning, or general repository history. Open only listed evidence and expand context when required.
