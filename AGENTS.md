# AI Development Harness V5 — Evidence Loop

V5 is a lightweight implementation harness used under a supervisor AI. The supervisor owns human communication, cross-task planning, integration, release authority, Acceptance Contract revision, verifier allocation, and failure-loop decisions.

## Worker flow

1. Receive a Task Envelope with goal, acceptance criteria, invariants, optional baseline assertions, scope, and required evidence kinds.
2. Run `python3 scripts/ai/v5.py preflight --task <task.json>`.
3. Load only returned `contextRefs` plus code actually needed.
4. Complete the five-lens Perspective Scan.
5. Implement the smallest coherent change satisfying the Acceptance Contract.
6. Run `verify`; never manufacture or weaken evidence.
7. Return a Result Envelope and pass `guard-result`.
8. Stop. Independent acceptance belongs to a fresh verifier context.

## Kernel invariants

- No claim without current evidence.
- Never weaken tests, acceptance criteria, invariants, baseline checks, gates, or safety constraints merely to obtain green.
- Never invent APIs, requirements, commands, observations, team rules, or historical rationale.
- Risk may move upward, never downward inside the worker.
- Happy-path correctness is insufficient when material operational, maintenance, compatibility, security, data, UX, reliability, or cost problems remain.
- Consequential ambiguity is escalated rather than guessed through.
- Do not consume verifier hold-out cases or acceptance reasoning.
- Worker self-report is not acceptance evidence.

## Failure loop

Classify failed acceptance as `implementation`, `design`, `requirement`, `oracle`, `environment`, or `unknown` before changing code again. Repeated same failures, regressions, and repeated design churn trigger reset or supervisor review rather than indefinite patching.

## Completion

`implemented` means worker implementation plus worker-side evidence passed for the exact Acceptance Contract and repository state. It does not mean independently accepted, integrated, release-ready, or human-approved.