"""Synthetic record tests; their fixtures are not release evidence."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "ai"))

from lib.assurance_core import (
    RISK_GATES, evaluate_readiness, repository_revision,
    sha256_file, validate_assurance,
)


class ReviewRecordTests(unittest.TestCase):
    def setUp(self):
        artifacts = ROOT / ".ai-artifacts"
        artifacts.mkdir(exist_ok=True)
        directory = tempfile.TemporaryDirectory(
            prefix="review-record-test-", dir=artifacts
        )
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)

        self.log = self.directory / "fixture.log"
        self.log.write_text("Synthetic observation, not product proof.\n")
        self.reference = {
            "path": self.log.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(self.log),
        }
        self.artifact = self.directory / "review.json"
        artifact_name = self.artifact.relative_to(ROOT).as_posix()

        fixture = ROOT / "ai/evals/assurance/valid/manifest.json"
        manifest = json.loads(fixture.read_text())
        manifest.pop("$schema", None)
        self.claim_id = manifest["claims"][0]["id"]
        manifest["claims"][0]["evidence_requirements"].append({
            "id": "EVR-REVIEW-RECORD-TEST",
            "kind": "ai-review-record",
            "description": "Synthetic review integrity fixture",
            "required": True,
            "artifact": artifact_name,
        })
        self.manifest_path = self.directory / "manifest.json"
        self.manifest_path.write_text(json.dumps(manifest))
        (self.directory / "human-checks.json").write_text(json.dumps({
            "schema_version": "1.0",
            "change_id": manifest["change"]["id"],
            "checks": [],
        }))
        self.validation = validate_assurance(self.manifest_path)
        self.assertTrue(self.validation["valid"], self.validation["errors"])

        gates = []
        for name in sorted(RISK_GATES["yellow"]):
            gate = {
                "gate": name, "result": "N/A", "command": None,
                "exit_code": None, "detail": "Outside this synthetic fixture",
                "log": None,
            }
            if name == "unit":
                gate.update(
                    result="PASS", command="synthetic-fixture",
                    exit_code=0, detail=None, log=self.reference,
                )
            gates.append(gate)

        self.evidence = {
            "schema_version": "1.0",
            "run": {
                "id": "synthetic-review-record-test",
                "risk": "yellow",
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
            "revision": repository_revision(ROOT),
            "environment": {
                "os": "fixture", "architecture": "fixture",
                "python": "fixture", "shell": "fixture",
            },
            "gates": gates,
        }
        self.evidence_path = self.directory / "evidence.json"
        self.evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")
        self.review = {
            "schema_version": "1.0",
            "change_id": manifest["change"]["id"],
            "claim_ids": [self.claim_id],
            "revision": copy.deepcopy(self.evidence["revision"]),
            "verification": {
                "run_id": self.evidence["run"]["id"],
                "evidence": {
                    "path": self.evidence_path.relative_to(ROOT).as_posix(),
                    "sha256": sha256_file(self.evidence_path),
                },
            },
            "reviewer": {
                "id": "synthetic-reviewer", "kind": "ai", "context": "shared",
            },
            "verdict": "PASS",
            "checks": [{
                "claim_id": self.claim_id,
                "kind": "counterexample",
                "basis": "The fixture defines its expected record contract.",
                "scenario": "A report is present but contains an unresolved issue.",
                "expected": "Such a report must not establish readiness.",
                "observed": "Synthetic input for testing record validation.",
                "evidence": [self.reference],
            }],
            "findings": [],
            "limitations": ["Synthetic fixture; not actual reviewer evidence."],
        }

    def store(self):
        self.evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")
        self.artifact.write_text(json.dumps(self.review), encoding="utf-8")

    def bind_review_to_evidence(self):
        self.evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")
        self.review["revision"] = copy.deepcopy(self.evidence["revision"])
        self.review["verification"] = {
            "run_id": self.evidence["run"]["id"],
            "evidence": {
                "path": self.evidence_path.relative_to(ROOT).as_posix(),
                "sha256": sha256_file(self.evidence_path),
            },
        }

    def result(self):
        self.store()
        return evaluate_readiness(self.validation, self.evidence)

    def test_valid_record_and_machine_evidence_can_be_ready(self):
        result = self.result()
        self.assertEqual("READY", result["readiness"])
        self.assertEqual("AI_REVIEWED", result["claims"][0]["ai_review"])

    def test_failed_or_pending_review_blocks(self):
        for verdict in ("BLOCKED", "PENDING"):
            with self.subTest(verdict=verdict):
                self.review["verdict"] = verdict
                self.assertEqual("BLOCKED", self.result()["readiness"])

    def test_missing_review_blocks(self):
        result = evaluate_readiness(self.validation, self.evidence)
        self.assertEqual("BLOCKED", result["readiness"])

    def test_stale_review_blocks(self):
        self.review["revision"]["working_tree_fingerprint"] = "0" * 64
        self.assertEqual("BLOCKED", self.result()["readiness"])

    def test_wrong_change_or_claim_blocks(self):
        original = copy.deepcopy(self.review)
        for field, value in (
            ("change_id", "CHG-UNRELATED"),
            ("claim_ids", ["CLM-UNRELATED"]),
        ):
            with self.subTest(field=field):
                self.review = copy.deepcopy(original)
                self.review[field] = value
                self.assertEqual("BLOCKED", self.result()["readiness"])

    def finding(self, origin="human"):
        return {
            "id": "F-001", "claim_ids": [self.claim_id],
            "origin": origin, "target": "unknown",
            "severity": "blocking",
            "statement": "Expected and observed behavior disagree.",
            "status": "open", "resolution": "", "evidence": [],
        }

    def test_ai_and_human_findings_are_both_blocking(self):
        for origin in ("ai", "human"):
            with self.subTest(origin=origin):
                self.review["findings"] = [self.finding(origin)]
                result = self.result()
                self.assertEqual("BLOCKED", result["readiness"])
                self.assertIn(
                    "UNRESOLVED_REVIEW_FINDING",
                    {item["code"] for item in result["blockers"]},
                )

    def test_blocking_finding_for_another_covered_claim_cannot_be_scoped_away(self):
        second_claim = copy.deepcopy(self.validation["data"]["claims"][0])
        second_claim.update(
            id="CLM-SECOND",
            criticality="should",
            evidence_requirements=[],
        )
        self.validation["data"]["claims"].append(second_claim)
        self.review["claim_ids"].append("CLM-SECOND")
        self.review["checks"].append({
            "claim_id": "CLM-SECOND",
            "kind": "boundary",
            "basis": "The second Claim has a distinct boundary.",
            "scenario": "The record reports a blocker outside its attachment Claim.",
            "expected": "The required record blocks readiness as a whole.",
            "observed": "Synthetic input for cross-Claim finding scope.",
            "evidence": [self.reference],
        })
        finding = self.finding()
        finding["claim_ids"] = ["CLM-SECOND"]
        self.review["findings"] = [finding]
        result = self.result()
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn(
            "UNRESOLVED_REVIEW_FINDING",
            {item["code"] for item in result["claims"][0]["blockers"]},
        )

    def test_retracting_wrong_finding_requires_evidence(self):
        finding = self.finding()
        finding.update(
            status="rejected",
            resolution="The discriminating observation refutes the concern.",
        )
        self.review["findings"] = [finding]
        self.assertEqual("BLOCKED", self.result()["readiness"])
        finding["evidence"] = [self.reference]
        self.assertEqual("READY", self.result()["readiness"])

    def test_evidence_tampering_invalidates_review(self):
        self.log.write_text("Changed observation.\n")
        result = self.result()
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn(
            "REVIEW_RECORD_INVALID",
            {item["code"] for item in result["blockers"]},
        )

    def test_review_cannot_replace_decisive_evidence(self):
        claim = self.validation["data"]["claims"][0]
        claim["evidence_requirements"] = [
            item for item in claim["evidence_requirements"]
            if item["kind"] == "ai-review-record"
        ]
        result = self.result()
        self.assertEqual("AI_REVIEWED", result["claims"][0]["ai_review"])
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn(
            "NO_DECISIVE_EVIDENCE",
            {item["code"] for item in result["blockers"]},
        )

    def test_review_cannot_override_failed_machine_gate(self):
        for gate in self.evidence["gates"]:
            if gate["gate"] == "unit":
                gate.update(result="FAIL", exit_code=1)
        self.bind_review_to_evidence()
        result = self.result()
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertEqual("UNVERIFIED", result["claims"][0]["machine"])
        self.assertIn(
            "REQUIRED_GATE_NOT_PASSING",
            {item["code"] for item in result["claims"][0]["blockers"]},
        )

    def test_required_review_is_required_for_should_claim(self):
        self.validation["data"]["claims"][0]["criticality"] = "should"
        self.review["verdict"] = "BLOCKED"
        self.assertEqual("BLOCKED", self.result()["readiness"])

    def test_failed_review_does_not_promote_other_should_gaps(self):
        claim = self.validation["data"]["claims"][0]
        claim["criticality"] = "should"
        claim["evidence_requirements"].append({
            "id": "EVR-SHOULD-MISSING-GATE",
            "kind": "gate",
            "description": "Synthetic missing gate",
            "required": True,
            "gate": "e2e",
            "locator": "synthetic",
        })
        self.review["verdict"] = "BLOCKED"
        result = self.result()
        blocker_codes = {item["code"] for item in result["claims"][0]["blockers"]}
        warning_codes = {item["code"] for item in result["warnings"]}
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn("REVIEW_NOT_PASSING", blocker_codes)
        self.assertNotIn("REQUIRED_GATE_NOT_PASSING", blocker_codes)
        self.assertIn("REQUIRED_GATE_NOT_PASSING", warning_codes)

    def test_duplicate_json_keys_are_rejected(self):
        self.artifact.write_text(
            json.dumps(self.review)[:-1] + ', "verdict": "PASS"}'
        )
        result = evaluate_readiness(self.validation, self.evidence)
        self.assertEqual("BLOCKED", result["readiness"])

    def test_human_record_is_not_reported_as_ai_reviewed(self):
        self.review["reviewer"]["kind"] = "human"
        result = self.result()
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertEqual("UNVERIFIED", result["claims"][0]["ai_review"])

    def test_review_is_bound_to_verification_run(self):
        self.evidence["run"]["id"] = "another-run-on-the-same-revision"
        result = self.result()
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn(
            "REVIEW_RECORD_INVALID",
            {item["code"] for item in result["blockers"]},
        )

    def test_unknown_claim_and_example_only_review_are_rejected(self):
        original = copy.deepcopy(self.review)
        cases = (
            ("unknown-claim", lambda: self.review["claim_ids"].append("CLM-UNKNOWN")),
            ("example-only", lambda: self.review["checks"][0].update(kind="example")),
        )
        for name, mutate in cases:
            with self.subTest(name=name):
                self.review = copy.deepcopy(original)
                mutate()
                self.assertEqual("BLOCKED", self.result()["readiness"])

    def test_duplicate_evidence_references_are_rejected(self):
        self.review["checks"][0]["evidence"] = [self.reference, self.reference]
        self.assertEqual("BLOCKED", self.result()["readiness"])

    def test_release_cli_rejects_blocked_review(self):
        self.review["verdict"] = "BLOCKED"
        self.store()
        self.evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")
        process = subprocess.run(
            [
                sys.executable, str(ROOT / "scripts/ai/validate-assurance"),
                "--manifest", str(self.manifest_path),
                "--evidence", str(self.evidence_path),
                "--release", "--format", "json",
            ],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertNotEqual(0, process.returncode)
        self.assertEqual("BLOCKED", json.loads(process.stdout)["readiness"])

    def test_release_cli_accepts_passing_review(self):
        self.store()
        process = subprocess.run(
            [
                sys.executable, str(ROOT / "scripts/ai/validate-assurance"),
                "--manifest", str(self.manifest_path),
                "--evidence", str(self.evidence_path),
                "--release", "--format", "json",
            ],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(0, process.returncode, process.stderr)
        self.assertEqual("READY", json.loads(process.stdout)["readiness"])

    def test_release_cli_accepts_review_with_required_agent_trace(self):
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["agent_trace_expectation"] = {
            "required": True,
            "event_types": ["shell.execute"],
            "reason": "Synthetic combined release fixture",
        }
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        trace_path = self.directory / "trace-summary.json"
        trace_path.write_text(json.dumps({
            "coverage": "declared-events-only",
            "action_counts": {"shell.execute": 1},
            "errors": [],
        }), encoding="utf-8")
        self.store()
        process = subprocess.run(
            [
                sys.executable, str(ROOT / "scripts/ai/validate-assurance"),
                "--manifest", str(self.manifest_path),
                "--evidence", str(self.evidence_path),
                "--agent-trace-summary", str(trace_path),
                "--release", "--format", "json",
            ],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(0, process.returncode, process.stderr)
        self.assertEqual("READY", json.loads(process.stdout)["readiness"])


if __name__ == "__main__":
    unittest.main()
