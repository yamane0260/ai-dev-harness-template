# Reliability

## Service expectations

- Availability expectation:
- Performance expectation:
- Data durability expectation:

## Observability

- Logs:
- Metrics:
- Traces:
- Error reporting:

## Failure handling

- Retry policy:
- Idempotency requirements:
- Timeout policy:
- External dependency failure behavior:

## Deployment and rollback

- Staging:
- Production:
- Rollback mechanism:
- Database rollback/forward-fix strategy:

## Reliability invariants

- A release is not complete until post-deploy checks pass.
- A risky data migration requires a tested rollback or a documented forward-recovery plan.
- Bugs should gain a regression test or other durable detection mechanism when practical.
