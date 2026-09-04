# Risk Policy

Risk controls evidence/release requirements. It does **not** control how much context an agent should load. Context/orchestration is separately classified as MICRO / STANDARD / CRITICAL in `AGENTS.md` and `develop-feature`.

A tiny auth change can therefore be CRITICAL/RED, while a broad but low-consequence refactor may be STANDARD/GREEN or YELLOW.

## General rules

1. `./scripts/ai/classify-risk` provides a deterministic **risk floor** from the diff.
2. An agent may raise risk based on consequences or uncertainty.
3. An agent must not lower the deterministic floor without an explicit human decision recorded in the PR.
4. Unknowns increase risk. A blocking unknown prevents release.
5. Risk is about consequences, not code size or context size.

## GREEN

Typical examples: documentation/comments, formatting, behavior-preserving internal refactors, low-impact developer tooling, or tests that do not alter product behavior.

Expected handling: required GREEN gates pass; no human approval solely for process compliance.

## YELLOW

Typical examples: user-visible behavior, API contracts, additive schema changes, new dependencies, data transformations, significant UI/layout changes, or reversible external integration changes.

Expected handling: required YELLOW gates pass; independent review when uncertainty/consequence warrants it; human approval only for remaining business/UX tradeoffs.

## RED

Typical examples: authentication/authorization, security controls, destructive/irreversible DB changes, sensitive-data exposure/retention, payments, production infrastructure/deployment policy, bulk external side effects, production-data deletion, or this harness's enforcement policy.

Expected handling: required RED gates pass; relevant independent specialist review; rollback/recovery evidence; No-Guess Approval before irreversible action/release; explicit human go/no-go for the consequence.

For YELLOW/RED release mode, use an assurance manifest. The final risk must be at least the deterministic floor and at least the manifest risk; evidence from a lower risk gate set is not sufficient. `READY` is scoped to declared Claims and does not lower the risk classification.

## Expertise Gate

Do not ask a non-expert to certify a technical claim they cannot reasonably evaluate. Identify missing expertise, seek independent evidence/expert review where available, otherwise choose a safer standard/reversible design or postpone the risky action.

## No-Guess Approval

A human approval request must state the exact decision, why AI/machine checks cannot decide it, minimum background knowledge, user/business consequences, verification evidence, assumptions/unknowns, worst case, rollback/recovery, alternatives, recommendation, and strongest argument against that recommendation.
