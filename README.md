# AI Dev Harness V4.1

A portable, composition-oriented harness for AI-led software development.

V4 keeps deterministic evidence, explicit Human Checks, durable project knowledge, and mutual verification while replacing the V3 fixed workflow with profiles, semantic capabilities, swappable providers, and inspectable execution plans.

The repository is the system of record.
The original AI conversation should be disposable.

## What V4 adds

- **Profiles** tune delivery speed, autonomy, human understanding, handoff depth, attention, and context efficiency without weakening mandatory constraints.
- **Capabilities** describe what the Harness needs semantically.
- **Providers** implement capabilities through existing scripts, Skills, or host-native behavior.
- **Execution plans** record what was selected, what provider supplies it, and why.
- **Run events** record bounded operational facts without raw prompts, completions, secrets, or private reasoning.
- **Project Dashboard** shows project status, explains the Harness structure through actual runs, and exposes retries/fallbacks/context events for Harness improvement.

## Start

For a project created from this template:

```sh
python3 scripts/ai/v4.py init
./scripts/ai/self-test
python3 scripts/ai/v4.py plan --task implement --risk GREEN
python3 scripts/ai/v4.py dashboard
```

The project-local Dashboard opens at `http://127.0.0.1:4310` by default.

### Normal implementation

```sh
python3 scripts/ai/v4.py plan --task implement
# execute only the capabilities/providers selected by the plan
python3 scripts/ai/v4.py verify --run-id <run-id>
python3 scripts/ai/v4.py finish --run-id <run-id>
```

Material routing inputs can be added explicitly:

```sh
python3 scripts/ai/v4.py plan \
  --task implement \
  --quality security \
  --knowledge-impact MATERIAL
```

## Dashboard

The Dashboard uses three stable views.

- **作業**: what is happening, what verification passed, what changed, and what a human still needs to check.
- **仕組み**: which Harness components were used, their roles, provider implementations, and machine-readable selection reasons.
- **診断**: run timeline, retries, fallbacks, context compaction, anomalies, execution plan, and raw bounded events.

The Dashboard renderer does not call an LLM.
Explanation text comes from `ai/v4/self-description.json`.
Runtime facts come from structured events and read models.

## Repository layout

```text
AGENTS.md
PROJECT_MAP.md

ai/
  v4/
    capabilities.md
    profiles/
    provider-registry.json
    self-description.json
  schemas/
  policies/
  templates/

scripts/ai/
  v4.py
  dashboard/
  lib/v4_core.py
  lib/v4_dashboard.py
  verify
  classify-risk
  validate-assurance
  ...

.harness/
  dashboard.json          # created per adopted project

.ai-artifacts/
  runs/                   # execution plans + bounded events
  dashboard/              # generated read model
  verification/           # deterministic evidence
  reviews/
  traces/
  index/
```

`.ai-artifacts/` is generated and uncommitted.

## Trust model

V4 keeps distinct:

- deterministic machine evidence;
- non-decisive AI review;
- Human Checks;
- runtime traces;
- durable knowledge;
- release/readiness evaluation.

Do not collapse them into a single confidence or quality score.

A required capability cannot silently disappear when a provider fails.
A profile cannot reduce the deterministic risk floor or remove a mandatory Claim, Evidence requirement, Human Check, security requirement, or release constraint.

## Existing V3 assets

V3 is no longer the authoritative orchestration model.

Useful V3-era assets such as `scripts/ai/verify`, assurance validation, evidence recording, review Skills, and legibility procedures are retained as V4 providers.
They can be replaced incrementally behind capability contracts without changing the whole Harness at once.

See `ai/v4/README.md` and `docs/decisions/2026-09-15-v4-composable-harness-architecture.md` for architecture details.


## Existing team repository: Sidecar Mode

V4.1 can observe and adapt to an existing team's collaboration conventions without adding Harness-only files to the target repository.

```sh
python3 scripts/ai/team-compat.py --repo /path/to/team-repo observe
python3 scripts/ai/team-compat.py --repo /path/to/team-repo show
python3 scripts/ai/team-compat.py --repo /path/to/team-repo guard --surface commit --file /tmp/commit-message.txt
```

State is external under `$HARNESS_STATE_HOME/repositories/<fingerprint>/` or `~/.local/state/ai-dev-harness/repositories/<fingerprint>/`.

Team conventions may change representation but never weaken verification. Explicit AI-use disclosure, DCO/sign-off, authorship, or other team requirements are preserved.

See `ai/v4/team-compatibility.md`.
