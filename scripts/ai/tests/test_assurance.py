#!/usr/bin/env python3

from __future__ import annotations

import copy
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "ai"))

from lib.assurance_core import (
    evaluate_readiness,
    repository_revision,
    sha256_file,
    validate_assurance,
)


class AssuranceReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = ROOT / "ai" / "evals" / "assurance" / "valid" / "manifest.json"
        cls.validation = validate_assurance(cls.manifest)
        if not cls.validation["valid"]:
            raise AssertionError(cls.validation["errors"])
        cls.log_path = ROOT / ".ai-artifacts" / "tests" / "assurance-fixture.log"
        cls.log_path.parent.mkdir(parents=True, exist_ok=True)
        cls.log_path.write_text("fixture evidence\n", encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.log_path.unlink(missing_ok=True)

    def evidence(self, result: str = "PASS") -> dict:
        records = []
        for gate in (
            "typecheck",
            "lint",
            "unit",
            "integration",
            "build",
            "security",
            "architecture",
        ):
            if gate == "unit":
                records.append(
                    {
                        "gate": gate,
                        "result": result,
                        "command": "python3 -m unittest",
                        "exit_code": 0 if result == "PASS" else None,
                        "detail": None if result == "PASS" else "fixture N/A",
                        "log": (
                            {
                                "path": ".ai-artifacts/tests/assurance-fixture.log",
                                "sha256": sha256_file(self.log_path),
                            }
                            if result == "PASS"
                            else None
                        ),
                    }
                )
            else:
                records.append(
                    {
                        "gate": gate,
                        "result": "N/A",
                        "command": None,
                        "exit_code": None,
                        "detail": "not needed by this focused readiness fixture",
                        "log": None,
                    }
                )
        return {
            "schema_version": "1.0",
            "run": {
                "id": "assurance-test",
                "risk": "yellow",
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
            "revision": repository_revision(ROOT),
            "environment": {
                "os": "test",
                "architecture": "test",
                "python": "test",
                "shell": "test",
            },
            "gates": records,
        }

    def test_current_passing_gate_is_machine_verified(self) -> None:
        result = evaluate_readiness(self.validation, self.evidence())
        self.assertEqual("READY", result["readiness"])
        self.assertEqual("MACHINE_VERIFIED", result["claims"][0]["machine"])

    def test_na_does_not_satisfy_required_gate(self) -> None:
        result = evaluate_readiness(self.validation, self.evidence("N/A"))
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertEqual("UNVERIFIED", result["claims"][0]["machine"])

    def test_stale_revision_blocks_readiness(self) -> None:
        evidence = self.evidence()
        evidence["revision"]["working_tree_fingerprint"] = "stale"
        result = evaluate_readiness(self.validation, evidence)
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertFalse(result["revision_current"])

    def test_pending_must_human_check_requires_action(self) -> None:
        validation = copy.deepcopy(self.validation)
        validation["data"]["claims"][0]["human_check_ids"] = ["HC-EVAL-001"]
        validation["human_checks"] = {
            "checks": [
                {
                    "id": "HC-EVAL-001",
                    "claim_ids": ["CLM-EVAL-001"],
                    "level": "must",
                    "status": "pending",
                }
            ]
        }
        result = evaluate_readiness(validation, self.evidence())
        self.assertEqual("ACTION_REQUIRED", result["readiness"])
        self.assertEqual("HUMAN_REQUIRED", result["claims"][0]["human"])

    def test_ai_review_alone_is_not_decisive(self) -> None:
        validation = copy.deepcopy(self.validation)
        validation["data"]["claims"][0]["evidence_requirements"] = [
            {
                "id": "EVR-EVAL-AI",
                "kind": "ai-review",
                "description": "Review fixture",
                "required": True,
                "artifact": "ai/evals/assurance/README.md",
            }
        ]
        result = evaluate_readiness(validation, self.evidence())
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertEqual("AI_REVIEWED", result["claims"][0]["ai_review"])

    def test_malformed_evidence_cannot_assert_ready(self) -> None:
        evidence = self.evidence()
        del evidence["run"]["id"]
        result = evaluate_readiness(self.validation, evidence)
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn("VALUE", {item["code"] for item in result["blockers"]})

    def test_lower_risk_evidence_cannot_satisfy_manifest(self) -> None:
        evidence = self.evidence()
        evidence["run"]["risk"] = "green"
        evidence["gates"] = [
            item for item in evidence["gates"] if item["gate"] in {"lint", "unit"}
        ]
        result = evaluate_readiness(self.validation, evidence)
        self.assertEqual("BLOCKED", result["readiness"])
        self.assertIn("RISK_UNDERSHOOT", {item["code"] for item in result["blockers"]})

    def test_required_agent_trace_is_enforced(self) -> None:
        validation = copy.deepcopy(self.validation)
        validation["data"]["agent_trace_expectation"] = {
            "required": True,
            "event_types": ["shell.execute"],
            "reason": "fixture",
        }
        missing = evaluate_readiness(validation, self.evidence())
        self.assertEqual("BLOCKED", missing["readiness"])
        self.assertEqual("UNVERIFIED", missing["agent_trace"])

        supplied = evaluate_readiness(
            validation,
            self.evidence(),
            trace_summary={
                "coverage": "declared-events-only",
                "action_counts": {"shell.execute": 1},
                "errors": [],
            },
        )
        self.assertEqual("READY", supplied["readiness"])
        self.assertEqual("declared-events-only", supplied["agent_trace"])


if __name__ == "__main__":
    unittest.main()
