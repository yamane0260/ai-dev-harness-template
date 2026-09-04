# Harness V3: Human Responsibility Transfer

## Goal

Make a non-trivial AI-developed result complete only when a maintainer can locate its intent, inspect what was and was not verified, see required human work, and drill from system intent to relevant code without the original AI conversation.

## Required outcomes

1. A human starting at the repository root can identify the role and source-of-truth status of `docs/`, `assurance/`, `ai/`, `.agents/skills/`, `scripts/ai/`, and `.ai-artifacts/`.
2. STANDARD/CRITICAL or YELLOW/RED changes can record Requirement → Claim → evidence requirement / Human Check relationships in dependency-free structured files.
3. Verification records command, result, exit code, exact repository fingerprint, environment, and log hash without committing raw output.
4. A required gate that is missing, failing, stale, unconfigured, or N/A cannot satisfy a MUST Claim.
5. `AI_REVIEWED` is visible but cannot be used as the only decisive support for a MUST Claim.
6. A pending or failed MUST Human Check prevents release readiness; SHOULD/OPTIONAL work remains visible without automatically blocking.
7. A derived relationship index can be rebuilt from repository sources and is never itself the source of truth.
8. Explanation depth can adapt by technical domain, but quality, security, Human Check, and release requirements cannot.
9. Agent action events have a sanitized interchange format, distinguish capture source/coverage, and never imply complete observation when the host cannot provide it.
10. Existing template-mode `verify` remains usable before project bootstrap. Template maintainers have a separate `--harness` verification mode that cannot stand in for product verification.

## Negative / invariant criteria

- Do not store chain-of-thought, full transcripts, secrets, credential values, or raw command output in human-facing records.
- Do not commit generated evidence, traces, or the derived graph.
- Do not require a graph database, YAML parser, web application, or third-party Python package for V3 foundations.
- Do not convert all changes into documentation ceremony; genuinely MICRO/GREEN/LOW work may retain an inline record.
- Do not mark a release READY merely because a manifest is structurally valid.
- Do not claim that provenance or agent traceability proves software correctness.

## Migration and compatibility

- With the documented Python 3 prerequisite present, `./scripts/ai/verify --risk <level>` retains its V2 template/product command behavior.
- Assurance is activated for a run with `--assurance <manifest>`.
- `--release` requires assurance for YELLOW/RED work.
- Projects adopt V3 records for new non-trivial changes; historical V2 changes do not need retroactive manifests unless current risk justifies one.

## Deferred scope

A graphical Harness Explorer is intentionally deferred. V3 first establishes validated repository data and a derived read model so a later UI does not become an inconsistent second source of truth.
