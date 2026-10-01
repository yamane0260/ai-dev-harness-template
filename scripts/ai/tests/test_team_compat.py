"""Tests for V4.1 Team Compatibility sidecar behavior."""
from __future__ import annotations
import importlib.util, importlib.machinery, subprocess, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SCRIPT=ROOT/"scripts"/"ai"/"team-compat.py"
loader=importlib.machinery.SourceFileLoader("team_compat",str(SCRIPT))
spec=importlib.util.spec_from_loader(loader.name,loader)
team_compat=importlib.util.module_from_spec(spec)
loader.exec_module(team_compat)

class TeamCompatTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/"repo";self.root.mkdir()
        subprocess.run(["git","init","-b","main"],cwd=self.root,check=True,capture_output=True)
        subprocess.run(["git","config","user.name","Harness Test"],cwd=self.root,check=True)
        subprocess.run(["git","config","user.email","harness@example.invalid"],cwd=self.root,check=True)
        (self.root/".github").mkdir()
        (self.root/".github/pull_request_template.md").write_text("## Summary\n\n## Test plan\n",encoding="utf-8")
        (self.root/"CONTRIBUTING.md").write_text("All commits must include Signed-off-by.\n",encoding="utf-8")
        for i in range(8):
            (self.root/"x.txt").write_text(str(i),encoding="utf-8")
            subprocess.run(["git","add","."],cwd=self.root,check=True)
            subprocess.run(["git","commit","-s","-m",f"feat: change {i}"],cwd=self.root,check=True,capture_output=True)
    def tearDown(self): self.tmp.cleanup()
    def test_observe_rules(self):
        profile=team_compat.observe(self.root,20)
        keys={x["key"] for x in profile["rules"]}
        self.assertIn("template.present",keys)
        self.assertIn("signoff.required",keys)
        self.assertIn("message.conventional-commits",keys)
        self.assertTrue(profile["safety"]["inferred_rules_do_not_weaken_verification"])
    def test_guard(self):
        p=team_compat.observe(self.root,20)
        self.assertFalse(team_compat.guard("commit","feat: x",p)["allowed"])
        self.assertFalse(team_compat.guard("commit","feat: x\n\nAI Dev Harness",p)["allowed"])
        self.assertTrue(team_compat.guard("commit","feat: x\n\nSigned-off-by: Harness Test <harness@example.invalid>",p)["allowed"])
    def test_sidecar_outside_repo(self):
        state=team_compat.get_state_root(self.root,Path(self.tmp.name)/"state")
        with self.assertRaises(ValueError):
            state.relative_to(self.root)

if __name__=="__main__": unittest.main()
