# Legibility Review: Responsibility-transfer V3 foundation

- Method: AI Absence Test using repository records as the review input
- Result: `PASS`
- Release impact: no blocking readiness gap found
- Limitation: performed in the implementation session rather than an independent fresh context; this is not independent certification

## AI Absence Test

1. **What changed?** `PROJECT_MAP.md` and folder READMEs provide the human entry path; `assurance/` adds structured proof obligations; verification emits exact-run evidence; the derived index supports relationship retrieval; explanation and agent-control policies define the later human/UI boundary.
2. **Why this approach?** `RECORDED`: the owner required completion to include human-understandable evidence and explicit AI/human limits without consuming the implementation context with exhaustive prose. `RECORDED`: structured Assurance data precedes the Explorer UI. The accepted choice and rejected alternatives are in `docs/decisions/2026-09-04-assurance-as-repository-data.md`.
3. **What must remain true?** AI review is non-decisive; required N/A/stale/failing evidence does not pass; MUST Human Checks block until passed; raw artifacts stay outside Git; familiarity changes explanation only; trace coverage is never invented.
4. **Where is the likely next modification?** Schema/readiness changes start in `scripts/ai/lib/assurance_core.py` plus matching `ai/schemas/`, tests, policy, and concept. Explorer work starts from `scripts/ai/build-project-index` output, not a new UI database.
5. **How is failure detected, diagnosed, and recovered?** `readiness.json` identifies the exact Claim/gate/check; targeted logs are hashed and linked; `docs/runbooks/assurance-readiness.md` gives the bounded recovery path.
6. **Can evidence classes be distinguished?** The manifest and readiness output display machine, AI-review, and human facets separately; `HC-V3-001` remains visibly pending at SHOULD level without blocking release.

The durable records answer all questions without requiring an implementation transcript. The representative human navigation timing remains a declared SHOULD observation rather than an unrecorded assumption.
