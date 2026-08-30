---
name: verify-work
description: Perform an independent verification pass when fresh-context validation is useful, especially for CRITICAL work, suspicious regressions, or pre-release confidence. Do not use merely to rerun routine commands that `scripts/ai/verify` already executes.
---

# Verify Work

Use a fresh context when supported. Receive only the Task Packet, current diff/changed paths, acceptance criteria, and verification summary unless more evidence is needed.

1. Determine the applicable risk level; do not silently lower the deterministic floor.
2. Inspect the existing verification summary first. Re-run focused commands only when evidence is missing, stale, or a finding depends on runtime behavior.
3. Compare implementation/diff to acceptance criteria and look for missing, contradictory, or unrequested behavior.
4. Do not ingest raw logs wholesale. Read targeted failing sections or artifact files as needed.
5. Report only material findings, residual unknowns, and whether current evidence supports completion.
6. A routine MICRO change that already has fresh deterministic evidence does not need this separate pass.
