"""Shared validation helpers for sanitized agent event metadata."""

from __future__ import annotations

import re


SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{7,127}$")
SENSITIVE_PATTERNS = [
    re.compile(r"(?i)authorization\s*:"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{8,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"://[^/\s:@]+:[^/\s@]+@"),
    re.compile(r"(?i)(token|password|secret|api[_-]?key)=[^&\s]{4,}"),
]


def sensitive_target(value: str) -> bool:
    return (
        not value
        or len(value) > 256
        or "\n" in value
        or "\r" in value
        or any(pattern.search(value) for pattern in SENSITIVE_PATTERNS)
    )
