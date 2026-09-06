#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class RiskClassifierTests(unittest.TestCase):
    def run_git(self, repository: Path, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        )

    def commit(self, repository: Path, message: str) -> None:
        self.run_git(repository, "add", ".")
        self.run_git(
            repository,
            "-c",
            "user.name=Harness Test",
            "-c",
            "user.email=harness-test@example.invalid",
            "commit",
            "-q",
            "-m",
            message,
        )

    def test_large_red_diff_cannot_be_downgraded_by_early_pipe_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            script = repository / "scripts" / "ai" / "classify-risk"
            script.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "scripts" / "ai" / "classify-risk", script)
            (repository / "README.md").write_text("fixture\n", encoding="utf-8")

            self.run_git(repository, "init", "-q")
            self.commit(repository, "baseline")

            policy = repository / "ai" / "policies" / "assurance.md"
            policy.parent.mkdir(parents=True)
            policy.write_text("large harness-sensitive change\n" * 20_000, encoding="utf-8")
            self.commit(repository, "large red change")

            result = subprocess.run(
                ["bash", str(script), "--base", "HEAD~1", "--format", "level"],
                cwd=repository,
                capture_output=True,
                text=True,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("red", result.stdout.strip())
        self.assertNotIn("Broken pipe", result.stderr)


if __name__ == "__main__":
    unittest.main()
