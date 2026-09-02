---
name: review-ux
description: Independently review user-facing interaction and information architecture for real-world usability rather than visual fidelity alone. Use for STRUCTURAL or meaningful INTERACTION UI changes, settings/navigation/forms/workflows, or whenever a feature can satisfy the written spec yet still be confusing, misplaced, overly complex, unfamiliar, or hard to recover from.
---

# Review UX

Use a fresh context when supported. Start from the Task Packet, UX Contract, rendered product, and only the relevant paths/docs.

1. Judge the workflow as a user task, not as a source-code implementation.
2. Check findability, grouping, priority, defaults, progressive disclosure, control semantics, predictability, feedback, recovery, and accessibility-in-use.
3. Prefer interaction conventions in this order: existing product pattern, existing design-system component, platform convention, established product-category convention, then custom interaction.
4. For settings, ask whether each option belongs in global settings at all; prefer sensible defaults and task-local controls when appropriate.
5. For STRUCTURAL UI, exercise representative tasks in the rendered product/browser when possible. Do not treat screenshots alone as sufficient UX evidence.
6. Report only material findings with severity, affected task, consequence, and a concrete correction. Keep raw browsing traces/screenshots outside the parent context.
7. Human review is only for unresolved product/brand tradeoffs, not for discovering basic usability defects that this review can identify.
