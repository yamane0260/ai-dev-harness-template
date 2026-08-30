---
name: prepare-approval
description: Convert a risky or non-automatable decision into a short human-ready No-Guess Approval Packet. Use before asking a human to approve YELLOW/RED consequences, irreversible actions, policy/product tradeoffs, or visual/business judgment, especially when the reviewer may not know the underlying technical details.
---

# Prepare Approval

Use `ai/templates/approval-packet.md` as the required structure.

Before requesting approval:

1. State exactly one decision in user/business terms.
2. Explain why machine checks and agent review cannot decide it.
3. Explain only the minimum technical background required, in plain language.
4. Translate implementation details into user, data, money, operational, or business consequences.
5. Cite fresh deterministic evidence and independent review results.
6. List assumptions and unknowns explicitly.
7. State a credible worst case and rollback/recovery limits.
8. Present at least one meaningful alternative.
9. Give a recommendation with reasons.
10. State the strongest argument against that recommendation.
11. Run `./scripts/ai/validate-approval <packet>` before presenting it.

If a blocking unknown remains, do not request approval. If the decision requires specialist expertise the reviewer cannot reasonably possess, activate the Expertise Gate: seek expert/independent evidence, choose a safer standard/reversible option, or defer. Never turn missing expertise into "please approve anyway."
