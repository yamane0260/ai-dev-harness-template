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
    build_verifier_packet,
    contract_fingerprint,
    dump_json,
    git_changed_paths,
    guard_acceptance,
    guard_result,
    load_json,
    next_action,
    preflight,
    run_verification,
    validate_acceptance_verdict,
    validate_failure_classification,
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
            "contractHash": contract_fingerprint(task),
            "passed": False,
            "repository": {},
            "checks": [],
            "blockedByScan": True,
        }))
        return 2
    evidence = run_verification(pf["requiredGates"], config, repo, contract_fingerprint(task))
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


def cmd_verifier_packet(args):
    repo = _repo(args.repo)
    packet = build_verifier_packet(
        load_json(args.task),
        load_json(args.preflight),
        load_json(args.verification),
        repo,
    )
    print(dump_json(packet))
    return 0


def cmd_validate_verdict(args):
    print(dump_json(validate_acceptance_verdict(load_json(args.verdict))))
    return 0


def cmd_guard_acceptance(args):
    repo = _repo(args.repo)
    verdict = guard_acceptance(
        load_json(args.task),
        load_json(args.preflight),
        load_json(args.packet),
        load_json(args.verdict),
        repo,
    )
    print(dump_json(verdict))
    return 0 if verdict["ok"] else 1


def cmd_validate_failure(args):
    print(dump_json(validate_failure_classification(load_json(args.classification))))
    return 0


def cmd_next_action(args):
    print(dump_json(next_action(load_json(args.classification), args.risk)))
    return 0


def parser():
    p = argparse.ArgumentParser(description="AI Development Harness V5 Evidence Loop")
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

    packet = sub.add_parser("verifier-packet")
    packet.add_argument("--task", required=True)
    packet.add_argument("--preflight", required=True)
    packet.add_argument("--verification", required=True)
    packet.add_argument("--repo", default=".")
    packet.set_defaults(func=cmd_verifier_packet)

    verdict = sub.add_parser("validate-verdict")
    verdict.add_argument("--verdict", required=True)
    verdict.set_defaults(func=cmd_validate_verdict)

    acceptance = sub.add_parser("guard-acceptance")
    acceptance.add_argument("--task", required=True)
    acceptance.add_argument("--preflight", required=True)
    acceptance.add_argument("--packet", required=True)
    acceptance.add_argument("--verdict", required=True)
    acceptance.add_argument("--repo", default=".")
    acceptance.set_defaults(func=cmd_guard_acceptance)

    failure = sub.add_parser("validate-failure")
    failure.add_argument("--classification", required=True)
    failure.set_defaults(func=cmd_validate_failure)

    action = sub.add_parser("next-action")
    action.add_argument("--classification", required=True)
    action.add_argument("--risk", choices=["GREEN", "YELLOW", "RED"], default="GREEN")
    action.set_defaults(func=cmd_next_action)
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
