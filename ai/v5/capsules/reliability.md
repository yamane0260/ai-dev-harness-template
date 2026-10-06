# Reliability Capsule

Load for external services, async work, retries, production operations, or failure-prone boundaries.

Check:

- timeout and cancellation behavior is bounded;
- retries do not multiply side effects;
- partial failure has a defined state and recovery path;
- external unavailability degrades predictably;
- critical operations leave enough structured evidence to diagnose failure;
- resource, rate, quota, and backpressure behavior is reasonable for representative load;
- rollback/restart behavior does not rely on hidden in-memory state.

Prefer explicit failure behavior over indefinite waiting or silent fallback that changes semantics.
