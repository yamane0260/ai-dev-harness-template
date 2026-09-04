---
name: verify-work
description: Perform an independent verification pass when fresh-context validation is useful, especially for CRITICAL work, suspicious regressions, or pre-release confidence. Do not use merely to rerun routine commands that `scripts/ai/verify` already executes.
---

# Verify Work

Use a fresh context when supported. Receive only the Task Packet, current diff/changed paths, acceptance criteria, and verification summary unless more evidence is needed.

1. Determine the applicable risk level; do not silently lower the deterministic floor.
2. Inspect the existing verification summary and exact-run `evidence.json` first. Re-run focused commands only when evidence is missing, stale, or a finding depends on runtime behavior.
3. When an assurance manifest exists, check that the evidence supports the stated Claim rather than merely showing a broad gate passed. Confirm that `AI_REVIEWED` has not been treated as machine proof.
4. Compare implementation/diff to acceptance criteria and look for missing, contradictory, or unrequested behavior.
5. Do not ingest raw logs wholesale. Read targeted failing sections or artifact files as needed.
6. Report only material findings, residual uncertainty, Human Checks, and whether current evidence supports completion.
7. A routine MICRO change that already has fresh deterministic evidence does not need this separate pass.
