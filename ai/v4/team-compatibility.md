# V4.1 Team Compatibility and Sidecar Mode

V4.1 adds an adoption mode for repositories already developed by a human team.

## Goals

- observe the team's explicit rules and repeated local Git conventions;
- keep Harness-only state outside the target repository;
- preserve V4 verification, review, evidence, and Human Check behavior;
- adapt team-visible branch, commit, pull-request, and comment surfaces;
- avoid exposing Harness-only implementation details unless the team explicitly wants them.

Team conventions may change **representation**. They must not weaken **verification**.

## Sidecar state

Run:

```sh
python3 scripts/ai/team-compat.py --repo /path/to/team-repo observe
```

State is written to:

```text
$HARNESS_STATE_HOME/repositories/<repository-fingerprint>/
```

or by default:

```text
~/.local/state/ai-dev-harness/repositories/<repository-fingerprint>/
```

No Harness-only file is added to the target repository.

## Rule strength

- `enforced`: host/repository policy;
- `explicit`: CONTRIBUTING, PR templates, CODEOWNERS, repository AI instructions;
- `strong-inferred`: repeated recent behavior with enough observations;
- `tentative`: a possible pattern with insufficient support.

Only explicit/enforced requirements should become blocking collaboration rules.
Inferred conventions guide representation and may warn, but they cannot reduce tests, risk floors, Claims/Evidence requirements, security requirements, or Human Checks.

## Baseline observer

The local observer reads bounded metadata from:

- CONTRIBUTING files;
- pull-request templates;
- CODEOWNERS;
- AGENTS.md / CLAUDE.md / repository AI instructions;
- recent commit subjects;
- local and remote branch names.

The Team Profile stores hashes, statistics, and structured rules rather than copying whole source documents.

Repository-host rulesets, protected-branch configuration, and PR discussion patterns are recorded as unknown until a host-specific provider supplies them.

## Surface guard

Before publication:

```sh
python3 scripts/ai/team-compat.py --repo /path/to/team-repo guard \
  --surface commit --file /tmp/commit-message.txt

python3 scripts/ai/team-compat.py --repo /path/to/team-repo guard \
  --surface pull_request --file /tmp/pr-body.md
```

The guard blocks Harness-internal names/state paths and explicit team-rule violations.
It warns on strongly inferred style differences.

If the team explicitly requires AI-use disclosure, sign-off, authorship, or other metadata, the guard preserves that requirement rather than hiding it.
