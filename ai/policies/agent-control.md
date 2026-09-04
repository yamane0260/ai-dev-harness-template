# Agent Control and Trace Policy

Generated-product assurance and agent-action assurance are separate layers.

## What to observe

When the host supports it, capture metadata for:

- file read/write;
- shell execution;
- network access;
- MCP/tool calls;
- credential access events (never credential values);
- Git push;
- release/deployment;
- subagent invocation.

Use `ai/schemas/agent-event.schema.json` as the interchange contract. Store events under `.ai-artifacts/traces/` and derive compact summaries/indexes for normal use.

## Boundaries

- A repository cannot prove that a host emitted every event. State instrumentation coverage explicitly.
- Never fabricate an event from an agent's narrative.
- Record metadata and control outcome, not private chain-of-thought, secrets, full file contents, or unredacted command output.
- Trace presence proves provenance/control visibility, not correctness of the generated product.
- High-impact external actions should identify their authorization source and outcome.

## Context handling

Read summaries first. Retrieve individual events only to investigate a specific action or control gap. Do not load a complete trace into the main implementation context by default.
