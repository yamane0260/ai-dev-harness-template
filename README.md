# AI Development Harness V5 — Evidence Loop

V5 is a lightweight worker harness for AI-supervised development.

Its optimization target is not to make every implementation attempt perfect. It is to reach realistic acceptance quickly, expose mismatches with evidence, classify the failure, and return to the correct layer.

```text
Human <-> Supervisor AI <-> V5 Worker <-> Implementation
                           |
                           +-> worker evidence -> fresh Verifier -> acceptance evidence
                                                   |
                                                   +-> classified failure -> next action
```

## Core loop

1. Supervisor creates a bounded Acceptance Contract.
2. Worker runs preflight, loads bounded context, implements, and produces evidence.
3. Worker handoff is blocked by stale evidence, missing evidence kinds, or contract drift.
4. A fresh verifier receives a compact verifier packet, not the worker reasoning transcript.
5. The verifier proves acceptance, invariants, and baseline compatibility from direct evidence.
6. Failure is classified before any retry.
7. Loop Guard chooses retry, fresh diagnosis, design return, oracle repair, environment repair, requirement clarification, or supervisor review.

## Main commands

```sh
python3 scripts/ai/v5.py validate-task --task ai/v5/examples/task.json
python3 scripts/ai/v5.py preflight --task ai/v5/examples/task.json
python3 scripts/ai/v5.py validate-scan --scan ai/v5/examples/scan.json
python3 scripts/ai/v5.py verify --task ai/v5/examples/task.json --scan ai/v5/examples/scan.json
python3 scripts/ai/v5.py verifier-packet --task <task> --preflight <preflight> --verification <verification>
python3 scripts/ai/v5.py guard-acceptance --task <task> --preflight <preflight> --packet <packet> --verdict <verdict>
python3 scripts/ai/v5.py next-action --classification <failure-classification> --risk GREEN
```

See `ai/v5/README.md` and `ai/v5/architecture.md`.