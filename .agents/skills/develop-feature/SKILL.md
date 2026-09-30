---
name: develop-feature
description: Implement product features and behavior changes through the V4 execution-plan runtime. Use for normal software changes that need bounded context, selected capabilities/providers, deterministic verification, explicit Human Checks, and proportional durable understanding.
---

# Develop Feature

1. Inspect the request and only the minimum repository metadata needed to identify task kind, material Quality Impact, Knowledge Impact, release intent, and any known blocking constraint.
2. Compile a V4 execution plan before broad implementation work:
   ```sh
   python3 scripts/ai/v4.py plan --task implement [routing options]
   ```
   Use `--quality <domain>` only for material domains and `--knowledge-impact` independently. Do not lower the deterministic risk floor.
3. Read the generated plan under `.ai-artifacts/runs/<run-id>/plan.json`. Treat selected capabilities as the active workflow. Do not load or invoke unselected provider instructions merely because they exist.
4. Load bounded project context through `ai/context-map.md` and the selected capability needs. Broad exploration should be isolated when supported; return structured findings instead of raw transcripts.
5. Apply selected planning/review capabilities before implementation when their contract requires preflight work. Preserve blocking unknowns rather than guessing.
6. Implement the smallest change that satisfies the request and compiled constraints. Record only non-reconstructable decisions, invariants, material alternatives, and Claim relationships.
7. Add focused tests or checks for requested behavior and material negative/invariant behavior.
8. Run selected deterministic verification on the stable tracked state. Use existing `scripts/ai/verify`, evidence, and assurance tooling as the V4 providers named by the execution plan.
9. Run only selected independent review capabilities. AI review remains non-decisive unless paired with the required machine evidence.
10. Handle Knowledge Impact proportionally. MATERIAL/CRITICAL changes create durable evidence-grounded knowledge when selected by the plan. Perform the fresh-context legibility check only when selected.
11. Leave explicit Human Checks only for observations or judgments automation cannot establish.
12. Emit bounded V4 events for material stages when the host/wrapper can do so. Never include raw prompts, raw completions, secrets, credentials, or large command output.
13. Rebuild the Dashboard read model after the run when needed:
   ```sh
   python3 scripts/ai/v4.py state --write
   ```

Return a compact completion summary containing outcome, verification/evidence path, remaining Human Checks, residual uncertainty, and durable knowledge path when applicable.

## Runtime boundary

The Dashboard is observational.
Do not spend implementation-agent context generating Dashboard explanations.
Self-description comes from `ai/v4/self-description.json` and structured events.
