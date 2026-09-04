#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class ProjectIndexTests(unittest.TestCase):
    def test_claim_relationships_are_derived(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "project-index.json"
            subprocess.run(
                [
                    str(ROOT / "scripts" / "ai" / "build-project-index"),
                    "--manifest",
                    "ai/evals/assurance/valid/manifest.json",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            data = json.loads(output.read_text(encoding="utf-8"))

        node_ids = {node["id"] for node in data["nodes"]}
        edge_keys = {
            (edge["from"], edge["relation"], edge["to"]) for edge in data["edges"]
        }
        self.assertIn("REQUIREMENT:REQ-EVAL-001", node_ids)
        self.assertIn("CLAIM:CLM-EVAL-001", node_ids)
        self.assertIn("EVIDENCE_REQUIREMENT:EVR-EVAL-001", node_ids)
        self.assertIn(
            (
                "REQUIREMENT:REQ-EVAL-001",
                "supported_by",
                "CLAIM:CLM-EVAL-001",
            ),
            edge_keys,
        )
        self.assertIn(
            (
                "CLAIM:CLM-EVAL-001",
                "verified_by",
                "EVIDENCE_REQUIREMENT:EVR-EVAL-001",
            ),
            edge_keys,
        )


if __name__ == "__main__":
    unittest.main()
