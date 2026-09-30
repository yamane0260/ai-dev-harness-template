#!/usr/bin/env python3
"""AI Dev Harness V4 command-line entrypoint."""
from __future__ import annotations

import argparse
import json
import sys
import uuid
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.v4_core import (
    build_read_model, compile_plan, emit_event, find_repo_root, initialize_project,
    save_plan, write_read_model,
)

def print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))

def main() -> int:
    parser = argparse.ArgumentParser(prog="v4.py")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize project-local dashboard config")
    init.add_argument("--force", action="store_true")

    plan = sub.add_parser("plan", help="compile and persist a V4 execution plan")
    plan.add_argument("--task", choices=("implement","debug","explain"), default="implement")
    plan.add_argument("--profile")
    plan.add_argument("--risk", choices=("GREEN","YELLOW","RED","green","yellow","red"))
    plan.add_argument("--quality", action="append", default=[])
    plan.add_argument("--knowledge-impact", default="LOW")
    plan.add_argument("--release", action="store_true")
    plan.add_argument("--claims-present", action="store_true")
    plan.add_argument("--host", default="generic")
    plan.add_argument("--run-id")

    event = sub.add_parser("event", help="append a sanitized V4 run event")
    event.add_argument("--run-id", required=True)
    event.add_argument("--type", required=True)
    event.add_argument("--status", choices=("pending","running","success","failure","blocked","skipped","unknown"), required=True)
    event.add_argument("--component")
    event.add_argument("--reason-code")
    event.add_argument("--summary")
    event.add_argument("--details-json")

    state = sub.add_parser("state", help="build dashboard read model")
    state.add_argument("--run-id")
    state.add_argument("--write", action="store_true")

    dashboard = sub.add_parser("dashboard", help="serve the project-local dashboard")
    dashboard.add_argument("--host", default="127.0.0.1")
    dashboard.add_argument("--port", type=int, default=4310)
    dashboard.add_argument("--no-browser", action="store_true")

    args = parser.parse_args()
    root = find_repo_root()

    if args.command == "init":
        path = initialize_project(root, force=args.force)
        print(path.relative_to(root))
        return 0

    if args.command == "plan":
        run_id = args.run_id or f"run_{uuid.uuid4().hex[:12]}"
        compiled = compile_plan(
            root, task_kind=args.task, profile_id=args.profile,
            risk=args.risk, quality_impacts=args.quality,
            knowledge_impact=args.knowledge_impact,
            release=args.release, claims_present=args.claims_present, host=args.host,
        )
        save_plan(root, run_id, compiled)
        emit_event(
            root, run_id=run_id, event_type="run.started", status="running",
            component="profile.resolve",
            reason_code="PLAN_INVALID" if compiled.get("invalid_reasons") else "PLAN_COMPILED",
            details={"summary": f"V4 plan compiled for {args.task}", "plan_id": compiled["plan_id"]},
        )
        write_read_model(root, run_id)
        print_json({"run_id": run_id, "plan": compiled})
        return 2 if compiled.get("invalid_reasons") else 0

    if args.command == "event":
        details = {}
        if args.details_json:
            parsed = json.loads(args.details_json)
            if not isinstance(parsed, dict):
                raise ValueError("--details-json must contain an object")
            details.update(parsed)
        if args.summary:
            details["summary"] = args.summary
        item = emit_event(
            root, run_id=args.run_id, event_type=args.type, status=args.status,
            component=args.component, reason_code=args.reason_code, details=details,
        )
        write_read_model(root, args.run_id)
        print_json(item)
        return 0

    if args.command == "state":
        if args.write:
            path = write_read_model(root, args.run_id)
            print(path.relative_to(root))
        else:
            print_json(build_read_model(root, args.run_id))
        return 0

    if args.command == "dashboard":
        from lib.v4_dashboard import serve
        initialize_project(root)
        url = f"http://{args.host}:{args.port}"
        if not args.no_browser:
            webbrowser.open(url)
        print(f"Harness Dashboard: {url}")
        serve(root, args.host, args.port)
        return 0

    return 2

if __name__ == "__main__":
    raise SystemExit(main())
