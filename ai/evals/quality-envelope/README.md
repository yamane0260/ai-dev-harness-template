# Quality Envelope Evals

These cases are lightweight regression prompts for checking whether a new model/tool still detects specification gaps without loading unnecessary context.

Expected behavior:

- identify only material quality domains;
- add negative/invariant criteria when needed;
- avoid ceremonial concerns unrelated to the task;
- classify STRUCTURAL UI and require a UX Contract;
- escalate to a human only for genuine product/business decisions.

## Case 001 — Settings sprawl

Input: "Add twelve configuration options to the Settings page exactly as listed."

Expected: UX MATERIAL, UI Impact STRUCTURAL; do not simply render twelve equal controls. Require grouping, defaults, advanced disclosure, task-local-vs-global assessment, and representative task audit.

## Case 002 — Retried external side effect

Input: "When payment succeeds, call the fulfillment webhook."

Expected: reliability/data/security MATERIAL or CRITICAL as project context dictates; define timeout/retry/idempotency/duplicate-side-effect invariants and observability. Functional success-path testing alone is insufficient.

## Case 003 — Additive schema field

Input: "Add a required `display_name` column and update the app to use it."

Expected: compatibility/migration and data integrity MATERIAL; consider existing rows, rollout coexistence, backfill/default strategy, rollback/forward recovery. Do not assume empty/new database.
