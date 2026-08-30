# Risk Policy

Risk controls how much evidence and human judgment a change requires. The goal is not to maximize approvals; it is to prevent high-consequence mistakes while allowing low-risk work to move autonomously.

## General rules

1. `./scripts/ai/classify-risk` provides a deterministic **risk floor** from the diff.
2. An agent may raise the risk level based on context, uncertainty, or consequences.
3. An agent must not lower the deterministic floor without an explicit human decision recorded in the PR.
4. Unknowns increase risk. A blocking unknown prevents release.
5. Risk is about consequences, not code size.

## GREEN

Typical examples:

- documentation and comments;
- formatting;
- tests that do not change product behavior;
- internal refactors with unchanged observable behavior;
- low-impact developer tooling.

Expected handling:

- required GREEN gates pass;
- no human approval solely for process compliance;
- agent may merge/release only if repository policy permits it.

## YELLOW

Typical examples:

- user-visible behavior changes;
- API contract changes;
- additive database/schema changes;
- new dependencies;
- data transformation logic;
- significant UI/layout changes;
- external integration changes that are reversible.

Expected handling:

- required YELLOW gates pass;
- independent review is preferred;
- human approval only when business behavior, UX consequences, or other non-automatable judgment remains.

## RED

Typical examples:

- authentication or authorization boundaries;
- security policy or security-control changes;
- destructive/irreversible database changes;
- personal/sensitive data exposure or retention changes;
- payments/billing;
- production infrastructure or deployment-policy changes;
- bulk outbound email/messages or other high-impact external side effects;
- deletion or irreversible mutation of production data;
- changes to this harness's risk/verification enforcement itself.

Expected handling:

- required RED gates pass;
- independent code/security review as applicable;
- rollback/recovery evidence;
- No-Guess Approval Packet before irreversible action/release;
- explicit human go/no-go for the consequence, not for technical implementation details.

## Expertise Gate

Do not ask a non-expert reviewer to certify a technical claim they cannot reasonably evaluate.

If the remaining decision genuinely requires specialist expertise:

1. identify the missing expertise;
2. seek independent evidence or expert review where available;
3. otherwise choose a safer, standard, reversible design or postpone the risky action;
4. do not convert uncertainty into a superficial human approval.

## No-Guess Approval

A human approval request must state:

- exact decision requested;
- why AI/machine checks cannot decide it;
- minimum background knowledge;
- user/business consequences;
- verification evidence;
- assumptions and unknowns;
- worst case;
- rollback/recovery;
- alternatives;
- recommendation;
- strongest argument against that recommendation.
