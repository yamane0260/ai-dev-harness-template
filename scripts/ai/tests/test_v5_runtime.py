from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from lib.v5_core import (
    build_verifier_packet,
    contract_fingerprint,
    detect_domains,
    guard_acceptance,
    guard_result,
    next_action,
    preflight,
    repository_fingerprint,
    risk_floor,
    run_verification,
    validate_acceptance_verdict,
    validate_scan,
    validate_task,
)


def task(**overrides):
    value = {
        "version": 1,
        "id": "t1",
        "goal": "Change behavior safely",
        "acceptance": ["Expected behavior is observable"],
        "invariants": ["Existing success behavior remains unchanged"],
        "baseline": [],
        "constraints": [],
        "scope": ["src/service.py"],
        "mustNot": [],
        "riskHints": [],
        "domainHints": [],
        "verification": [],
        "evidenceKinds": ["test"],
        "metadata": {},
    }
    value.update(overrides)
    return value


def config(command="true"):
    return {
        "version": 1,
        "gates": {"basic": {"command": command, "kind": "test", "timeoutSeconds": 5}},
        "riskGates": {"GREEN": ["basic"], "YELLOW": ["basic"], "RED": ["basic"]},
        "domainGates": {domain: [] for domain in ("security", "ux", "data", "reliability", "architecture")},
    }


def scan():
    return {
        "version": 1,
        "lenses": {
            name: {"status": "clear", "note": "checked"}
            for name in ("correctness", "boundary", "failure", "work_fit", "simplicity")
        },
        "escalations": [],
        "blockingUnknowns": [],
    }


def result():
    return {
        "version": 1,
        "taskId": "t1",
        "status": "implemented",
        "changedPaths": [],
        "decisions": [],
        "residualRisks": [],
        "assumptions": [],
        "escalation": None,
    }


class V5RuntimeTests(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        (root / "a.txt").write_text("hello\n", encoding="utf-8")
        subprocess.run(["git", "add", "a.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=root, check=True)

    def verdict(self, value, root, independent=False, holdout_status="not_used", holdout_reason=""):
        contract_hash = contract_fingerprint(value)
        return {
            "version": 1,
            "taskId": value["id"],
            "contractHash": contract_hash,
            "repository": repository_fingerprint(root),
            "independentContext": independent,
            "holdout": {"status": holdout_status, "reason": holdout_reason},
            "acceptance": [
                {"text": x, "status": "pass", "evidence": ["direct-observation:acceptance"]}
                for x in validate_task(value)["acceptance"]
            ],
            "invariants": [
                {"text": x, "status": "pass", "evidence": ["direct-observation:invariant"]}
                for x in validate_task(value)["invariants"]
            ],
            "baseline": [
                {"text": x, "status": "pass", "evidence": ["snapshot:before-after"]}
                for x in validate_task(value)["baseline"]
            ],
            "unresolved": [],
        }

    def test_task_requires_acceptance(self):
        with self.assertRaises(ValueError):
            validate_task(task(acceptance=[]))

    def test_contract_hash_changes_with_invariant(self):
        self.assertNotEqual(
            contract_fingerprint(task()),
            contract_fingerprint(task(invariants=["Different invariant"])),
        )

    def test_scan_requires_all_lenses(self):
        value = scan()
        value["lenses"].pop("work_fit")
        with self.assertRaises(ValueError):
            validate_scan(value)

    def test_auth_is_red_and_security_routed(self):
        value = task(scope=["src/auth/session.py"])
        risk, _ = risk_floor(value, value["scope"])
        self.assertEqual("RED", risk)
        self.assertIn("security", detect_domains(value, value["scope"]))

    def test_ui_is_yellow_and_ux_routed(self):
        value = task(scope=["src/components/Form.tsx"])
        risk, _ = risk_floor(value, value["scope"])
        self.assertEqual("YELLOW", risk)
        self.assertIn("ux", detect_domains(value, value["scope"]))

    def test_plain_change_can_be_green(self):
        risk, _ = risk_floor(task(), ["src/service.py"])
        self.assertEqual("GREEN", risk)

    def test_verification_and_handoff(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task()
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            self.assertTrue(evidence["passed"])
            self.assertEqual(repository_fingerprint(root), evidence["repository"])
            verdict = guard_result(value, pf, scan(), evidence, result(), root)
            self.assertTrue(verdict["ok"])

    def test_missing_required_evidence_kind_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task(evidenceKinds=["browser"])
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            verdict = guard_result(value, pf, scan(), evidence, result(), root)
            self.assertFalse(verdict["ok"])
            self.assertTrue(any("browser" in reason for reason in verdict["reasons"]))

    def test_stale_evidence_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task()
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            (root / "a.txt").write_text("changed\n", encoding="utf-8")
            verdict = guard_result(value, pf, scan(), evidence, result(), root)
            self.assertFalse(verdict["ok"])
            self.assertTrue(any("stale" in reason for reason in verdict["reasons"]))

    def test_changed_contract_blocks_old_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            original = task()
            pf = preflight(original, original["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(original))
            changed = task(acceptance=["A new acceptance condition"])
            verdict = guard_result(changed, pf, scan(), evidence, result(), root)
            self.assertFalse(verdict["ok"])
            self.assertTrue(any("different acceptance contract" in reason for reason in verdict["reasons"]))

    def test_verifier_packet_excludes_worker_narrative(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task()
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            packet = build_verifier_packet(value, pf, evidence, root)
            self.assertNotIn("decisions", packet)
            self.assertNotIn("assumptions", packet)
            self.assertIn("independenceRule", packet)

    def test_yellow_requires_fresh_verifier(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task(riskHints=["api"])
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            packet = build_verifier_packet(value, pf, evidence, root)
            acceptance = self.verdict(value, root, independent=False)
            verdict = guard_acceptance(value, pf, packet, acceptance, root)
            self.assertFalse(verdict["ok"])
            self.assertTrue(any("fresh independent" in reason for reason in verdict["reasons"]))

    def test_red_requires_holdout_or_justification(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task(riskHints=["auth"])
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            packet = build_verifier_packet(value, pf, evidence, root)
            acceptance = self.verdict(value, root, independent=True)
            verdict = guard_acceptance(value, pf, packet, acceptance, root)
            self.assertFalse(verdict["ok"])
            acceptance = self.verdict(value, root, independent=True, holdout_status="not_applicable", holdout_reason="No executable holdout exists; direct security review used.")
            verdict = guard_acceptance(value, pf, packet, acceptance, root)
            self.assertTrue(verdict["ok"])

    def test_baseline_requires_explicit_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task(baseline=["Legacy API response stays byte-compatible"])
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root, contract_fingerprint(value))
            packet = build_verifier_packet(value, pf, evidence, root)
            acceptance = self.verdict(value, root)
            acceptance["baseline"] = []
            verdict = guard_acceptance(value, pf, packet, acceptance, root)
            self.assertFalse(verdict["ok"])
            self.assertTrue(any("baseline missing" in reason for reason in verdict["reasons"]))

    def test_verdict_rejects_pass_without_evidence(self):
        value = {
            "version": 1,
            "taskId": "t1",
            "contractHash": "x",
            "repository": {},
            "independentContext": True,
            "holdout": {"status": "used", "reason": ""},
            "acceptance": [{"text": "x", "status": "pass", "evidence": []}],
            "invariants": [],
            "baseline": [],
            "unresolved": [],
        }
        with self.assertRaises(ValueError):
            validate_acceptance_verdict(value)

    def test_loop_guard_stops_repeated_implementation_retry(self):
        classification = {
            "version": 1,
            "taskId": "t1",
            "class": "implementation",
            "reason": "same assertion still fails",
            "sameFailureCount": 2,
            "designChangeCount": 0,
            "regression": False,
        }
        self.assertEqual("fresh_diagnosis", next_action(classification)["action"])

    def test_oracle_failure_repairs_verification_not_code(self):
        classification = {
            "version": 1,
            "taskId": "t1",
            "class": "oracle",
            "reason": "acceptance test asserts the wrong legacy response",
            "sameFailureCount": 1,
            "designChangeCount": 0,
            "regression": False,
        }
        self.assertEqual("repair_verification", next_action(classification)["action"])


if __name__ == "__main__":
    unittest.main()
