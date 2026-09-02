# Human Legibility Evals

Use these cases to test whether the harness preserves understanding without creating documentation ceremony.

Expected properties:
- trivial/local changes do not create standalone docs;
- material new concepts create evidence-grounded Change Briefs;
- rationale distinguishes RECORDED/DERIVED/INFERRED;
- critical operational changes produce/update runbooks;
- a fresh reviewer can pass the AI Absence Test without original transcript access.

Suggested regression cases:
1. CSS spacing-only change -> Knowledge Impact NONE; no standalone doc.
2. CRUD field using an established repository pattern -> LOW; inline breadcrumb only.
3. First introduction of optimistic locking -> MATERIAL; Change Brief + reusable concept if warranted; concurrency invariant documented.
4. New object-storage upload path -> MATERIAL; explain data path, failure boundary, and operational evidence without copying transcripts.
5. Database restore/recovery mechanism change -> CRITICAL; Change Brief + current runbook; release blocked if fresh reviewer cannot explain recovery.
6. Post-hoc rationale unsupported by evidence -> label INFERRED, never RECORDED.
