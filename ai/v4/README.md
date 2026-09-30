# V4 Runtime and Contract Index

V4 is the active harness architecture.

It combines a small constitutional kernel, semantic capabilities, swappable providers, profiles, bounded runtime records, and a project-local self-describing Dashboard.

## Active runtime sources

- `capabilities.md`: semantic capability contracts.
- `profiles/*.json`: optimization presets and non-negotiable constraints.
- `provider-registry.json`: capability-to-provider implementations.
- `self-description.json`: human-facing architecture and explanation metadata used by the Dashboard without LLM calls.
- `../schemas/capability.schema.json`: capability descriptor contract.
- `../schemas/plugin-manifest.schema.json`: provider metadata and execution boundary.
- `../schemas/profile.schema.json`: profile contract.
- `../schemas/execution-plan.schema.json`: compiled execution plan.
- `../schemas/run-event.schema.json`: append-only bounded run event.
- `../schemas/project-dashboard.schema.json`: project-local Dashboard configuration.
- `../../scripts/ai/v4.py`: runtime CLI and Dashboard entrypoint.

## Runtime flow

```text
request
  -> deterministic risk + explicit routing inputs
  -> profile compiler
  -> capability selection
  -> provider resolution
  -> inspectable execution plan
  -> selected providers execute
  -> bounded run events + evidence + Human Checks
  -> Dashboard read model
```

The Dashboard is not an orchestration dependency.
If Dashboard telemetry fails, normal implementation should continue unless the underlying failed operation is itself a required assurance or verification capability.

## Self-describing Dashboard

Run:

```sh
python3 scripts/ai/v4.py init
python3 scripts/ai/v4.py dashboard
```

The Dashboard has three stable views.

- **作業**: current project work, verification, recent changes, and Human Checks.
- **仕組み**: Harness architecture, selected capabilities/providers, and machine-readable selection reasons.
- **診断**: timeline, retries, fallbacks, context compaction, anomalies, and raw technical records.

Explanations come from static self-description metadata and structured events.
Normal Dashboard rendering does not invoke an LLM or consume the implementation agent's context.

## Compatibility boundary

Dashboard UI reads the V4 read model rather than internal files directly.
Future V4-derived architectures can replace the adapter/compiler while preserving the human-facing model where the semantics remain compatible.

Legacy V3 assets remain only where they act as V4 providers or durable project sources.
