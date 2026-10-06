#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from lib.v5_core import (
    dump_json,
    git_changed_paths,
    guard_result,
    load_json,
    preflight,
    run_verification,
    validate_scan,
    validate_task,
)


def _repo(value: str) -> Path:
    path = Path(value).resolve()
    if not path.exists():
        raise SystemExit(f"repository path does not exist: {path}")
    return path


def cmd_validate_task(args):
    print(dump_json(validate_task(load_json(args.task))))
    return 0


def cmd_preflight(args):
    repo = _repo(args.repo)
    task = load_json(args.task)
    config = load_json(args.config)
    changed = args.changed or git_changed_paths(repo)
    print(dump_json(preflight(task, changed, config, repo)))
    return 0


def cmd_validate_scan(args):
    print(dump_json(validate_scan(load_json(args.scan))))
    return 0


def cmd_verify(args):
    repo = _repo(args.repo)
    task = load_json(args.task)
    scan = validate_scan(load_json(args.scan))
    config = load_json(args.config)
    changed = args.changed or git_changed_paths(repo)
    pf = preflight(task, changed, config, repo)
    if scan["blockingUnknowns"] or any(item["status"] == "unknown" for item in scan["lenses"].values()):
        print(dump_json({
            "version": 1,
            "passed": False,
            "repository": {},
            "checks": [],
            "blockedByScan": True
        }))
        return 2
    evidence = run_verification(pf["requiredGates"], config, repo)
    print(dump_json(evidence))
    return 0 if evidence["passed"] else 1


def cmd_guard_result(args):
    repo = _repo(args.repo)
    verdict = guard_result(
        load_json(args.task),
        load_json(args.preflight),
        load_json(args.scan),
        load_json(args.verification),
        load_json(args.result),
        repo,
    )
    print(dump_json(verdict))
    return 0 if verdict["ok"] else 1


def parser():
    p = argparse.ArgumentParser(description="AI Development Harness V5 Worker Core")
    sub = p.add_subparsers(dest="command", required=True)

    task = sub.add_parser("validate-task")
    task.add_argument("--task", required=True)
    task.set_defaults(func=cmd_validate_task)

    pf = sub.add_parser("preflight")
    pf.add_argument("--task", required=True)
    pf.add_argument("--repo", default=".")
    pf.add_argument("--config", default="ai/v5/project/commands.json")
    pf.add_argument("--changed", action="append", default=[])
    pf.set_defaults(func=cmd_preflight)

    scan = sub.add_parser("validate-scan")
    scan.add_argument("--scan", required=True)
    scan.set_defaults(func=cmd_validate_scan)

    verify = sub.add_parser("verify")
    verify.add_argument("--task", required=True)
    verify.add_argument("--scan", required=True)
    verify.add_argument("--repo", default=".")
    verify.add_argument("--config", default="ai/v5/project/commands.json")
    verify.add_argument("--changed", action="append", default=[])
    verify.set_defaults(func=cmd_verify)

    guard = sub.add_parser("guard-result")
    guard.add_argument("--task", required=True)
    guard.add_argument("--preflight", required=True)
    guard.add_argument("--scan", required=True)
    guard.add_argument("--verification", required=True)
    guard.add_argument("--result", required=True)
    guard.add_argument("--repo", default=".")
    guard.set_defaults(func=cmd_guard_result)
    return p


def main():
    try:
        args = parser().parse_args()
        return args.func(args)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"V5 contract error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
