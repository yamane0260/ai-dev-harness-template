from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

RISK_ORDER = {"GREEN": 0, "YELLOW": 1, "RED": 2}
LENSES = ("correctness", "boundary", "failure", "work_fit", "simplicity")
DOMAINS = ("security", "ux", "data", "reliability", "architecture")

RED_HINTS = {
    "auth", "authentication", "authorization", "permission", "permissions",
    "secret", "secrets", "credential", "credentials", "payment", "payments",
    "production", "prod", "destructive", "delete-data", "sensitive-data",
    "security-control", "harness-policy", "irreversible"
}
YELLOW_HINTS = {
    "api", "schema", "migration", "dependency", "user-facing", "ui",
    "external-integration", "webhook", "persistence", "database", "db",
    "workflow", "data-transform"
}

RED_PATHS = (
    r"(^|/)(auth|authentication|authorization|permissions?)(/|$)",
    r"(^|/)(secrets?|credentials?)(/|$)",
    r"(^|/)(payments?|billing)(/|$)",
    r"(^|/)(terraform|infra|infrastructure|deploy|deployment|production)(/|$)",
    r"(^|/)ai/v5/(kernel|schemas)(/|\.|$)",
    r"(^|/)scripts/ai/(v5\.py|lib/v5_core\.py)$",
)
YELLOW_PATHS = (
    r"(^|/)(api|routes?|controllers?)(/|$)",
    r"(^|/)(migrations?|schema|models?)(/|$)",
    r"(^|/)(package\.json|pyproject\.toml|requirements[^/]*\.txt|go\.mod|Cargo\.toml)$",
    r"(^|/)(ui|components?|views?|pages?|templates?)(/|$)",
    r"(^|/)(integrations?|webhooks?)(/|$)",
)
DOMAIN_PATHS = {
    "security": (r"(^|/)(auth|authentication|authorization|permissions?|security|secrets?|credentials?)(/|$)", r"(^|/)(middleware|session|tokens?)(/|$)"),
    "ux": (r"(^|/)(ui|components?|views?|pages?|templates?|forms?|navigation)(/|$)", r"\.(css|scss|sass|less|tsx|jsx|vue|svelte)$"),
    "data": (r"(^|/)(migrations?|schema|models?|database|db|repositories?)(/|$)", r"\.sql$"),
    "reliability": (r"(^|/)(jobs?|queues?|workers?|integrations?|webhooks?|deploy|deployment|infra|infrastructure)(/|$)", r"(^|/)(retry|retries|circuit|timeout)(/|$)"),
    "architecture": (r"(^|/)(architecture|core|kernel|platform|shared|common)(/|$)", r"(^|/)(package\.json|pyproject\.toml|requirements[^/]*\.txt|go\.mod|Cargo\.toml)$"),
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def dump_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _string(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _strings(value, name, allow_empty=True):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f"{name} must be a list of non-empty strings")
    if not allow_empty and not value:
        raise ValueError(f"{name} must not be empty")
    return [x.strip() for x in value]


def _dedupe(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def validate_task(task):
    allowed = {"version", "id", "goal", "acceptance", "constraints", "scope", "mustNot", "riskHints", "domainHints", "verification", "metadata"}
    unknown = sorted(set(task) - allowed)
    if unknown:
        raise ValueError("unknown task fields: " + ", ".join(unknown))
    if task.get("version", 1) != 1:
        raise ValueError("task.version must be 1")
    result = {
        "version": 1,
        "id": _string(task.get("id", "task"), "task.id"),
        "goal": _string(task.get("goal"), "task.goal"),
        "acceptance": _strings(task.get("acceptance"), "task.acceptance", False),
        "constraints": _strings(task.get("constraints", []), "task.constraints"),
        "scope": _strings(task.get("scope", []), "task.scope"),
        "mustNot": _strings(task.get("mustNot", []), "task.mustNot"),
        "riskHints": _strings(task.get("riskHints", []), "task.riskHints"),
        "domainHints": _strings(task.get("domainHints", []), "task.domainHints"),
        "verification": _strings(task.get("verification", []), "task.verification"),
        "metadata": task.get("metadata", {})
    }
    if not isinstance(result["metadata"], dict):
        raise ValueError("task.metadata must be an object")
    bad = sorted(set(result["domainHints"]) - set(DOMAINS))
    if bad:
        raise ValueError("unsupported domainHints: " + ", ".join(bad))
    return result


def _matches(path, patterns):
    path = path.replace("\\", "/")
    return any(re.search(pattern, path, re.I) for pattern in patterns)


def risk_floor(task, paths):
    task = validate_task(task)
    level, reasons = "GREEN", []
    for hint in task["riskHints"]:
        key = hint.lower()
        if key in RED_HINTS:
            level = "RED"
            reasons.append(f"risk hint '{hint}' -> RED")
        elif key in YELLOW_HINTS and level != "RED":
            level = "YELLOW"
            reasons.append(f"risk hint '{hint}' -> YELLOW")
    for path in paths:
        if _matches(path, RED_PATHS):
            level = "RED"
            reasons.append(f"high-consequence path: {path}")
        elif _matches(path, YELLOW_PATHS) and level == "GREEN":
            level = "YELLOW"
            reasons.append(f"material path: {path}")
    return level, _dedupe(reasons or ["no deterministic YELLOW/RED trigger found"])


def detect_domains(task, paths):
    task = validate_task(task)
    domains = list(task["domainHints"])
    hints = {x.lower() for x in task["riskHints"]}
    if hints & {"auth", "authentication", "authorization", "permission", "permissions", "secret", "secrets", "credential", "credentials", "sensitive-data", "security-control"}:
        domains.append("security")
    if hints & {"ui", "user-facing", "workflow"}:
        domains.append("ux")
    if hints & {"schema", "migration", "persistence", "database", "db", "data-transform", "destructive", "delete-data"}:
        domains.append("data")
    if hints & {"external-integration", "webhook", "production", "prod"}:
        domains.append("reliability")
    if hints & {"dependency", "harness-policy"}:
        domains.append("architecture")
    for path in paths:
        for domain, patterns in DOMAIN_PATHS.items():
            if _matches(path, patterns):
                domains.append(domain)
    return _dedupe(domains)


def validate_config(config):
    if config.get("version", 1) != 1:
        raise ValueError("gate config version must be 1")
    for field in ("gates", "riskGates", "domainGates"):
        if not isinstance(config.get(field, {}), dict):
            raise ValueError(f"{field} must be an object")
    for name, gate in config.get("gates", {}).items():
        if not isinstance(gate, dict):
            raise ValueError(f"gate {name} must be an object")
        _string(gate.get("command"), f"gate {name}.command")
        timeout = gate.get("timeoutSeconds", 300)
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError(f"gate {name}.timeoutSeconds must be positive")
    return config


def required_gates(task, risk, domains, config):
    task, config = validate_task(task), validate_config(config)
    names = list(config.get("riskGates", {}).get(risk, []))
    for domain in domains:
        names += config.get("domainGates", {}).get(domain, [])
    names += task["verification"]
    return _dedupe(names)


def git_changed_paths(repo):
    paths = []
    for command in (["git", "diff", "--name-only"], ["git", "diff", "--cached", "--name-only"]):
        proc = subprocess.run(command, cwd=repo, capture_output=True, text=True, check=False)
        if proc.returncode == 0:
            paths += [x.strip() for x in proc.stdout.splitlines() if x.strip()]
    return _dedupe(paths)


def select_context(task, domains, paths, repo):
    refs = []
    for filename in ("AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"):
        if (repo / filename).exists():
            refs.append(filename)
    refs += task["scope"] + list(paths)
    refs += [f"ai/v5/capsules/{domain}.md" for domain in domains]
    return _dedupe(refs)


def preflight(task, paths, config, repo):
    task = validate_task(task)
    paths = _dedupe(list(paths) + task["scope"])
    risk, reasons = risk_floor(task, paths)
    domains = detect_domains(task, paths)
    return {
        "version": 1,
        "taskId": task["id"],
        "riskFloor": risk,
        "riskReasons": reasons,
        "domains": domains,
        "contextRefs": select_context(task, domains, paths, Path(repo)),
        "perspectiveLenses": list(LENSES),
        "requiredGates": required_gates(task, risk, domains, config)
    }


def validate_scan(scan):
    if scan.get("version", 1) != 1 or not isinstance(scan.get("lenses"), dict):
        raise ValueError("invalid perspective scan")
    missing = [x for x in LENSES if x not in scan["lenses"]]
    if missing:
        raise ValueError("scan is missing lenses: " + ", ".join(missing))
    lenses = {}
    for name in LENSES:
        item = scan["lenses"][name]
        if not isinstance(item, dict) or item.get("status") not in {"clear", "finding", "unknown"} or not isinstance(item.get("note", ""), str):
            raise ValueError(f"invalid scan lens: {name}")
        lenses[name] = {"status": item["status"], "note": item.get("note", "").strip()}
    escalations = scan.get("escalations", [])
    if not isinstance(escalations, list):
        raise ValueError("scan.escalations must be a list")
    normalized = []
    for item in escalations:
        if not isinstance(item, dict) or item.get("domain") not in DOMAINS:
            raise ValueError("invalid scan escalation")
        normalized.append({"domain": item["domain"], "reason": _string(item.get("reason"), "escalation reason")})
    return {
        "version": 1,
        "lenses": lenses,
        "escalations": normalized,
        "blockingUnknowns": _strings(scan.get("blockingUnknowns", []), "scan.blockingUnknowns")
    }


def repository_fingerprint(repo):
    def run(*args):
        return subprocess.run(args, cwd=repo, capture_output=True, text=True, check=False)
    head, status = run("git", "rev-parse", "HEAD"), run("git", "status", "--porcelain=v1", "--untracked-files=all")
    if head.returncode or status.returncode:
        return {"head": None, "dirty": None, "workingTreeHash": None}
    raw = status.stdout.strip()
    return {"head": head.stdout.strip(), "dirty": bool(raw), "workingTreeHash": hashlib.sha256(raw.encode()).hexdigest()}


def run_verification(required, config, repo):
    config = validate_config(config)
    results = []
    for name in required:
        gate = config.get("gates", {}).get(name)
        if not gate:
            results.append({"name": name, "status": "unconfigured", "exitCode": None, "outputHash": None})
            continue
        try:
            proc = subprocess.run(gate["command"], cwd=repo, shell=True, executable="/bin/sh", capture_output=True, text=True, timeout=gate.get("timeoutSeconds", 300), check=False)
            output = (proc.stdout or "") + (proc.stderr or "")
            item = {"name": name, "status": "passed" if proc.returncode == 0 else "failed", "exitCode": proc.returncode, "outputHash": hashlib.sha256(output.encode(errors="replace")).hexdigest()}
            if proc.returncode:
                item["failureTail"] = output[-600:].strip()
            results.append(item)
        except subprocess.TimeoutExpired:
            results.append({"name": name, "status": "failed", "exitCode": None, "outputHash": None, "failureTail": "timed out"})
    return {"version": 1, "repository": repository_fingerprint(Path(repo)), "checks": results, "passed": all(x["status"] == "passed" for x in results)}


def validate_result(result):
    if result.get("version", 1) != 1 or result.get("status") not in {"implemented", "blocked", "needs_supervisor"}:
        raise ValueError("invalid result envelope")
    return {
        "version": 1,
        "taskId": _string(result.get("taskId"), "result.taskId"),
        "status": result["status"],
        "changedPaths": _strings(result.get("changedPaths", []), "result.changedPaths"),
        "decisions": _strings(result.get("decisions", []), "result.decisions"),
        "residualRisks": _strings(result.get("residualRisks", []), "result.residualRisks"),
        "assumptions": _strings(result.get("assumptions", []), "result.assumptions"),
        "escalation": result.get("escalation")
    }


def guard_result(task, pf, scan, verification, result, repo):
    task, scan, result = validate_task(task), validate_scan(scan), validate_result(result)
    reasons = []
    if result["taskId"] != task["id"] or pf.get("taskId") != task["id"]:
        reasons.append("task identity mismatch")
    checks = {x.get("name"): x for x in verification.get("checks", []) if isinstance(x, dict)}
    for gate in pf.get("requiredGates", []):
        if checks.get(gate, {}).get("status") != "passed":
            reasons.append(f"required gate not passed: {gate}")
    if verification.get("repository") != repository_fingerprint(Path(repo)):
        reasons.append("verification evidence is stale for the current repository state")
    if scan["blockingUnknowns"] or any(x["status"] == "unknown" for x in scan["lenses"].values()):
        reasons.append("perspective scan contains unresolved unknowns")
    if result["status"] == "implemented" and (result["escalation"] is not None or scan["escalations"]):
        reasons.append("implemented result contains unresolved escalation")
    return {
        "ok": not reasons,
        "status": "HANDOFF_READY" if not reasons else "BLOCKED",
        "reasons": reasons,
        "scope": "worker implementation handoff only; not release readiness"
    }
