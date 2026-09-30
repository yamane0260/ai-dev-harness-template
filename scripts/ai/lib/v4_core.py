"""V4 composition, event, and dashboard read-model helpers.

Standard-library only. The runtime emits bounded structured state; it never invokes an LLM
for dashboard explanations.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
KERNEL_VERSION = "4.0.0"
COMPILER_VERSION = "1.0.0"
RISK_ORDER = {"GREEN": 0, "YELLOW": 1, "RED": 2}
SENSITIVE_KEY = re.compile(r"(?i)(password|secret|token|api.?key|authorization|cookie|credential)")
SENSITIVE_VALUE = [
    re.compile(r"(?i)bearer\\s+[A-Za-z0-9._-]{8,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"://[^/\\s:@]+:[^/\\s@]+@"),
]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").is_file():
            return candidate
    raise RuntimeError("repository root not found")

def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data

def dump_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)

def git_value(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True, check=True
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""

def project_config(root: Path) -> dict[str, Any]:
    path = root / ".harness" / "dashboard.json"
    if path.is_file():
        data = load_json(path)
        return data
    name = root.name
    project_id = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-") or "project"
    return {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id[:63],
        "name": name,
        "locale": "ja",
        "profile": "balanced",
        "dashboard": {
            "show_project_specific": True,
            "technical_details_default_open": False,
        },
    }

def initialize_project(root: Path, *, force: bool = False) -> Path:
    target = root / ".harness" / "dashboard.json"
    if target.exists() and not force:
        return target
    config = project_config(root)
    dump_json(config, target)
    return target

def load_profile(root: Path, profile_id: str) -> dict[str, Any]:
    path = root / "ai" / "v4" / "profiles" / f"{profile_id}.json"
    if not path.is_file():
        raise ValueError(f"unknown profile: {profile_id}")
    return load_json(path)

def load_registry(root: Path) -> dict[str, Any]:
    return load_json(root / "ai" / "v4" / "provider-registry.json")

def provider_map(root: Path) -> dict[str, dict[str, Any]]:
    registry = load_registry(root)
    result: dict[str, dict[str, Any]] = {}
    for item in registry.get("providers", []):
        capability = item.get("implements", {}).get("capability")
        if capability and capability not in result:
            result[capability] = item
    return result

def max_risk(a: str, b: str) -> str:
    return a if RISK_ORDER[a] >= RISK_ORDER[b] else b

def detect_risk(root: Path, base: str | None = None) -> tuple[str, list[str]]:
    command = [str(root / "scripts" / "ai" / "classify-risk")]
    if base:
        command += ["--base", base]
    try:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise RuntimeError(f"risk classifier failed: {detail.strip()}") from exc
    level = "GREEN"
    reasons: list[str] = []
    for line in result.stdout.splitlines():
        if line.startswith("risk="):
            level = line.split("=", 1)[1].strip().upper()
        elif line.startswith("reason="):
            reasons.append(line.split("=", 1)[1].strip())
    if level not in RISK_ORDER:
        raise ValueError(f"invalid risk classifier output: {level}")
    return level, reasons

def _when_applies(when: str, risk: str, release: bool, quality: set[str], claims: bool) -> bool:
    if when == "always":
        return True
    if when == "selected":
        return False
    if when == "release":
        return release
    if when == "risk-yellow-or-higher":
        return RISK_ORDER[risk] >= RISK_ORDER["YELLOW"]
    if when == "risk-red":
        return risk == "RED"
    if when == "quality-impact":
        return bool(quality)
    if when == "claim-required":
        return claims
    return False

def compile_plan(
    root: Path,
    *,
    task_kind: str = "implement",
    profile_id: str | None = None,
    risk: str | None = None,
    risk_reasons: list[str] | None = None,
    quality_impacts: list[str] | None = None,
    knowledge_impact: str = "LOW",
    release: bool = False,
    claims_present: bool = False,
    host: str = "generic",
) -> dict[str, Any]:
    config = project_config(root)
    profile_id = profile_id or str(config.get("profile", "balanced"))
    profile = load_profile(root, profile_id)
    providers = provider_map(root)
    quality = {item.strip().lower() for item in (quality_impacts or []) if item.strip()}
    knowledge = knowledge_impact.upper()
    if knowledge not in {"NONE", "LOW", "MATERIAL", "CRITICAL"}:
        raise ValueError("knowledge impact must be NONE, LOW, MATERIAL, or CRITICAL")

    if risk is None:
        risk, detected = detect_risk(root)
        risk_reasons = risk_reasons or detected
    risk = risk.upper()
    if risk not in RISK_ORDER:
        raise ValueError("risk must be GREEN, YELLOW, or RED")
    minimum = profile.get("constraints", {}).get("risk_policy", {}).get("minimum")
    if minimum:
        risk = max_risk(risk, minimum)

    selected: dict[str, dict[str, Any]] = {}
    reasons: dict[str, str] = {}

    def require(capability: str, reason: str, required: bool = True) -> None:
        if capability in selected:
            if required:
                selected[capability]["required"] = True
            return
        provider = providers.get(capability)
        if not provider:
            selected[capability] = {
                "capability": capability, "contract_version": 1, "provider": "",
                "provider_version": "", "required": required, "reason": reason,
                "depends_on": [], "context_budget_tokens": 0,
            }
            reasons[capability] = "NO_PROVIDER"
            return
        selected[capability] = {
            "capability": capability,
            "contract_version": int(provider["implements"]["contract_version"]),
            "provider": provider["id"],
            "provider_version": provider["version"],
            "required": required,
            "reason": reason,
            "depends_on": [r["capability"] for r in provider.get("requires", []) if r.get("required", True)],
            "context_budget_tokens": int(provider.get("context", {}).get("parent_budget_tokens", 0)),
        }
        reasons[capability] = reason

    require("profile.resolve", "PROFILE_SELECTED")
    require("risk.floor", "CAPABILITY_SELECTED")

    if task_kind == "implement":
        require("project.explore", "CAPABILITY_SELECTED")
        require("change.implement", "CAPABILITY_SELECTED")
        require("verification.run", "AUTOMATED_TEST_AVAILABLE")
    elif task_kind == "debug":
        require("project.explore", "CAPABILITY_SELECTED")
        require("debug.diagnose", "CAPABILITY_SELECTED")
        require("verification.run", "AUTOMATED_TEST_AVAILABLE")
    elif task_kind == "explain":
        require("knowledge.explain-system", "CAPABILITY_SELECTED")
    else:
        raise ValueError("task kind must be implement, debug, or explain")

    if quality:
        require("quality.preflight", "CAPABILITY_SELECTED")
    if "security" in quality:
        require("review.security", "CAPABILITY_SELECTED")
    if "ux" in quality or "accessibility" in quality:
        require("review.ux", "CAPABILITY_SELECTED")
    if "design" in quality:
        require("review.design", "CAPABILITY_SELECTED")
    if "maintainability" in quality or "architecture" in quality:
        require("review.code", "CAPABILITY_SELECTED")

    for constraint in profile.get("constraints", {}).get("required_capabilities", []):
        if _when_applies(constraint["when"], risk, release, quality, claims_present):
            require(constraint["capability"], "RISK_LEVEL_HIGH" if "risk-" in constraint["when"] else "CAPABILITY_SELECTED")

    if task_kind == "implement" and RISK_ORDER[risk] >= RISK_ORDER["YELLOW"]:
        require("assurance.evaluate", "RISK_LEVEL_HIGH")

    knowledge_policy = profile.get("understanding", {}).get("knowledge_impact_policy", "durable-on-material")
    if task_kind == "implement" and (
        knowledge in {"MATERIAL", "CRITICAL"}
        or knowledge_policy == "durable-always"
        or profile.get("understanding", {}).get("requirement") == "EXPLAINABLE"
    ):
        require("knowledge.explain-change", "CAPABILITY_SELECTED")
    review_threshold = profile.get("understanding", {}).get("fresh_legibility_review", "never")
    need_legibility = (
        review_threshold == "always"
        or (review_threshold == "material" and knowledge in {"MATERIAL", "CRITICAL"})
        or (review_threshold == "critical" and knowledge == "CRITICAL")
    )
    if need_legibility:
        require("knowledge.legibility", "CAPABILITY_SELECTED")
    if release:
        require("release.evaluate", "CAPABILITY_SELECTED")

    invalid = [f"no provider for required capability {c}" for c, item in selected.items() if item["required"] and not item["provider"]]
    ordered = list(selected.values())
    hash_inputs = [
        f"kernel:{KERNEL_VERSION}", f"compiler:{COMPILER_VERSION}", f"profile:{profile_id}",
        f"risk:{risk}", f"host:{host}",
        *[f"{item['capability']}:{item['provider']}:{item['provider_version']}" for item in ordered],
    ]
    composition_hash = hashlib.sha256("\n".join(hash_inputs).encode("utf-8")).hexdigest()
    plan = {
        "schema_version": SCHEMA_VERSION,
        "plan_id": f"plan_{uuid.uuid4().hex}",
        "profile_id": profile_id,
        "risk": {"floor": risk, "effective": risk, "reasons": risk_reasons or []},
        "host": {"id": host, "coverage": "PARTIAL", "missing_capabilities": []},
        "selected": ordered,
        "skipped": [],
        "context_budget": {
            "parent_tokens": int(profile["context_budget"]["parent_tokens"]),
            "plugin_instruction_tokens": int(profile["context_budget"]["plugin_instruction_tokens"]),
            "tool_result_tokens": int(profile["context_budget"]["tool_result_tokens"]),
            "child_context_isolation": "preferred" if profile["context_budget"].get("child_context_isolation_preferred") else "unavailable",
            "compaction_allowed": bool(profile["context_budget"].get("compaction_allowed", True)),
        },
        "composition": {
            "kernel_version": KERNEL_VERSION,
            "compiler_version": COMPILER_VERSION,
            "composition_hash": composition_hash,
            "composition_hash_inputs": hash_inputs,
        },
        "invalid_reasons": invalid,
        "dashboard_context": {
            "task_kind": task_kind,
            "quality_impacts": sorted(quality),
            "knowledge_impact": knowledge,
            "release": release,
        },
    }
    return plan

def _safe_value(value: Any, path: str = "details") -> Any:
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if SENSITIVE_KEY.search(str(key)):
                raise ValueError(f"sensitive event key rejected: {path}.{key}")
            result[str(key)] = _safe_value(item, f"{path}.{key}")
        return result
    if isinstance(value, list):
        return [_safe_value(item, path) for item in value]
    if isinstance(value, str):
        if len(value) > 2048:
            raise ValueError(f"event value too large at {path}")
        if any(pattern.search(value) for pattern in SENSITIVE_VALUE):
            raise ValueError(f"sensitive event value rejected at {path}")
        return value
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise ValueError(f"unsupported event value at {path}")

def run_dir(root: Path, run_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9._-]{3,128}", run_id):
        raise ValueError("invalid run id")
    return root / ".ai-artifacts" / "runs" / run_id

def emit_event(
    root: Path, *, run_id: str, event_type: str, status: str,
    component: str | None = None, reason_code: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = project_config(root)
    safe_details = _safe_value(details or {})
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": f"evt_{uuid.uuid4().hex}",
        "timestamp": utc_now(),
        "project_id": config["project_id"],
        "run_id": run_id,
        "type": event_type,
        "component": component,
        "status": status,
        "reason_code": reason_code,
        "details": safe_details,
        "redaction": {"raw_prompt": False, "raw_completion": False, "secrets": False},
    }
    directory = run_dir(root, run_id)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "events.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    return event

def load_events(root: Path, run_id: str) -> list[dict[str, Any]]:
    path = run_dir(root, run_id) / "events.jsonl"
    if not path.is_file():
        return []
    result = []
    with path.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid event JSON at line {number}") from exc
            if isinstance(item, dict):
                result.append(item)
    return result

def latest_run_id(root: Path) -> str | None:
    base = root / ".ai-artifacts" / "runs"
    if not base.is_dir():
        return None
    candidates = [path for path in base.iterdir() if path.is_dir()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime).name

def save_plan(root: Path, run_id: str, plan: dict[str, Any]) -> Path:
    path = run_dir(root, run_id) / "plan.json"
    dump_json(plan, path)
    return path

def load_plan(root: Path, run_id: str) -> dict[str, Any] | None:
    path = run_dir(root, run_id) / "plan.json"
    return load_json(path) if path.is_file() else None

def _duration_ms(events: list[dict[str, Any]]) -> int | None:
    if len(events) < 2:
        return None
    try:
        start = datetime.fromisoformat(events[0]["timestamp"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(events[-1]["timestamp"].replace("Z", "+00:00"))
    except (KeyError, ValueError):
        return None
    return max(0, int((end - start).total_seconds() * 1000))

def build_read_model(root: Path, run_id: str | None = None) -> dict[str, Any]:
    config = project_config(root)
    self_description = load_json(root / "ai" / "v4" / "self-description.json")
    run_id = run_id or latest_run_id(root)
    events = load_events(root, run_id) if run_id else []
    plan = load_plan(root, run_id) if run_id else None
    last_status: dict[str, str] = {}
    human_checks: list[dict[str, Any]] = []
    changes: list[str] = []
    retry_count = fallback_count = compaction_count = 0
    anomalies: list[dict[str, str]] = []
    verification = {"state": "not-run", "summary": ""}

    for event in events:
        component = event.get("component")
        if component:
            last_status[component] = event.get("status", "unknown")
        etype = event.get("type", "")
        details = event.get("details", {})
        if etype == "human_check.required":
            human_checks.append({"summary": details.get("summary", "確認が必要です"), "status": event.get("status", "pending")})
        elif etype == "change.recorded":
            summary = details.get("summary")
            if summary:
                changes.append(str(summary))
        elif etype == "retry.performed":
            retry_count += 1
        elif etype == "fallback.performed":
            fallback_count += 1
            anomalies.append({"kind": "fallback", "summary": details.get("summary", "別の方法へ切り替えました")})
        elif etype == "context.compacted":
            compaction_count += 1
        elif etype == "verification.completed":
            verification = {"state": event.get("status", "unknown"), "summary": str(details.get("summary", ""))}
        elif etype.endswith(".failed") or event.get("status") in {"failure", "blocked"}:
            anomalies.append({"kind": "failure", "summary": str(details.get("summary", f"{etype} failed"))})

    active_components = [item["capability"] for item in (plan or {}).get("selected", [])]
    current = events[-1] if events else None
    work_state = "idle"
    if current:
        if current["status"] in {"failure", "blocked"}:
            work_state = "attention"
        elif current["type"] == "run.completed":
            work_state = "complete"
        else:
            work_state = "running"
    revision = git_value(root, "rev-parse", "--short", "HEAD") or "unknown"
    branch = git_value(root, "branch", "--show-current") or "detached"

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "project": {
            "id": config["project_id"], "name": config["name"], "locale": config.get("locale", "ja"),
            "profile": (plan or {}).get("profile_id", config.get("profile", "balanced")),
            "revision": revision, "branch": branch, "run_id": run_id,
        },
        "work": {
            "state": work_state,
            "current": {
                "component": current.get("component") if current else None,
                "summary": (current or {}).get("details", {}).get("summary", "作業履歴はまだありません") if current else "作業履歴はまだありません",
                "updated_at": current.get("timestamp") if current else None,
            },
            "attention": human_checks,
            "verification": verification,
            "recent_changes": changes[-8:],
        },
        "harness": {
            "kernel_version": KERNEL_VERSION,
            "compiler_version": COMPILER_VERSION,
            "architecture": self_description.get("architecture", {}),
            "components": self_description.get("components", {}),
            "reason_codes": self_description.get("reason_codes", {}),
            "active_components": active_components,
            "component_states": last_status,
            "selected": (plan or {}).get("selected", []),
            "risk": (plan or {}).get("risk"),
            "context_budget": (plan or {}).get("context_budget"),
        },
        "diagnosis": {
            "duration_ms": _duration_ms(events),
            "retry_count": retry_count,
            "fallback_count": fallback_count,
            "human_check_count": len(human_checks),
            "context_compaction_count": compaction_count,
            "event_count": len(events),
            "anomalies": anomalies[-20:],
        },
        "technical": {"events": events[-250:], "plan": plan},
    }

def completion_blockers(root: Path, run_id: str) -> list[str]:
    plan = load_plan(root, run_id)
    if not plan:
        return [f"no V4 plan found for {run_id}"]
    blockers = list(plan.get("invalid_reasons", []))
    model = build_read_model(root, run_id)

    verification_required = any(
        item.get("capability") == "verification.run" and item.get("required", True)
        for item in plan.get("selected", [])
    )
    if verification_required and model["work"]["verification"].get("state") != "success":
        blockers.append("required deterministic verification has not passed")

    for item in model["work"].get("attention", []):
        if item.get("status") not in {"success", "completed", "skipped"}:
            blockers.append(f"human check remains incomplete: {item.get('summary', 'unspecified check')}")

    return blockers

def write_read_model(root: Path, run_id: str | None = None) -> Path:
    model = build_read_model(root, run_id)
    path = root / ".ai-artifacts" / "dashboard" / "state.json"
    dump_json(model, path)
    summary = {
        "schema_version": SCHEMA_VERSION,
        "project_id": model["project"]["id"],
        "name": model["project"]["name"],
        "state": model["work"]["state"],
        "attention_required": bool(model["work"]["attention"]) or bool(model["diagnosis"]["anomalies"]),
        "last_activity": model["work"]["current"]["updated_at"],
    }
    dump_json(summary, root / ".ai-artifacts" / "dashboard" / "summary.json")
    return path
