#!/usr/bin/env python3
"""Validation and readiness logic for the V3 assurance layer."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


GATES = {
    "typecheck",
    "lint",
    "unit",
    "integration",
    "e2e",
    "build",
    "security",
    "dependency",
    "architecture",
    "visual",
}
RISK_GATES = {
    "green": {"lint", "unit"},
    "yellow": {"typecheck", "lint", "unit", "integration", "build", "security", "architecture"},
    "red": GATES,
}
EVENT_TYPES = {
    "file.read",
    "file.write",
    "shell.execute",
    "network.request",
    "tool.call",
    "credential.access",
    "git.push",
    "release.deploy",
    "subagent.invoke",
}
ID_PATTERNS = {
    "change": re.compile(r"^CHG-[A-Za-z0-9][A-Za-z0-9._-]*$"),
    "requirement": re.compile(r"^REQ-[A-Za-z0-9][A-Za-z0-9._-]*$"),
    "claim": re.compile(r"^CLM-[A-Za-z0-9][A-Za-z0-9._-]*$"),
    "evidence": re.compile(r"^EVR-[A-Za-z0-9][A-Za-z0-9._-]*$"),
    "human_check": re.compile(r"^HC-[A-Za-z0-9][A-Za-z0-9._-]*$"),
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "ai").is_dir():
            return candidate
    raise ValueError(f"cannot locate repository root from {start}")


def _run_git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], stderr=subprocess.DEVNULL
    )


def repository_revision(root: Path) -> dict[str, Any]:
    commit = _run_git(root, "rev-parse", "HEAD").decode().strip()
    status = _run_git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    return {
        "commit": commit,
        "dirty": bool(status),
        "working_tree_fingerprint": working_tree_fingerprint(root, commit),
    }


def working_tree_fingerprint(root: Path, commit: str | None = None) -> str:
    """Hash HEAD, tracked diffs, and untracked file content; ignored artifacts are excluded."""

    if commit is None:
        commit = _run_git(root, "rev-parse", "HEAD").decode().strip()
    digest = hashlib.sha256()
    digest.update(b"commit\0")
    digest.update(commit.encode())
    digest.update(b"\0unstaged\0")
    digest.update(_run_git(root, "diff", "--binary", "HEAD", "--", "."))
    digest.update(b"\0staged\0")
    digest.update(_run_git(root, "diff", "--cached", "--binary", "HEAD", "--", "."))

    untracked = _run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    for raw_path in sorted(item for item in untracked.split(b"\0") if item):
        relative = raw_path.decode("utf-8", errors="surrogateescape")
        path = root / relative
        digest.update(b"\0untracked\0")
        digest.update(raw_path)
        digest.update(b"\0")
        if path.is_symlink():
            digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        elif path.is_file():
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _issue(code: str, message: str, location: str = "") -> dict[str, str]:
    item = {"code": code, "message": message}
    if location:
        item["location"] = location
    return item


def _check_object(
    value: Any,
    required: Iterable[str],
    allowed: Iterable[str],
    location: str,
    errors: list[dict[str, str]],
) -> bool:
    if not isinstance(value, dict):
        errors.append(_issue("TYPE", "must be an object", location))
        return False
    required_set = set(required)
    allowed_set = set(allowed)
    for key in sorted(required_set - set(value)):
        errors.append(_issue("MISSING_FIELD", f"missing required field '{key}'", location))
    for key in sorted(set(value) - allowed_set):
        errors.append(_issue("UNKNOWN_FIELD", f"unknown field '{key}'", location))
    return True


def _nonempty_string(
    value: Any, location: str, errors: list[dict[str, str]]
) -> bool:
    if not isinstance(value, str) or not value.strip():
        errors.append(_issue("VALUE", "must be a non-empty string", location))
        return False
    return True


def _string_list(
    value: Any,
    location: str,
    errors: list[dict[str, str]],
    *,
    require_nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(_issue("TYPE", "must be an array", location))
        return []
    if require_nonempty and not value:
        errors.append(_issue("VALUE", "must not be empty", location))
    result: list[str] = []
    for index, item in enumerate(value):
        if _nonempty_string(item, f"{location}[{index}]", errors):
            result.append(item)
    if len(result) != len(set(result)):
        errors.append(_issue("DUPLICATE", "must not contain duplicate values", location))
    return result


def _valid_id(
    value: Any, kind: str, location: str, errors: list[dict[str, str]]
) -> bool:
    if not _nonempty_string(value, location, errors):
        return False
    if not ID_PATTERNS[kind].fullmatch(value):
        errors.append(_issue("ID_FORMAT", f"invalid {kind} ID '{value}'", location))
        return False
    return True


def _repo_relative_path(
    root: Path, raw: str, location: str, errors: list[dict[str, str]]
) -> Path | None:
    path = Path(raw)
    if path.is_absolute():
        errors.append(_issue("PATH", "must be repository-relative", location))
        return None
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(_issue("PATH", "must not escape the repository", location))
        return None
    return resolved


def _validate_schema_ref(
    base: Path, value: Any, location: str, errors: list[dict[str, str]]
) -> None:
    if value is None:
        return
    if not _nonempty_string(value, location, errors):
        return
    if "://" in value or value.startswith("urn:"):
        return
    resolved = (base / value).resolve()
    if not resolved.is_file():
        errors.append(
            _issue("SCHEMA_REFERENCE", f"local schema does not exist: {value}", location)
        )


def _parse_datetime(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_assurance(manifest_path: Path) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    root = find_repo_root(manifest_path)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "valid": False,
            "manifest": str(manifest_path),
            "errors": [_issue("JSON", str(exc))],
            "warnings": [],
        }

    manifest_keys = {
        "$schema",
        "schema_version",
        "change",
        "requirements",
        "claims",
        "human_checks_file",
        "references",
        "agent_trace_expectation",
    }
    if not _check_object(
        manifest,
        {
            "schema_version",
            "change",
            "requirements",
            "claims",
            "human_checks_file",
            "references",
        },
        manifest_keys,
        "manifest",
        errors,
    ):
        return {
            "valid": False,
            "manifest": str(manifest_path),
            "errors": errors,
            "warnings": warnings,
        }

    if manifest.get("schema_version") != "1.0":
        errors.append(_issue("SCHEMA_VERSION", "schema_version must be '1.0'"))
    _validate_schema_ref(manifest_path.parent, manifest.get("$schema"), "$schema", errors)

    change = manifest.get("change")
    if _check_object(
        change,
        {"id", "title", "risk", "knowledge_impact", "status"},
        {"id", "title", "risk", "knowledge_impact", "status"},
        "change",
        errors,
    ):
        _valid_id(change.get("id"), "change", "change.id", errors)
        _nonempty_string(change.get("title"), "change.title", errors)
        if change.get("risk") not in {"green", "yellow", "red"}:
            errors.append(_issue("ENUM", "risk must be green/yellow/red", "change.risk"))
        if change.get("knowledge_impact") not in {
            "none",
            "low",
            "material",
            "critical",
        }:
            errors.append(
                _issue(
                    "ENUM",
                    "knowledge_impact must be none/low/material/critical",
                    "change.knowledge_impact",
                )
            )
        if change.get("status") not in {"draft", "active", "ready", "released"}:
            errors.append(
                _issue("ENUM", "status must be draft/active/ready/released", "change.status")
            )

    requirements = manifest.get("requirements")
    requirement_ids: set[str] = set()
    if not isinstance(requirements, list) or not requirements:
        errors.append(_issue("VALUE", "requirements must be a non-empty array", "requirements"))
        requirements = []
    for index, requirement in enumerate(requirements):
        location = f"requirements[{index}]"
        if not _check_object(
            requirement,
            {"id", "statement", "source"},
            {"id", "statement", "source"},
            location,
            errors,
        ):
            continue
        req_id = requirement.get("id")
        if _valid_id(req_id, "requirement", f"{location}.id", errors):
            if req_id in requirement_ids:
                errors.append(_issue("DUPLICATE_ID", f"duplicate ID '{req_id}'", location))
            requirement_ids.add(req_id)
        _nonempty_string(requirement.get("statement"), f"{location}.statement", errors)
        _nonempty_string(requirement.get("source"), f"{location}.source", errors)

    claims = manifest.get("claims")
    claim_ids: set[str] = set()
    evidence_ids: set[str] = set()
    used_requirement_ids: set[str] = set()
    if not isinstance(claims, list) or not claims:
        errors.append(_issue("VALUE", "claims must be a non-empty array", "claims"))
        claims = []
    for index, claim in enumerate(claims):
        location = f"claims[{index}]"
        claim_keys = {
            "id",
            "statement",
            "criticality",
            "requirement_ids",
            "scope",
            "evidence_requirements",
            "human_check_ids",
            "residual_uncertainty",
        }
        if not _check_object(claim, claim_keys, claim_keys, location, errors):
            continue
        claim_id = claim.get("id")
        if _valid_id(claim_id, "claim", f"{location}.id", errors):
            if claim_id in claim_ids:
                errors.append(_issue("DUPLICATE_ID", f"duplicate ID '{claim_id}'", location))
            claim_ids.add(claim_id)
        _nonempty_string(claim.get("statement"), f"{location}.statement", errors)
        if claim.get("criticality") not in {"must", "should"}:
            errors.append(
                _issue("ENUM", "criticality must be must/should", f"{location}.criticality")
            )
        linked_requirements = _string_list(
            claim.get("requirement_ids"),
            f"{location}.requirement_ids",
            errors,
            require_nonempty=True,
        )
        for req_id in linked_requirements:
            used_requirement_ids.add(req_id)
            if req_id not in requirement_ids:
                errors.append(
                    _issue(
                        "UNKNOWN_REFERENCE",
                        f"unknown requirement ID '{req_id}'",
                        f"{location}.requirement_ids",
                    )
                )

        scope = claim.get("scope")
        if _check_object(
            scope,
            {"components", "paths"},
            {"components", "paths"},
            f"{location}.scope",
            errors,
        ):
            components = _string_list(
                scope.get("components"), f"{location}.scope.components", errors
            )
            paths = _string_list(scope.get("paths"), f"{location}.scope.paths", errors)
            if not components and not paths:
                errors.append(
                    _issue(
                        "EMPTY_SCOPE",
                        "at least one component or path is required",
                        f"{location}.scope",
                    )
                )

        evidence_requirements = claim.get("evidence_requirements")
        if not isinstance(evidence_requirements, list):
            errors.append(
                _issue("TYPE", "must be an array", f"{location}.evidence_requirements")
            )
            evidence_requirements = []
        linked_checks = _string_list(
            claim.get("human_check_ids"), f"{location}.human_check_ids", errors
        )
        required_evidence = [
            item
            for item in evidence_requirements
            if isinstance(item, dict) and item.get("required") is True
        ]
        if claim.get("criticality") == "must" and not required_evidence and not linked_checks:
            errors.append(
                _issue(
                    "UNSUPPORTED_MUST_CLAIM",
                    "a must Claim needs evidence requirements or a Human Check",
                    location,
                )
            )
        for evidence_index, evidence in enumerate(evidence_requirements):
            evidence_location = f"{location}.evidence_requirements[{evidence_index}]"
            evidence_keys = {
                "id",
                "kind",
                "description",
                "required",
                "gate",
                "locator",
                "artifact",
            }
            if not _check_object(
                evidence,
                {"id", "kind", "description", "required"},
                evidence_keys,
                evidence_location,
                errors,
            ):
                continue
            evidence_id = evidence.get("id")
            if _valid_id(evidence_id, "evidence", f"{evidence_location}.id", errors):
                if evidence_id in evidence_ids:
                    errors.append(
                        _issue("DUPLICATE_ID", f"duplicate ID '{evidence_id}'", evidence_location)
                    )
                evidence_ids.add(evidence_id)
            _nonempty_string(
                evidence.get("description"), f"{evidence_location}.description", errors
            )
            if not isinstance(evidence.get("required"), bool):
                errors.append(
                    _issue("TYPE", "required must be boolean", f"{evidence_location}.required")
                )
            kind = evidence.get("kind")
            if kind not in {"gate", "ai-review"}:
                errors.append(
                    _issue("ENUM", "kind must be gate/ai-review", f"{evidence_location}.kind")
                )
            elif kind == "gate":
                if evidence.get("gate") not in GATES:
                    errors.append(
                        _issue("ENUM", "gate is not supported", f"{evidence_location}.gate")
                    )
                _nonempty_string(
                    evidence.get("locator"), f"{evidence_location}.locator", errors
                )
            elif kind == "ai-review":
                artifact = evidence.get("artifact")
                if _nonempty_string(artifact, f"{evidence_location}.artifact", errors):
                    artifact_path = _repo_relative_path(
                        root, artifact, f"{evidence_location}.artifact", errors
                    )
                    if artifact_path is not None and not artifact_path.is_file():
                        warnings.append(
                            _issue(
                                "MISSING_REVIEW_ARTIFACT",
                                f"AI review artifact does not exist yet: {artifact}",
                                evidence_location,
                            )
                        )
        _nonempty_string(
            claim.get("residual_uncertainty"), f"{location}.residual_uncertainty", errors
        )

    for requirement_id in sorted(requirement_ids - used_requirement_ids):
        errors.append(
            _issue(
                "UNMAPPED_REQUIREMENT",
                f"requirement '{requirement_id}' is not linked to any Claim",
                "requirements",
            )
        )

    references = manifest.get("references")
    reference_keys = {"specs", "decisions", "concepts", "runbooks"}
    if _check_object(
        references, reference_keys, reference_keys, "references", errors
    ):
        for group in sorted(reference_keys):
            for index, raw_path in enumerate(
                _string_list(references.get(group), f"references.{group}", errors)
            ):
                resolved = _repo_relative_path(
                    root, raw_path, f"references.{group}[{index}]", errors
                )
                if resolved is not None and not resolved.is_file():
                    errors.append(
                        _issue(
                            "MISSING_REFERENCE",
                            f"referenced file does not exist yet: {raw_path}",
                            f"references.{group}[{index}]",
                        )
                    )

    trace = manifest.get("agent_trace_expectation")
    if trace is not None and _check_object(
        trace,
        {"required", "event_types", "reason"},
        {"required", "event_types", "reason"},
        "agent_trace_expectation",
        errors,
    ):
        if not isinstance(trace.get("required"), bool):
            errors.append(_issue("TYPE", "required must be boolean", "agent_trace_expectation"))
        event_types = _string_list(
            trace.get("event_types"), "agent_trace_expectation.event_types", errors
        )
        for event_type in event_types:
            if event_type not in EVENT_TYPES:
                errors.append(
                    _issue(
                        "ENUM",
                        f"unsupported agent event type '{event_type}'",
                        "agent_trace_expectation.event_types",
                    )
                )
        _nonempty_string(trace.get("reason"), "agent_trace_expectation.reason", errors)
        if trace.get("required") and not event_types:
            errors.append(
                _issue(
                    "TRACE_EXPECTATION",
                    "required agent tracing needs at least one event type",
                    "agent_trace_expectation",
                )
            )

    human_checks_file = manifest.get("human_checks_file")
    human_checks: dict[str, Any] = {"checks": []}
    human_path: Path | None = None
    if _nonempty_string(human_checks_file, "human_checks_file", errors):
        candidate = (manifest_path.parent / human_checks_file).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(_issue("PATH", "human_checks_file escapes repository", "human_checks_file"))
        else:
            human_path = candidate
            if not candidate.is_file():
                errors.append(
                    _issue(
                        "MISSING_HUMAN_CHECKS",
                        f"human checks file does not exist: {candidate}",
                        "human_checks_file",
                    )
                )
            else:
                try:
                    human_checks = load_json(candidate)
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(_issue("JSON", str(exc), "human_checks_file"))

    checks_by_id: dict[str, dict[str, Any]] = {}
    if human_path is not None and human_path.is_file():
        check_keys = {"$schema", "schema_version", "change_id", "checks"}
        if _check_object(
            human_checks,
            {"schema_version", "change_id", "checks"},
            check_keys,
            "human_checks",
            errors,
        ):
            _validate_schema_ref(
                human_path.parent,
                human_checks.get("$schema"),
                "human_checks.$schema",
                errors,
            )
            if human_checks.get("schema_version") != "1.0":
                errors.append(
                    _issue("SCHEMA_VERSION", "schema_version must be '1.0'", "human_checks")
                )
            if isinstance(change, dict) and human_checks.get("change_id") != change.get("id"):
                errors.append(
                    _issue(
                        "CHANGE_ID_MISMATCH",
                        "human checks change_id does not match manifest",
                        "human_checks.change_id",
                    )
                )
            checks = human_checks.get("checks")
            if not isinstance(checks, list):
                errors.append(_issue("TYPE", "checks must be an array", "human_checks.checks"))
                checks = []
            for index, check in enumerate(checks):
                location = f"human_checks.checks[{index}]"
                required_keys = {
                    "id",
                    "claim_ids",
                    "level",
                    "statement",
                    "reason",
                    "procedure",
                    "expected",
                    "status",
                    "performed_by",
                    "performed_at",
                    "evidence",
                }
                allowed_keys = required_keys | {"not_applicable_reason"}
                if not _check_object(check, required_keys, allowed_keys, location, errors):
                    continue
                check_id = check.get("id")
                if _valid_id(check_id, "human_check", f"{location}.id", errors):
                    if check_id in checks_by_id:
                        errors.append(
                            _issue("DUPLICATE_ID", f"duplicate ID '{check_id}'", location)
                        )
                    checks_by_id[check_id] = check
                for claim_id in _string_list(
                    check.get("claim_ids"),
                    f"{location}.claim_ids",
                    errors,
                    require_nonempty=True,
                ):
                    if claim_id not in claim_ids:
                        errors.append(
                            _issue(
                                "UNKNOWN_REFERENCE",
                                f"unknown Claim ID '{claim_id}'",
                                f"{location}.claim_ids",
                            )
                        )
                if check.get("level") not in {"must", "should", "optional"}:
                    errors.append(
                        _issue("ENUM", "level must be must/should/optional", f"{location}.level")
                    )
                for field in ("statement", "reason", "expected"):
                    _nonempty_string(check.get(field), f"{location}.{field}", errors)
                _string_list(
                    check.get("procedure"),
                    f"{location}.procedure",
                    errors,
                    require_nonempty=True,
                )
                status = check.get("status")
                if status not in {"pending", "passed", "failed", "not_applicable"}:
                    errors.append(
                        _issue(
                            "ENUM",
                            "status must be pending/passed/failed/not_applicable",
                            f"{location}.status",
                        )
                    )
                if status in {"passed", "failed"}:
                    for field in ("performed_by", "performed_at", "evidence"):
                        _nonempty_string(check.get(field), f"{location}.{field}", errors)
                    performed_at = check.get("performed_at")
                    if isinstance(performed_at, str) and not _parse_datetime(performed_at):
                        errors.append(
                            _issue(
                                "DATETIME",
                                "performed_at must be ISO 8601",
                                f"{location}.performed_at",
                            )
                        )
                elif status == "pending":
                    if any(check.get(field) is not None for field in ("performed_by", "performed_at", "evidence")):
                        errors.append(
                            _issue(
                                "PENDING_METADATA",
                                "pending check must not contain completion metadata",
                                location,
                            )
                        )
                elif status == "not_applicable":
                    _nonempty_string(
                        check.get("not_applicable_reason"),
                        f"{location}.not_applicable_reason",
                        errors,
                    )

    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("id")
        for check_id in claim.get("human_check_ids", []) if isinstance(claim.get("human_check_ids"), list) else []:
            if check_id not in checks_by_id:
                errors.append(
                    _issue(
                        "UNKNOWN_REFERENCE",
                        f"unknown Human Check ID '{check_id}'",
                        f"claims[{index}].human_check_ids",
                    )
                )
            elif claim_id not in checks_by_id[check_id].get("claim_ids", []):
                errors.append(
                    _issue(
                        "ASYMMETRIC_REFERENCE",
                        f"Human Check '{check_id}' does not link back to Claim '{claim_id}'",
                        f"claims[{index}].human_check_ids",
                    )
                )
    for check_id, check in checks_by_id.items():
        for claim_id in check.get("claim_ids", []):
            matching = next(
                (claim for claim in claims if isinstance(claim, dict) and claim.get("id") == claim_id),
                None,
            )
            if matching is not None and check_id not in matching.get("human_check_ids", []):
                errors.append(
                    _issue(
                        "ASYMMETRIC_REFERENCE",
                        f"Claim '{claim_id}' does not link back to Human Check '{check_id}'",
                        f"human_checks.{check_id}",
                    )
                )

    for index, claim in enumerate(claims):
        if not isinstance(claim, dict) or claim.get("criticality") != "must":
            continue
        required_gate = any(
            isinstance(item, dict)
            and item.get("required") is True
            and item.get("kind") == "gate"
            for item in claim.get("evidence_requirements", [])
        )
        if required_gate:
            continue
        linked = [checks_by_id.get(check_id) for check_id in claim.get("human_check_ids", [])]
        if not any(check and check.get("level") == "must" for check in linked):
            errors.append(
                _issue(
                    "NO_DECISIVE_PLAN",
                    "a must Claim without a required machine gate needs a MUST Human Check",
                    f"claims[{index}]",
                )
            )

    return {
        "valid": not errors,
        "manifest": str(manifest_path.relative_to(root)),
        "root": str(root),
        "change_id": change.get("id") if isinstance(change, dict) else None,
        "errors": errors,
        "warnings": warnings,
        "data": manifest,
        "human_checks": human_checks,
    }


def validate_evidence_record(
    evidence: Any, root: Path | None = None
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(evidence, dict):
        return [_issue("EVIDENCE_FORMAT", "evidence must be an object")]
    if evidence.get("schema_version") != "1.0":
        errors.append(_issue("EVIDENCE_SCHEMA", "evidence schema_version must be '1.0'"))

    run = evidence.get("run")
    if not isinstance(run, dict):
        errors.append(_issue("EVIDENCE_FORMAT", "evidence.run must be an object"))
        run = {}
    _nonempty_string(run.get("id"), "evidence.run.id", errors)
    risk = run.get("risk")
    if risk not in RISK_GATES:
        errors.append(_issue("EVIDENCE_RISK", "evidence run risk is missing or invalid"))
    recorded_at = run.get("recorded_at")
    if not isinstance(recorded_at, str) or not _parse_datetime(recorded_at):
        errors.append(_issue("EVIDENCE_TIME", "recorded_at must be timezone-aware ISO 8601"))

    revision = evidence.get("revision")
    if not isinstance(revision, dict):
        errors.append(_issue("EVIDENCE_FORMAT", "evidence.revision must be an object"))
        revision = {}
    commit = revision.get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        errors.append(
            _issue("EVIDENCE_FORMAT", "revision.commit must be a full Git object ID")
        )
    if not isinstance(revision.get("dirty"), bool):
        errors.append(_issue("EVIDENCE_FORMAT", "revision.dirty must be boolean"))
    fingerprint = revision.get("working_tree_fingerprint")
    if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
        errors.append(
            _issue("EVIDENCE_FORMAT", "working_tree_fingerprint must be a SHA-256 hex value")
        )

    environment = evidence.get("environment")
    if not isinstance(environment, dict):
        errors.append(_issue("EVIDENCE_FORMAT", "evidence.environment must be an object"))
    else:
        for field in ("os", "architecture", "python", "shell"):
            _nonempty_string(environment.get(field), f"evidence.environment.{field}", errors)

    gates = evidence.get("gates")
    if not isinstance(gates, list):
        errors.append(_issue("EVIDENCE_FORMAT", "evidence.gates must be an array"))
        return errors
    seen_gates: set[str] = set()
    gate_results: dict[str, str] = {}
    for index, gate_record in enumerate(gates):
        location = f"evidence.gates[{index}]"
        if not isinstance(gate_record, dict):
            errors.append(_issue("EVIDENCE_FORMAT", "gate record must be an object", location))
            continue
        gate = gate_record.get("gate")
        if gate not in GATES:
            errors.append(_issue("EVIDENCE_GATE", f"unsupported gate '{gate}'", location))
            continue
        if gate in seen_gates:
            errors.append(_issue("EVIDENCE_GATE", f"duplicate gate '{gate}'", location))
        seen_gates.add(gate)
        result = gate_record.get("result")
        gate_results[gate] = result
        if result not in {"PASS", "FAIL", "N/A", "UNCONFIGURED"}:
            errors.append(_issue("EVIDENCE_RESULT", "invalid gate result", location))
            continue
        command = gate_record.get("command")
        exit_code = gate_record.get("exit_code")
        detail = gate_record.get("detail")
        log = gate_record.get("log")
        if result == "PASS":
            if not isinstance(command, str) or not command:
                errors.append(_issue("EVIDENCE_COMMAND", "PASS requires a command", location))
            if exit_code != 0:
                errors.append(_issue("EVIDENCE_EXIT", "PASS requires exit_code 0", location))
            _validate_evidence_log(log, location, errors, root)
        elif result == "FAIL":
            if not isinstance(command, str) or not command:
                errors.append(_issue("EVIDENCE_COMMAND", "FAIL requires a command", location))
            if not isinstance(exit_code, int) or exit_code == 0:
                errors.append(_issue("EVIDENCE_EXIT", "FAIL requires non-zero exit_code", location))
            _validate_evidence_log(log, location, errors, root)
        else:
            if not isinstance(detail, str) or not detail:
                errors.append(_issue("EVIDENCE_DETAIL", f"{result} requires detail", location))

    if risk in RISK_GATES:
        for gate in sorted(RISK_GATES[risk] - seen_gates):
            errors.append(
                _issue("MISSING_RISK_GATE", f"risk '{risk}' evidence is missing gate '{gate}'")
            )
        for gate in sorted(RISK_GATES[risk] & seen_gates):
            if gate_results.get(gate) in {"FAIL", "UNCONFIGURED"}:
                errors.append(
                    _issue(
                        "FAILING_RISK_GATE",
                        f"required risk gate '{gate}' is {gate_results.get(gate)}",
                    )
                )
    return errors


def _validate_evidence_log(
    log: Any,
    location: str,
    errors: list[dict[str, str]],
    root: Path | None,
) -> None:
    if not isinstance(log, dict):
        errors.append(_issue("EVIDENCE_LOG", "PASS/FAIL requires a hashed log record", location))
        return
    raw_path = log.get("path")
    digest = log.get("sha256")
    if not _nonempty_string(raw_path, f"{location}.log.path", errors):
        return
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append(_issue("EVIDENCE_LOG", "invalid log SHA-256", location))
        return
    if root is None:
        return
    resolved = _repo_relative_path(root, raw_path, f"{location}.log.path", errors)
    if resolved is None:
        return
    if not resolved.is_file():
        errors.append(_issue("EVIDENCE_LOG", f"log file is missing: {raw_path}", location))
        return
    if sha256_file(resolved) != digest:
        errors.append(_issue("EVIDENCE_LOG", f"log hash mismatch: {raw_path}", location))


def evaluate_readiness(
    validation: dict[str, Any],
    evidence: dict[str, Any],
    *,
    check_revision: bool = True,
    trace_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    root = Path(validation["root"])
    errors.extend(validate_evidence_record(evidence, root))
    warnings = list(validation.get("warnings", []))
    blockers: list[dict[str, str]] = []
    action_required: list[dict[str, str]] = []

    evidence_revision = evidence.get("revision", {}) if isinstance(evidence, dict) else {}
    revision_current = False
    if check_revision:
        try:
            current = repository_revision(root)
            revision_current = (
                evidence_revision.get("commit") == current["commit"]
                and evidence_revision.get("working_tree_fingerprint")
                == current["working_tree_fingerprint"]
            )
        except (OSError, subprocess.CalledProcessError, ValueError) as exc:
            blockers.append(_issue("REVISION_CHECK_FAILED", str(exc)))
        if not revision_current:
            blockers.append(
                _issue(
                    "STALE_EVIDENCE",
                    "evidence does not match the current commit and working-tree fingerprint",
                )
            )
    else:
        revision_current = True

    gate_records = {}
    if isinstance(evidence, dict) and isinstance(evidence.get("gates"), list):
        gate_records = {
            item.get("gate"): item
            for item in evidence["gates"]
            if isinstance(item, dict) and isinstance(item.get("gate"), str)
        }
    else:
        blockers.append(_issue("EVIDENCE_FORMAT", "evidence.gates must be an array"))

    human_checks = validation.get("human_checks", {}).get("checks", [])
    checks_by_id = {
        item.get("id"): item
        for item in human_checks
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    claim_results = []
    manifest_path = root / validation["manifest"]
    manifest_dir = manifest_path.parent

    trace_expectation = validation.get("data", {}).get("agent_trace_expectation")
    trace_status = "N/A"
    if isinstance(trace_expectation, dict) and trace_expectation.get("required"):
        if not isinstance(trace_summary, dict):
            blockers.append(
                _issue(
                    "AGENT_TRACE_MISSING",
                    "the manifest requires an agent trace summary for this release",
                )
            )
            trace_status = "UNVERIFIED"
        elif trace_summary.get("errors"):
            blockers.append(
                _issue("AGENT_TRACE_INVALID", "the supplied agent trace summary contains errors")
            )
            trace_status = "UNVERIFIED"
        else:
            action_counts = trace_summary.get("action_counts", {})
            missing_events = [
                event_type
                for event_type in trace_expectation.get("event_types", [])
                if not isinstance(action_counts, dict) or action_counts.get(event_type, 0) < 1
            ]
            if missing_events:
                blockers.append(
                    _issue(
                        "AGENT_TRACE_COVERAGE",
                        f"required event types are absent: {', '.join(missing_events)}",
                    )
                )
                trace_status = "PARTIAL"
            else:
                trace_status = str(trace_summary.get("coverage", "declared-events-only"))

    declared_risk = validation.get("data", {}).get("change", {}).get("risk")
    evidence_risk = evidence.get("run", {}).get("risk") if isinstance(evidence, dict) else None
    risk_rank = {"green": 0, "yellow": 1, "red": 2}
    if evidence_risk not in risk_rank:
        blockers.append(_issue("EVIDENCE_RISK", "evidence run risk is missing or invalid"))
    elif declared_risk in risk_rank and risk_rank[evidence_risk] < risk_rank[declared_risk]:
        blockers.append(
            _issue(
                "RISK_UNDERSHOOT",
                f"evidence risk '{evidence_risk}' is below manifest risk '{declared_risk}'",
            )
        )

    for claim in validation.get("data", {}).get("claims", []):
        claim_id = claim.get("id")
        machine = "N/A"
        ai_review = "N/A"
        human = "N/A"
        claim_blockers: list[dict[str, str]] = []
        claim_actions: list[dict[str, str]] = []
        required_gate_states = []
        required_review_states = []

        for requirement in claim.get("evidence_requirements", []):
            if not requirement.get("required"):
                continue
            if requirement.get("kind") == "gate":
                gate = requirement.get("gate")
                record = gate_records.get(gate)
                result = record.get("result") if record else "MISSING"
                required_gate_states.append(result)
                if result != "PASS":
                    claim_blockers.append(
                        _issue(
                            "REQUIRED_GATE_NOT_PASSING",
                            f"{claim_id} requires gate '{gate}', current result: {result}",
                            requirement.get("id", ""),
                        )
                    )
            elif requirement.get("kind") == "ai-review":
                artifact = requirement.get("artifact")
                artifact_path = (root / artifact).resolve() if artifact else manifest_dir
                present = artifact_path.is_file() and artifact_path.stat().st_size > 0
                required_review_states.append("PRESENT" if present else "MISSING")
                if not present:
                    claim_blockers.append(
                        _issue(
                            "REQUIRED_AI_REVIEW_MISSING",
                            f"{claim_id} requires AI review artifact '{artifact}'",
                            requirement.get("id", ""),
                        )
                    )

        if required_gate_states:
            if all(state == "PASS" for state in required_gate_states) and revision_current:
                machine = "MACHINE_VERIFIED"
            elif any(state == "PASS" for state in required_gate_states):
                machine = "PARTIAL"
            else:
                machine = "UNVERIFIED"
        if required_review_states:
            ai_review = (
                "AI_REVIEWED"
                if all(state == "PRESENT" for state in required_review_states)
                else "UNVERIFIED"
            )

        linked_checks = [
            checks_by_id[check_id]
            for check_id in claim.get("human_check_ids", [])
            if check_id in checks_by_id
        ]
        if linked_checks:
            if any(check.get("status") == "failed" for check in linked_checks):
                human = "FAILED"
            elif all(check.get("status") == "passed" for check in linked_checks):
                human = "HUMAN_VERIFIED"
            elif any(
                check.get("level") == "must" and check.get("status") != "passed"
                for check in linked_checks
            ):
                human = "HUMAN_REQUIRED"
            else:
                human = "HUMAN_REQUIRED"

            for check in linked_checks:
                status = check.get("status")
                level = check.get("level")
                if level == "must" and status != "passed":
                    item = _issue(
                        "MUST_HUMAN_CHECK_INCOMPLETE",
                        f"{claim_id} requires Human Check '{check.get('id')}', status: {status}",
                        check.get("id", ""),
                    )
                    if status == "pending":
                        claim_actions.append(item)
                    else:
                        claim_blockers.append(item)
                elif level in {"should", "optional"} and status != "passed":
                    warnings.append(
                        _issue(
                            "HUMAN_CHECK_RECOMMENDED",
                            f"{level.upper()} Human Check '{check.get('id')}' is {status}",
                            claim_id,
                        )
                    )

        decisive = machine == "MACHINE_VERIFIED" or any(
            check.get("status") == "passed" for check in linked_checks
        )
        if claim.get("criticality") == "must" and not decisive:
            if not claim_actions:
                claim_blockers.append(
                    _issue(
                        "NO_DECISIVE_EVIDENCE",
                        f"{claim_id} has neither current machine proof nor a passed Human Check",
                        claim_id,
                    )
                )
        if claim.get("criticality") == "should" and (claim_blockers or claim_actions):
            warnings.extend(claim_blockers + claim_actions)
            claim_blockers = []
            claim_actions = []

        blockers.extend(claim_blockers)
        action_required.extend(claim_actions)
        claim_results.append(
            {
                "id": claim_id,
                "criticality": claim.get("criticality"),
                "machine": machine,
                "ai_review": ai_review,
                "human": human,
                "ready": not claim_blockers and not claim_actions,
                "blockers": claim_blockers,
                "actions": claim_actions,
                "residual_uncertainty": claim.get("residual_uncertainty"),
            }
        )

    if errors or blockers:
        readiness = "BLOCKED"
    elif action_required:
        readiness = "ACTION_REQUIRED"
    else:
        readiness = "READY"
    return {
        "change_id": validation.get("change_id"),
        "manifest": validation.get("manifest"),
        "structurally_valid": not errors,
        "revision_current": revision_current,
        "agent_trace": trace_status,
        "readiness": readiness,
        "claims": claim_results,
        "blockers": errors + blockers,
        "human_actions": action_required,
        "warnings": warnings,
    }


def dump_json(data: Any, path: Path | None = None) -> str:
    rendered = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    return rendered
