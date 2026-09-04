# Assurance Review: Responsibility-transfer V3 foundation

- Review type: `AI_REVIEWED`
- Method: `review-code` + `review-assurance`
- Context: same implementation session
- Independence: not independent of the implementation agent
- Decisive status: this review is required scrutiny, but no MUST Claim relies on it without deterministic gate evidence

## Scope reviewed

- V3 requirements and negative criteria in `docs/specs/harness-v3-responsibility-transfer.md`.
- Claim/Evidence/Human Check mapping in the change manifest.
- Assurance validation/readiness logic and its fixtures/tests.
- Exact-revision evidence recording, log hashing, and release behavior.
- Derived-index relationships and source-of-truth boundary.
- Agent-event redaction/coverage claims.
- Template-mode and `--harness` compatibility boundary.

## Material findings corrected during review

1. The first index implementation failed when a test wrote output outside the repository. Output display now safely handles both repository-relative and external temporary paths.
2. Early evidence evaluation trusted the shape of a supplied PASS too readily. It now validates the complete risk-gate set, command/exit semantics, full Git object ID, timezone-aware timestamp, log existence, and log SHA-256.
3. Release evaluation initially exposed a fixture-only revision bypass. `--skip-revision-check` is now rejected with `--release`.
4. MUST Claims could initially declare only optional/non-decisive support. Structural validation now requires a required gate or a linked MUST Human Check and rejects unmapped requirements.
5. Local `$schema` references in eval fixtures were one directory too high. The paths were corrected and local schema existence is now validated.
6. The active-manifest scan used GNU-oriented `find` depth flags. It now uses Bash `nullglob` for macOS/Linux portability.
7. Agent trace IDs could have influenced the default output path, and query-string secrets were not covered. IDs are now restricted to safe characters/length and common credential-bearing targets are rejected.
8. The graph test previously proved only that a JSON file was produced. It now asserts Requirement → Claim and Claim → Evidence edges.

## Post-correction Claim review

| Claim | Evidence actually relevant to the Claim | Assessment |
|---|---|---|
| `CLM-V3-001` | Integration self-test requires human entry points; `HC-V3-001` separately tests real findability | Mapping is bounded; machine evidence does not claim human usability |
| `CLM-V3-002` | Unit fixtures reject malformed/unmapped structures; this review checks wording and relationship scope | Supported; review remains non-decisive |
| `CLM-V3-003` | Unit tests cover PASS/N/A/stale state; evidence validator checks log content hashes | Supported within local exact-worktree scope |
| `CLM-V3-004` | Unit tests cover AI-review-only and pending MUST Human Check behavior | Supported |
| `CLM-V3-005` | Architecture gate rebuilds index; focused test asserts required edges | Supported; symbol-level graph remains deferred |
| `CLM-V3-006` | Security tests cover common credential payloads; summary explicitly says declared-events-only | Supported without claiming host completeness |
| `CLM-V3-007` | Policy and Skill both prohibit familiarity-based gate reduction | Instruction/eval risk remains explicitly uncertain |
| `CLM-V3-008` | Integration gate runs default template verification from harness mode | Supported when documented Python 3 prerequisite exists |

## Residual uncertainty / human work

- `HC-V3-001` remains a SHOULD check for representative human findability.
- No independent fresh-context semantic reviewer was used; this is disclosed and the review is not counted as machine proof.
- A graphical Harness Explorer is deferred until the data model is exercised in real projects.
- Automatic agent trace completeness depends on host adapters and is not claimed by this repository.

## Result

`PASS` for internal Claim/evidence consistency after the corrections above. This result is `AI_REVIEWED`, not independent certification and not a substitute for the RED deterministic gates.
