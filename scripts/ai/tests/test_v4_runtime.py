"""Regression tests for the V4 composition and dashboard substrate."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.v4_core import build_read_model, compile_plan, completion_blockers, emit_event, initialize_project, save_plan

class V4RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "AGENTS.md").write_text("# test\n", encoding="utf-8")
        (self.root / "ai" / "v4" / "profiles").mkdir(parents=True)
        (self.root / "ai" / "v4" / "self-description.json").write_text(
            json.dumps({
                "schema_version":"1.0",
                "architecture":{"nodes":[],"edges":[]},
                "components":{
                    "profile.resolve":{"label":{"ja":"方針"},"technical_name":"Profile Resolver","summary":{"ja":"summary"}},
                    "risk.floor":{"label":{"ja":"Risk"},"technical_name":"Risk Floor","summary":{"ja":"summary"}},
                    "project.explore":{"label":{"ja":"Explore"},"technical_name":"Explore","summary":{"ja":"summary"}},
                    "change.implement":{"label":{"ja":"Implement"},"technical_name":"Implement","summary":{"ja":"summary"}},
                    "verification.run":{"label":{"ja":"Verify"},"technical_name":"Verify","summary":{"ja":"summary"}},
                    "assurance.evaluate":{"label":{"ja":"Assurance"},"technical_name":"Assurance","summary":{"ja":"summary"}},
                    "knowledge.explain-change":{"label":{"ja":"Explain"},"technical_name":"Explain","summary":{"ja":"summary"}},
                    "knowledge.legibility":{"label":{"ja":"Legibility"},"technical_name":"Legibility","summary":{"ja":"summary"}},
                    "review.security":{"label":{"ja":"Security"},"technical_name":"Security","summary":{"ja":"summary"}},
                    "release.evaluate":{"label":{"ja":"Release"},"technical_name":"Release","summary":{"ja":"summary"}}
                },
                "reason_codes":{"PLAN_COMPILED":{"ja":"compiled"}}
            }), encoding="utf-8"
        )
        profile = {
            "schema_version":"1.0","id":"balanced",
            "objectives":{
                "delivery_speed":"high","autonomy":"high","human_understanding":"medium",
                "handoff_depth":"medium","human_attention":"low","context_efficiency":"high"
            },
            "constraints":{
                "risk_policy":{"allow_below_deterministic_floor":False},
                "required_capabilities":[
                    {"capability":"risk.floor","contract_version":1,"when":"always"},
                    {"capability":"profile.resolve","contract_version":1,"when":"always"},
                    {"capability":"assurance.evaluate","contract_version":1,"when":"risk-yellow-or-higher"}
                ]
            },
            "understanding":{
                "requirement":"WORKING","knowledge_impact_policy":"durable-on-material",
                "fresh_legibility_review":"material"
            },
            "context_budget":{
                "strategy":"balanced","parent_tokens":36000,"plugin_instruction_tokens":8000,
                "tool_result_tokens":10000,"child_context_isolation_preferred":True,
                "compaction_allowed":True
            }
        }
        (self.root / "ai" / "v4" / "profiles" / "balanced.json").write_text(json.dumps(profile),encoding="utf-8")
        capabilities = [
            "profile.resolve","risk.floor","project.explore","change.implement","verification.run",
            "assurance.evaluate","knowledge.explain-change","knowledge.legibility","review.security",
            "release.evaluate"
        ]
        providers=[]
        for capability in capabilities:
            providers.append({
                "schema_version":"1.0","id":"test."+capability.replace(".","-"),"version":"1.0.0",
                "implements":{"capability":capability,"contract_version":1},
                "requires":[],"permissions":{},"context":{"parent_budget_tokens":0},
                "failure":{"mode":"block"},"lifecycle":{"state":"stateless"},"cost":{}
            })
        (self.root / "ai" / "v4" / "provider-registry.json").write_text(
            json.dumps({"schema_version":"1.0","providers":providers}),encoding="utf-8"
        )
        initialize_project(self.root)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_balanced_implementation_plan(self) -> None:
        plan=compile_plan(self.root,risk="GREEN",task_kind="implement")
        selected={item["capability"] for item in plan["selected"]}
        self.assertIn("change.implement",selected)
        self.assertIn("verification.run",selected)
        self.assertNotIn("assurance.evaluate",selected)
        self.assertFalse(plan["invalid_reasons"])

    def test_yellow_adds_assurance(self) -> None:
        plan=compile_plan(self.root,risk="YELLOW",task_kind="implement")
        selected={item["capability"] for item in plan["selected"]}
        self.assertIn("assurance.evaluate",selected)

    def test_security_and_knowledge_routing(self) -> None:
        plan=compile_plan(
            self.root,risk="YELLOW",task_kind="implement",
            quality_impacts=["security"],knowledge_impact="MATERIAL"
        )
        selected={item["capability"] for item in plan["selected"]}
        self.assertIn("review.security",selected)
        self.assertIn("knowledge.explain-change",selected)
        self.assertIn("knowledge.legibility",selected)

    def test_event_rejects_secret_like_payload(self) -> None:
        with self.assertRaises(ValueError):
            emit_event(
                self.root,run_id="run_test",event_type="test.event",status="success",
                details={"api_token":"should-not-be-recorded"}
            )

    def test_read_model_from_events(self) -> None:
        run_id="run_test"
        plan=compile_plan(self.root,risk="GREEN",task_kind="implement")
        save_plan(self.root,run_id,plan)
        emit_event(
            self.root,run_id=run_id,event_type="run.started",status="running",
            component="profile.resolve",details={"summary":"開始"}
        )
        emit_event(
            self.root,run_id=run_id,event_type="verification.completed",status="success",
            component="verification.run",details={"summary":"28件成功"}
        )
        emit_event(
            self.root,run_id=run_id,event_type="human_check.required",status="pending",
            details={"summary":"実機確認"}
        )
        model=build_read_model(self.root,run_id)
        self.assertEqual(model["work"]["verification"]["state"],"success")
        self.assertEqual(model["diagnosis"]["human_check_count"],1)
        self.assertGreaterEqual(model["diagnosis"]["event_count"],3)


    def test_completion_requires_verification(self) -> None:
        run_id="run_finish"
        plan=compile_plan(self.root,risk="GREEN",task_kind="implement")
        save_plan(self.root,run_id,plan)
        emit_event(
            self.root,run_id=run_id,event_type="run.started",status="running",
            component="profile.resolve",details={"summary":"開始"}
        )
        blockers=completion_blockers(self.root,run_id)
        self.assertIn("required deterministic verification has not passed",blockers)
        emit_event(
            self.root,run_id=run_id,event_type="verification.completed",status="success",
            component="verification.run",details={"summary":"成功"}
        )
        self.assertEqual(completion_blockers(self.root,run_id),[])

if __name__ == "__main__":
    unittest.main()
