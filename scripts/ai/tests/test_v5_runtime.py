from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from lib.v5_core import (
    detect_domains,
    guard_result,
    preflight,
    repository_fingerprint,
    risk_floor,
    run_verification,
    validate_scan,
    validate_task,
)


def task(**overrides):
    value = {
        "version": 1,
        "id": "t1",
        "goal": "Change behavior safely",
        "acceptance": ["Expected behavior is observable"],
        "constraints": [],
        "scope": ["src/service.py"],
        "mustNot": [],
        "riskHints": [],
        "domainHints": [],
        "verification": [],
        "metadata": {},
    }
    value.update(overrides)
    return value


def config(command="true"):
    return {
        "version": 1,
        "gates": {"basic": {"command": command, "timeoutSeconds": 5}},
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


class V5RuntimeTests(unittest.TestCase):
    def init_repo(self, root):
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        (root / "a.txt").write_text("hello\n", encoding="utf-8")
        subprocess.run(["git", "add", "a.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=root, check=True)

    def test_task_requires_acceptance(self):
        with self.assertRaises(ValueError):
            validate_task(task(acceptance=[]))

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
            evidence = run_verification(pf["requiredGates"], config(), root)
            self.assertTrue(evidence["passed"])
            self.assertEqual(repository_fingerprint(root), evidence["repository"])
            result = {
                "version": 1,
                "taskId": "t1",
                "status": "implemented",
                "changedPaths": [],
                "decisions": [],
                "residualRisks": [],
                "assumptions": [],
                "escalation": None,
            }
            verdict = guard_result(value, pf, scan(), evidence, result, root)
            self.assertTrue(verdict["ok"])

    def test_stale_evidence_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.init_repo(root)
            value = task()
            pf = preflight(value, value["scope"], config(), root)
            evidence = run_verification(pf["requiredGates"], config(), root)
            (root / "a.txt").write_text("changed\n", encoding="utf-8")
            result = {
                "version": 1,
                "taskId": "t1",
                "status": "implemented",
                "changedPaths": ["a.txt"],
                "decisions": [],
                "residualRisks": [],
                "assumptions": [],
                "escalation": None,
            }
            verdict = guard_result(value, pf, scan(), evidence, result, root)
            self.assertFalse(verdict["ok"])
            self.assertTrue(any("stale" in reason for reason in verdict["reasons"]))


if __name__ == "__main__":
    unittest.main()
