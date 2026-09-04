# Adaptive Explanation Policy

Store compact facts and relationships; generate prose for the current reader on demand.

## Local familiarity profile

An optional `.harness-user.json` describes familiarity by domain on a 0–4 scale:

- `0`: unfamiliar; introduce prerequisites and terms.
- `1`: basic recognition; explain the mechanism and project use.
- `2`: working knowledge; focus on project-specific flow and failure modes.
- `3`: proficient; focus on constraints, deltas, and evidence.
- `4`: expert; provide terse references, exceptions, and unresolved uncertainty.

The file is local and ignored by Git. Use `.harness-user.example.json` as a starting point.

## Invariants

- Familiarity changes explanation depth only.
- It never changes tests, security controls, Claim criticality, Human Check level, release gates, or the amount of evidence required.
- Project/domain familiarity is separate from language/framework familiarity.
- If no profile exists, infer only from the current request and explicitly supplied context; do not create a durable personal profile without the user's instruction.

## Progressive drill-down

Explain from the requested zoom level and expand only as needed:

1. system purpose;
2. component responsibility;
3. change/Claim and affected paths;
4. relevant project-specific concept or decision;
5. function/symbol behavior;
6. selected line or expression;
7. failure mode and verifying evidence.

For material "why" statements, preserve `RECORDED`, `DERIVED`, and `INFERRED`. Do not invent historical rationale from code shape.
