# AI Development Harness

This repository is designed for agent-led development with machine-verifiable quality gates and minimal, meaningful human approval.

## Source of truth

Read only the documents relevant to the task:

- Product intent and user outcomes: `docs/PRODUCT.md`
- Architecture and dependency boundaries: `docs/ARCHITECTURE.md`
- Security and data handling: `docs/SECURITY.md`
- UI and visual language: `docs/DESIGN.md`
- Reliability, observability, rollback: `docs/RELIABILITY.md`
- Risk levels and human approval policy: `ai/policies/risk-policy.md`
- Required quality gates: `ai/policies/quality-gates.md`

## Mandatory workflow

1. For a new or adopted repository, use the `bootstrap-project` skill first.
2. For feature work, use `develop-feature`.
3. Classify risk before release. `./scripts/ai/classify-risk` is the deterministic risk floor; an agent may raise risk but must not lower it without an explicit human decision recorded in the PR.
4. Before claiming completion, use `verify-work` and run `./scripts/ai/verify --risk <green|yellow|red>`.
5. For meaningful changes, obtain an independent review using `review-code`; use `review-security` for security-sensitive changes and `review-design` for user-facing visual work.
6. For any decision requiring human judgment, use `prepare-approval`. Never ask a human to guess about technical correctness.
7. For release/deployment work, use `release-change`.

## Hard rules

- Never claim success without fresh verification evidence from the current revision.
- Never weaken, delete, skip, or rewrite a failing test solely to make CI green.
- Never bypass a required quality gate.
- Never invent commands, dependencies, APIs, environment variables, data, or product requirements. Verify them from the repository or authoritative sources.
- Prefer the smallest change that satisfies the written acceptance criteria. Avoid speculative abstractions and unrelated refactors.
- Keep technical correctness machine-verifiable where possible. Human approval is for desired consequences, business tradeoffs, visual judgment, and genuinely non-automatable risk acceptance.
- If a reviewer would need specialist knowledge they cannot reasonably be expected to have, do not request a cosmetic approval. Escalate, obtain independent evidence, or choose a safer reversible design.
- If a blocking unknown remains, do not release.

## Standard commands

```sh
./scripts/ai/self-test
./scripts/ai/classify-risk
./scripts/ai/verify --risk green
./scripts/ai/verify --risk yellow
./scripts/ai/verify --risk red
```

Project-specific verification commands live in `ai/commands.conf`.
