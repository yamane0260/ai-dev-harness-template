#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "ai"))

from lib.agent_trace import sensitive_target


class AgentTraceRedactionTests(unittest.TestCase):
    def test_repository_path_is_safe_metadata(self) -> None:
        self.assertFalse(sensitive_target("scripts/ai/verify"))

    def test_bearer_token_is_rejected(self) -> None:
        self.assertTrue(sensitive_target("Authorization: Bearer abcdefghijklmnop"))

    def test_github_token_is_rejected(self) -> None:
        self.assertTrue(sensitive_target("ghp_abcdefghijklmnopqrstuvwxyz123456"))

    def test_url_userinfo_is_rejected(self) -> None:
        self.assertTrue(sensitive_target("https://user:password@example.com/path"))

    def test_multiline_payload_is_rejected(self) -> None:
        self.assertTrue(sensitive_target("shell.execute\nfull command output"))

    def test_query_string_secret_is_rejected(self) -> None:
        self.assertTrue(sensitive_target("https://example.test/?token=abcd1234"))


if __name__ == "__main__":
    unittest.main()
