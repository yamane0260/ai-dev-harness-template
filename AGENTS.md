# AI Development Harness V5 — Worker Core

V5 is a lightweight harness for implementation agents supervised by another AI.
The supervisor owns human communication, planning across workers, integration, approval, release decisions, and long-term project explanation.
The worker owns only its assigned implementation scope and evidence-backed handoff.

## Worker flow

1. Receive a bounded Task Envelope.
2. Run `python3 scripts/ai/v5.py preflight --task <task.json>`.
3. Load only the returned `contextRefs` plus code needed for the task.
4. Complete the five-lens Perspective Scan before or during implementation.
5. Implement the smallest coherent change that satisfies acceptance criteria and constraints.
6. Run `python3 scripts/ai/v5.py verify --task <task.json> --scan <scan.json>`.
7. Return a Result Envelope and pass `guard-result` before reporting `implemented`.

## Kernel invariants

- Never claim `implemented` without current-repository verification for every required gate.
- Never weaken tests, requirements, gates, or safety constraints merely to obtain a passing result.
- Never invent APIs, requirements, commands, observations, or historical rationale.
- Deterministic risk floors may be raised but never lowered by the worker.
- A technically working solution is insufficient if it creates a material operational, maintenance, UX, data, security, or reliability problem.
- Unresolved uncertainty is returned to the supervisor; do not silently guess through consequential ambiguity.

## Perspective Scan

Always examine exactly these lenses:

- `correctness`
- `boundary`
- `failure`
- `work_fit`
- `simplicity`

Only load a domain capsule when preflight or the scan triggers it. Do not load all V5 documents by default.

## Meaning of completion

`implemented` means the worker completed the assigned change and its required local verification.
It does **not** mean release-ready, approved, production-safe in every dimension, or accepted by a human.
Those judgments belong to the supervisor/integration layer.
