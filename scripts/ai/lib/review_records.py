"""Validate review records, not the truth of their authors' conclusions.

Reviewer identity, independence, oracle correctness and completeness are not
authenticated by this module. Machine evidence remains a separate requirement.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, fields: str, label: str) -> dict:
    expected = set(fields.split())
    _require(isinstance(value, dict), f"{label} must be an object")
    _require(
        set(value) == expected,
        f"{label} must contain exactly: {', '.join(sorted(expected))}",
    )
    return value


def _text(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and bool(value.strip()),
        f"{label} must be a non-empty string",
    )
    return value


def _enum(value: Any, choices: str, label: str) -> None:
    _require(
        isinstance(value, str) and value in choices.split(),
        f"{label} must be one of: {choices}",
    )


def _strings(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    _require(isinstance(value, list), f"{label} must be an array")
    _require(not nonempty or bool(value), f"{label} must not be empty")
    for item in value:
        _text(item, label)
    _require(len(value) == len(set(value)), f"{label} contains duplicates")
    return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _file(root: Path, raw: Any) -> Path:
    relative = Path(_text(raw, "path"))
    _require(not relative.is_absolute(), "path must be repository-relative")
    resolved = (root / relative).resolve()
    resolved.relative_to(root.resolve())
    _require(resolved.is_file(), f"file does not exist: {relative}")
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reference(
    root: Path,
    value: Any,
    review_path: Path,
    *,
    label: str,
) -> Path:
    _object(value, "path sha256", label)
    path = _file(root, value["path"])
    _require(path != review_path, "a review cannot cite itself as evidence")
    digest = _text(value["sha256"], f"{label}.sha256")
    _require(
        re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
        f"{label}.sha256 must be a lowercase SHA-256 digest",
    )
    _require(_sha256(path) == digest, f"evidence hash mismatch: {path}")
    return path


def _references(
    root: Path, values: Any, review_path: Path, *, required: bool
) -> None:
    _require(isinstance(values, list), "evidence must be an array")
    _require(not required or bool(values), "supporting evidence is required")
    paths = []
    for index, reference in enumerate(values):
        paths.append(
            _reference(
                root,
                reference,
                review_path,
                label=f"evidence[{index}]",
            )
        )
    _require(len(paths) == len(set(paths)), "evidence contains duplicate paths")


def validate_review(
    root: Path,
    artifact: Any,
    *,
    change_id: str,
    claim_id: str,
    manifest_claim_ids: set[str],
    evidence: dict,
) -> list[dict[str, str]]:
    """Return blocking issues. An empty list means record checks passed."""

    def issue(code: str, message: str) -> dict[str, str]:
        return {
            "code": code,
            "message": message,
            "location": str(artifact),
        }

    try:
        path = _file(root, artifact)

        # Keep exact-revision run records outside the tracked worktree.
        # Otherwise writing a review would invalidate its own revision.
        path.relative_to((root / ".ai-artifacts").resolve())
        _require(path.suffix == ".json", "review artifact must be JSON")
        _require(path.stat().st_size <= 1024 * 1024, "review exceeds 1 MiB")

        record = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
        _object(
            record,
            "schema_version change_id claim_ids revision verification reviewer "
            "verdict checks findings limitations",
            "review",
        )
        _require(record["schema_version"] == "1.0", "unsupported review version")
        _require(record["change_id"] == change_id, "review change_id mismatch")

        claims = _strings(record["claim_ids"], "claim_ids", nonempty=True)
        _require(claim_id in claims, "review does not cover this Claim")
        _require(
            set(claims) <= manifest_claim_ids,
            "review contains a Claim that is absent from the manifest",
        )

        _object(
            record["revision"],
            "commit dirty working_tree_fingerprint",
            "revision",
        )
        _require(
            record["revision"] == evidence.get("revision"),
            "review does not match the verification revision",
        )

        verification = _object(
            record["verification"], "run_id evidence", "verification"
        )
        run_id = _text(verification["run_id"], "verification.run_id")
        _require(
            run_id == evidence.get("run", {}).get("id"),
            "review does not match the verification run",
        )
        evidence_path = _reference(
            root,
            verification["evidence"],
            path,
            label="verification.evidence",
        )
        evidence_path.relative_to((root / ".ai-artifacts").resolve())
        reviewed_evidence = json.loads(
            evidence_path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
        _require(
            reviewed_evidence == evidence,
            "reviewed evidence file differs from supplied verification evidence",
        )

        reviewer = _object(record["reviewer"], "id kind context", "reviewer")
        _text(reviewer["id"], "reviewer.id")
        _require(
            reviewer["kind"] == "ai",
            "an ai-review-record requires reviewer.kind to be ai",
        )
        _enum(reviewer["context"], "fresh shared unknown", "reviewer.context")

        _enum(record["verdict"], "PENDING PASS BLOCKED", "verdict")
        _strings(record["limitations"], "limitations")

        checks = record["checks"]
        _require(isinstance(checks, list) and bool(checks), "checks are required")
        covered = set()
        adverse_claims = set()
        for check in checks:
            _object(
                check,
                "claim_id kind basis scenario expected observed evidence",
                "check",
            )
            _require(check["claim_id"] in claims, "unknown Claim in check")
            _enum(check["kind"], "example boundary counterexample", "check.kind")
            for key in ("basis", "scenario", "expected", "observed"):
                _text(check[key], f"check.{key}")
            _references(root, check["evidence"], path, required=True)
            covered.add(check["claim_id"])
            if check["kind"] in {"boundary", "counterexample"}:
                adverse_claims.add(check["claim_id"])
        _require(set(claims) <= covered, "some Claims have no review check")
        _require(
            set(claims) <= adverse_claims,
            "each Claim requires a relevant boundary or counterexample",
        )

        findings = record["findings"]
        _require(isinstance(findings, list), "findings must be an array")
        seen = set()
        issues = []
        for finding in findings:
            _object(
                finding,
                "id claim_ids origin target severity statement status resolution "
                "evidence",
                "finding",
            )
            identifier = _text(finding["id"], "finding.id")
            _require(identifier not in seen, "duplicate finding ID")
            seen.add(identifier)
            finding_claims = _strings(
                finding["claim_ids"], "finding.claim_ids", nonempty=True
            )
            _require(
                set(finding_claims) <= set(claims),
                "finding contains a Claim outside the review scope",
            )
            _enum(finding["origin"], "ai human", "finding.origin")
            _enum(
                finding["target"],
                "requirement implementation test explanation unknown",
                "finding.target",
            )
            _enum(finding["severity"], "blocking advisory", "finding.severity")
            _enum(finding["status"], "open resolved rejected", "finding.status")
            _text(finding["statement"], "finding.statement")
            _require(
                isinstance(finding["resolution"], str),
                "finding.resolution must be a string",
            )

            closed = finding["status"] in {"resolved", "rejected"}
            if closed:
                _text(finding["resolution"], "finding.resolution")
            _references(root, finding["evidence"], path, required=closed)

            if (
                finding["severity"] == "blocking"
                and not closed
            ):
                issues.append(
                    issue(
                        "UNRESOLVED_REVIEW_FINDING",
                        f"{identifier}: {finding['statement']}",
                    )
                )

        if record["verdict"] != "PASS":
            issues.append(
                issue("REVIEW_NOT_PASSING", f"verdict is {record['verdict']}")
            )
        return issues

    except (OSError, ValueError, RecursionError) as exc:
        return [issue("REVIEW_RECORD_INVALID", str(exc))]
