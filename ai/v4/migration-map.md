# V3 to V4 File Migration Map

This map assigns current V3 files and responsibilities to their V4 destination.
It is intentionally file-oriented so that later migration work can be reviewed as a sequence of bounded moves instead of a broad rewrite.

The current V3 runtime remains authoritative until the relevant migration phase is completed and verified.

## Status vocabulary

- **KEEP**: retain the file or responsibility with only documentation updates.
- **SPLIT**: divide one V3 responsibility across V4 kernel, capability, provider, or substrate boundaries.
- **WRAP**: keep current implementation initially and expose it through a V4 provider contract.
- **MOVE**: relocate source-of-truth responsibility to a V4 location.
- **THIN**: retain only a host-facing adapter or bootstrap entry point.
- **DEPRECATE**: keep temporarily for compatibility, then remove after V4 equivalence is demonstrated.
- **REMOVE**: delete after the target V4 replacement is active and migration evidence passes.

## Root files

| V3 path | V4 action | Target responsibility | Migration notes |
|---|---|---|---|
| `AGENTS.md` | SPLIT, then THIN | constitutional kernel bootstrap + profile runtime entry | Extract non-negotiable invariants into kernel policy. Remove fixed workflow detail after the V4 runtime is authoritative. Keep only portable agent bootstrap and source-of-truth pointers. |
| `README.md` | KEEP | human overview | Rewrite from V3 workflow description to V4 composition model after runtime cutover. During migration, document both status and authoritative path. |
| `PROJECT_MAP.md` | KEEP | project-state navigation | Preserve as the human entry point. Add V4 composition, run, and context-artifact locations after they exist. |
| `CLAUDE.md` | KEEP, THIN | Claude Code host adapter shim | Continue delegating repository policy to shared sources rather than duplicating policy. |
| `.harness-user.example.json` | MOVE/EXPAND | local explanation preference input | Keep local familiarity preferences separate from quality/release constraints. Later map into profile/user preference input rather than policy. |

## `.agents/skills/`

V3 Skills remain useful provider implementations, but they should stop owning global routing policy.
The first V4 migration wraps them before rewriting them.

| V3 path | V4 action | Capability/provider target | Migration notes |
|---|---|---|---|
| `.agents/skills/README.md` | KEEP, rewrite later | host-facing provider catalog | Replace workflow taxonomy with mapping from Skills to capability providers after wrapping is complete. |
| `.agents/skills/bootstrap-project/` | WRAP | `project.bootstrap` provider | Preserve behavior initially. Project bootstrap may later emit the V4 project profile and host capability baseline. |
| `.agents/skills/develop-feature/` | DEPRECATE, then THIN | `profile.resolve` + workflow runtime adapter | This is the main V3 orchestration concentration. First make it call a shadow compiler, then an execution plan, then reduce it to a thin adapter. |
| `.agents/skills/spec-gap-preflight/` | WRAP | `quality.preflight` provider | Keep domain reasoning but load only when Quality Impact or ambiguity triggers it. |
| `.agents/skills/verify-work/` | WRAP | `review.verification` provider | Its fresh-context, summary-first behavior already fits V4 well. |
| `.agents/skills/review-code/` | WRAP | `review.code` provider | Convert free-form output to the structured review contract. |
| `.agents/skills/review-security/` | WRAP | `review.security` provider | Add explicit context, host, permission, and failure metadata. |
| `.agents/skills/review-ux/` | WRAP | `review.ux` provider | Preserve explicit Human Checks for real-device or subjective observations. |
| `.agents/skills/review-design/` | WRAP | `review.design` provider | Keep design review advisory unless profile/Claim policy makes it required. |
| `.agents/skills/review-assurance/` | WRAP | `assurance.review` candidate provider | Keep distinct from `assurance.evaluate`, which remains deterministic readiness logic. |
| `.agents/skills/explain-change/` | WRAP | `knowledge.explain-change` provider | Preserve rationale provenance and evidence-derived explanation. |
| `.agents/skills/explain-system/` | WRAP | `knowledge.explain-system` provider | Drive context through project index and bounded source selection. |
| `.agents/skills/review-legibility/` | WRAP | `knowledge.legibility` provider | Preserve fresh-context AI Absence Test. |
| `.agents/skills/prepare-approval/` | WRAP | `human.approval.prepare` provider | Keep human approval separate from technical verification. |
| `.agents/skills/release-change/` | SPLIT | `release.evaluate` provider + host release adapter | Move readiness calculation into structured runtime state. Keep actual external release actions behind explicit permissions. |
| `.agents/skills/debug-systematically/` | WRAP | `debug.diagnose` provider | Preserve discriminating-observation approach. |

## `ai/` routing and configuration

| V3 path | V4 action | Target responsibility | Migration notes |
|---|---|---|---|
| `ai/README.md` | KEEP, update | harness contract index | Point to `ai/v4/` during migration. Later describe the stable contract layout. |
| `ai/TEMPLATE_MODE` | DEPRECATE, REMOVE | explicit project profile/bootstrap state | Replace marker-file semantics with a structured project profile field once compiler/runtime exists. |
| `ai/commands.conf` | WRAP, later MOVE | local `verification.run` provider configuration | Keep project commands as provider config. Do not move command knowledge into model prompts. |
| `ai/harness-commands.conf` | WRAP, later MOVE | harness self-test provider configuration | Preserve distinction between template mechanics and adopted-product evidence. |
| `ai/context-map.md` | WRAP, then DEPRECATE | `context.select` provider policy/data | Use as source material for the first selector. Replace instruction-based routing with structured reference selection and provenance. |
| `ai/quality-envelope.md` | SPLIT | Quality Impact taxonomy + `quality.preflight` providers | Keep domain taxonomy. Move domain-specific instructions behind progressive disclosure and capability routing. |

## `ai/policies/`

| V3 path | V4 action | Target responsibility | Migration notes |
|---|---|---|---|
| `ai/policies/risk-policy.md` | SPLIT | kernel risk invariants + `risk.floor` contract/provider | Deterministic floor remains non-negotiable. Consequence examples become classifier/provider guidance. |
| `ai/policies/quality-gates.md` | DEPRECATE in current form | risk baseline + Quality Impact + Claim requirements | V4 should compute the required gate union instead of selecting one large fixed bundle solely from risk. Preserve a minimum baseline. |
| `ai/policies/assurance.md` | SPLIT | kernel trust semantics + `assurance.evaluate` contract | Claim/Evidence/Human Check distinctions remain central. Deterministic readiness logic stays executable. |
| `ai/policies/mutual-verification.md` | SPLIT | kernel fallibility principle + review-provider guidance | Keep mutual correction as a kernel principle. Move concrete review procedures into providers. |
| `ai/policies/human-legibility.md` | SPLIT | Knowledge Impact policy + `knowledge.*` capabilities | Preserve AI Absence Test and rationale provenance. Separate Knowledge Impact from the new Human Understanding Requirement. |
| `ai/policies/adaptive-explanation.md` | MOVE | `knowledge.explain-*` provider guidance + local preferences | Familiarity may alter explanation depth but never constraints. |
| `ai/policies/agent-control.md` | SPLIT | `trace.capture` contract + host adapters | Keep trace coverage explicit and non-decisive. Host-specific mechanics move to adapters. |

## `ai/schemas/`

Existing evidence schemas remain valuable stable contracts.
They should be versioned rather than replaced without migration.

| V3 path | V4 action | Target responsibility |
|---|---|---|
| `ai/schemas/assurance-manifest.schema.json` | KEEP, version | Claim and evidence requirement contract |
| `ai/schemas/evidence-record.schema.json` | KEEP, version | exact-run evidence contract |
| `ai/schemas/human-checks.schema.json` | KEEP, version | human observation/judgment contract |
| `ai/schemas/review-record.schema.json` | KEEP, version | structured review output contract |
| `ai/schemas/agent-event.schema.json` | KEEP, evolve | run/trace event input; later align with the V4 run-event contract |
| `ai/schemas/project-index.schema.json` | KEEP, evolve | derived project index contract |
| `ai/schemas/capability.schema.json` | NEW | semantic capability contract descriptor |
| `ai/schemas/plugin-manifest.schema.json` | NEW | provider composition, permissions, context, lifecycle, cost, failure contract |
| `ai/schemas/profile.schema.json` | NEW | objectives and non-negotiable constraints |
| `ai/schemas/execution-plan.schema.json` | NEW | compiled inspectable composition |
| `ai/schemas/run-event.schema.json` | PLANNED | V4 append-only run ledger event |
| `ai/schemas/host-capability.schema.json` | PLANNED | host feature/enforcement coverage |
| `ai/schemas/context-metrics.schema.json` | PLANNED | context and cost accounting |

## `ai/templates/`

| V3 path | V4 action | Target responsibility | Migration notes |
|---|---|---|---|
| `ai/templates/assurance/manifest.json` | KEEP | assurance contract template | Update only when the assurance schema version changes. |
| `ai/templates/assurance/human-checks.json` | KEEP | Human Check contract template | No V4-specific prose should be required. |
| `ai/templates/task-packet.md` | SPLIT | structured exploration result + Markdown projection | Add a machine-readable Task Packet contract before retiring Markdown as the only form. |
| `ai/templates/quality-impact.md` | MOVE | compiler impact input/projection | Convert from manually carried template state to structured compiler input while retaining a human-readable projection. |
| `ai/templates/ux-contract.md` | MOVE | `review.ux` provider/project-state template | Load only for UX-relevant tasks. |
| `ai/templates/change-record.md` | MOVE | `knowledge.explain-change` output template | Preserve compact low-impact record form. |
| `ai/templates/change-brief.md` | MOVE | `knowledge.explain-change` output template | Keep evidence-derived, rationale-labeled behavior. |
| `ai/templates/runbook.md` | KEEP | project durable operational knowledge | This is project state, not a runtime plugin itself. |
| `ai/templates/approval-packet.md` | MOVE | `human.approval.prepare` output template | Continue validating No-Guess Approval structure. |
| `ai/templates/review-record.json` | MOVE | review capability output template | Align to provider-independent review contract. |

## `ai/evals/`

| V3 path | V4 action | Target responsibility |
|---|---|---|
| `ai/evals/quality-envelope/` | KEEP, evolve | Quality Impact and preflight routing regression |
| `ai/evals/human-legibility/` | KEEP, evolve | Knowledge Impact and AI Absence Test regression |
| `ai/evals/no-guess-approval/` | KEEP | approval capability regression |
| `ai/evals/assurance/` | KEEP | kernel/assurance contract regression |
| new `ai/evals/composition/` | ADD | dependency, conflict, fallback, required-capability regression |
| new `ai/evals/context-efficiency/` | ADD | unnecessary context and plugin loading regression |
| new `ai/evals/profiles/` | ADD | Rapid/Balanced/Understanding/High-Assurance selection behavior |
| new `ai/evals/hosts/` | ADD | host coverage and non-silent downgrade behavior |

## `scripts/ai/`

| V3 path | V4 action | Capability/substrate target | Migration notes |
|---|---|---|---|
| `scripts/ai/self-test` | KEEP, expand | kernel/runtime self-test | Add schema and composition contract validation before runtime cutover. |
| `scripts/ai/classify-risk` | WRAP | `risk.floor` deterministic provider | Keep implementation stable initially and publish structured output. |
| `scripts/ai/verify` | SPLIT gradually | `verification.run` + runner + evidence substrate | First wrap current behavior. Later separate gate resolution, command execution, evidence recording, and assurance evaluation. |
| `scripts/ai/validate-assurance` | WRAP | `assurance.evaluate` deterministic provider | Preserve current decisive semantics. |
| `scripts/ai/record-evidence` | KEEP | evidence store substrate | Add composition identity after the V4 compiler exists. |
| `scripts/ai/build-project-index` | WRAP | `project.index` provider | Keep derived index non-authoritative. |
| `scripts/ai/record-agent-event` | WRAP | `trace.capture` host adapter/provider | Later emit common V4 run-event shape where possible. |
| `scripts/ai/validate-agent-trace` | WRAP | trace validation provider | Preserve explicit coverage summary. |
| `scripts/ai/validate-approval` | WRAP | `human.approval.prepare` validation | Keep deterministic structure validation. |
| `scripts/ai/lib/` | SPLIT gradually | capability/provider libraries | Move only after dependencies are clear and tests protect behavior. |
| `scripts/ai/tests/` | KEEP, expand | deterministic contract tests | Add schema, profile compiler, resolver, and composition invariant tests. |

## `docs/`

These files are project state, not plugins.
They stay authoritative while `context.select` controls when the model loads them.

| V3 path | V4 action | Target responsibility |
|---|---|---|
| `docs/PRODUCT.md` | KEEP | current product requirements |
| `docs/ARCHITECTURE.md` | KEEP | current system boundaries |
| `docs/DESIGN.md` | KEEP | current design decisions/guidance |
| `docs/SECURITY.md` | KEEP | project security authority |
| `docs/UX.md` | KEEP | project UX authority |
| `docs/RELIABILITY.md` | KEEP | reliability/recovery authority |
| `docs/specs/` | KEEP | current detailed requirements |
| `docs/decisions/` | KEEP | durable decision provenance |
| `docs/concepts/` | KEEP | canonical project concepts |
| `docs/runbooks/` | KEEP | operational procedures |
| `docs/changes/` | KEEP | historical human-facing change knowledge |

The selector should reference these sources rather than copying them into global instructions.

## `assurance/`

| V3 path | V4 action | Target responsibility |
|---|---|---|
| `assurance/README.md` | KEEP, update later | human-facing assurance model |
| `assurance/current/` | KEEP | active Claim/Evidence/Human Check project state |
| `assurance/changes/` | KEEP | historical assurance state |

Provider implementations can change without changing these project-level records.

## `.ai-artifacts/`

The directory remains generated and uncommitted.
V4 extends it rather than replacing it.

| Current/planned path | V4 role |
|---|---|
| `.ai-artifacts/verification/` | exact-run evidence and logs |
| `.ai-artifacts/reviews/` | structured review artifacts |
| `.ai-artifacts/traces/` | sanitized host action traces |
| `.ai-artifacts/index/` | derived project relationships |
| `.ai-artifacts/runs/` | PLANNED append-only V4 run ledger |
| `.ai-artifacts/compositions/` | PLANNED execution plans and composition identity |
| `.ai-artifacts/context/` | PLANNED context-selection and compaction metadata |
| `.ai-artifacts/metrics/` | PLANNED context, cost, latency, and human-attention metrics |

Raw artifacts remain separate from normal model context and durable documentation.

## `.github/`

| V3 path | V4 action | Target responsibility |
|---|---|---|
| `.github/workflows/verify.yml` | KEEP, later THIN | CI host adapter | CI should invoke the same V4 runtime/plan rather than recreate routing logic in YAML. |
| `.github/pull_request_template.md` | KEEP, evolve | human projection | Later surface effective profile, Claims, pending Human Checks, and release state without duplicating policy. |

## Proposed migration sequence by file impact

### Phase A: contract-only, no runtime behavior change

Add:

- `docs/decisions/2026-09-15-v4-composable-harness-architecture.md`;
- `ai/v4/README.md`;
- `ai/v4/capabilities.md`;
- `ai/v4/profiles/*.json`;
- this migration map;
- V4 capability, plugin, profile, and execution-plan schemas.

Update only indexes/README pointers.

### Phase B: schema validation and wrappers

Modify:

- `scripts/ai/self-test` to validate V4 JSON sources;
- existing deterministic scripts to expose stable provider-friendly structured outputs;
- Skill metadata to declare the capability they implement without changing their main instructions.

Do not switch normal development routing yet.

### Phase C: shadow composition

Add:

- profile compiler;
- plugin/provider registry;
- host capability registry;
- execution-plan validator;
- composition evals.

Modify `develop-feature` only enough to generate and report the shadow plan while V3 still executes.

### Phase D: runtime cutover

Turn `develop-feature` into a thin adapter that executes the validated plan.
Add run ledger and context metrics.
Keep legacy V3 routing available behind an explicit compatibility path during evaluation.

### Phase E: context and provider decomposition

Move provider instructions behind progressive disclosure.
Introduce structured child outputs and bounded parent-context budgets.
Split `scripts/ai/verify` only after its current behavior is covered by contract tests.

### Phase F: removal

Remove:

- `ai/TEMPLATE_MODE` after structured bootstrap/project state replaces it;
- fixed Work Mode workflow selection after the compiler is authoritative;
- static full-document routing instructions after structured context selection passes evaluation;
- legacy `develop-feature` orchestration after V4 demonstrates equivalent or stronger quality and lower context overhead.

## Migration acceptance criteria

The V4 runtime should not replace V3 merely because the new architecture is cleaner.
Cutover requires evidence on a reference task suite showing that V4:

- preserves kernel and assurance invariants;
- does not silently downgrade required capabilities or provider failures;
- keeps or improves functional and quality outcomes;
- reduces unnecessary parent-context consumption for simple work;
- makes selected and skipped capabilities explainable;
- preserves host portability or reports host limitations explicitly;
- keeps durable project state usable without the original AI session.
