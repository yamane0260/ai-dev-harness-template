#!/usr/bin/env python3
"""V4.1 Team Compatibility sidecar observer and external-surface guard."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CONVENTIONAL=re.compile(r"^(?:build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(?:\([^)]+\))?!?:\s+\S",re.I)
SIGNED_OFF=re.compile(r"(?im)^Signed-off-by:\s+.+<[^>]+>\s*$")
AI_TERM=re.compile(r"(?i)\b(?:AI|Copilot|ChatGPT|Claude)\b|生成AI")
AI_REQ=re.compile(r"(?is)(?:\b(?:AI|Copilot|ChatGPT|Claude)\b|生成AI).{0,160}(?:must|required|disclos|必須|明記|開示|記載)|(?:must|required|disclos|必須|明記|開示|記載).{0,160}(?:\b(?:AI|Copilot|ChatGPT|Claude)\b|生成AI)")
SIGNOFF_REQ=re.compile(r"(?is)(?:DCO|Signed-off-by).{0,160}(?:must|required|必須|必要)|(?:must|required|必須|必要).{0,160}(?:DCO|Signed-off-by)")
MARKERS=[
 ("HARNESS_NAME",re.compile(r"(?i)\bAI Dev Harness\b")),
 ("HARNESS_STATE",re.compile(r"(?:^|[\\/])(?:\.ai-artifacts|\.harness)(?:[\\/]|$)",re.I)),
 ("HARNESS_CAPABILITY",re.compile(r"(?i)\bcollaboration\.(?:observe|profile|surface\.adapt|surface\.guard)\b")),
]

def git(root:Path,*args:str)->str:
 try:return subprocess.run(["git",*args],cwd=root,text=True,capture_output=True,check=True).stdout.strip()
 except (OSError,subprocess.CalledProcessError):return ""

def utc()->str:return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def fingerprint(root:Path)->str:
 remote=git(root,"remote","get-url","origin") or str(root.resolve())
 remote=re.sub(r"(https?://)[^/@\s]+@",r"\1",remote)
 return hashlib.sha256(remote.encode()).hexdigest()[:24]

def get_state_root(root:Path,home:Path|None)->Path:
 base=home or Path(os.environ.get("HARNESS_STATE_HOME",str(Path.home()/".local/state/ai-dev-harness")))
 target=base.expanduser().resolve()/"repositories"/fingerprint(root)
 try:
  target.relative_to(root.resolve())
 except ValueError:return target
 raise ValueError("sidecar state must be outside the target repository")

def mk_rule(surface,key,value,strength,confidence,count,sources):
 return {"surface":surface,"key":key,"value":value,"strength":strength,"confidence":round(confidence,3),"evidence_count":count,"sources":sources}

def candidates(root:Path):
 fixed=[("CONTRIBUTING.md","contributing"),("docs/CONTRIBUTING.md","contributing"),(".github/pull_request_template.md","pr-template"),(".github/CODEOWNERS","codeowners"),("CODEOWNERS","codeowners"),("AGENTS.md","agent-instructions"),("CLAUDE.md","agent-instructions"),(".github/copilot-instructions.md","agent-instructions")]
 out=[]
 for rel,kind in fixed:
  p=root/rel
  if p.is_file():out.append((p,kind))
 d=root/".github/PULL_REQUEST_TEMPLATE"
 if d.is_dir():out.extend((p,"pr-template") for p in sorted(d.glob("*.md")))
 return out

def observe(root:Path,limit:int)->dict:
 if not (root/".git").exists():raise ValueError("target must be a Git working tree")
 if not 1<=limit<=500:raise ValueError("history limit must be 1..500")
 rules=[];sources=[];texts=[]
 for p,kind in candidates(root):
  raw=p.read_bytes();rel=p.relative_to(root).as_posix();text=raw[:262144].decode("utf-8","replace")
  sources.append({"path":rel,"kind":kind,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)})
  texts.append((rel,text))
  if kind=="pr-template":
   heads=[x.strip() for x in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$",text) if x.strip()]
   rules.append(mk_rule("pull_request","template.present",{"path":rel,"headings":heads[:24]},"explicit",1.0,1,[rel]))
  elif kind=="codeowners":rules.append(mk_rule("pull_request","codeowners.present",True,"explicit",1.0,1,[rel]))
 ai=[p for p,t in texts if AI_REQ.search(t)]
 if ai:rules.append(mk_rule("external","ai-disclosure.guidance",True,"explicit",1.0,len(ai),ai))
 sign=[p for p,t in texts if SIGNOFF_REQ.search(t)]
 if sign:rules.append(mk_rule("commit","signoff.required",True,"explicit",1.0,len(sign),sign))
 subjects=[x for x in git(root,"log",f"-n{limit}","--pretty=format:%s").splitlines() if x.strip()]
 if subjects:
  n=sum(bool(CONVENTIONAL.match(x)) for x in subjects);ratio=n/len(subjects)
  if n>=3:rules.append(mk_rule("commit","message.conventional-commits",True,"strong-inferred" if len(subjects)>=8 and ratio>=.8 else "tentative",ratio,n,["git-log:subjects"]))
 branches=[]
 for x in git(root,"for-each-ref","--format=%(refname:short)","refs/heads","refs/remotes/origin").splitlines():
  x=x.strip().removeprefix("origin/")
  if x and x not in {"main","master","HEAD"}:branches.append(x)
 prefixes=[x.split("/",1)[0] for x in branches if "/" in x]
 if len(prefixes)>=5:
  c=Counter(prefixes);common=[{"prefix":k,"count":v} for k,v in c.most_common(6)];ratio=common[0]["count"]/len(prefixes)
  rules.append(mk_rule("branch","prefixes.observed",common,"strong-inferred" if len(prefixes)>=10 and ratio>=.85 else "tentative",ratio,len(prefixes),["git-refs:branches"]))
 return {
  "schema_version":"1.0","generated_at":utc(),
  "repository":{"fingerprint":fingerprint(root),"name":root.name,"source_revision":git(root,"rev-parse","HEAD") or "unknown"},
  "mode":"sidecar","observation":{"history_limit":limit,"commit_subject_count":len(subjects),"branch_count":len(branches)},
  "explicit_sources":sources,"rules":sorted(rules,key=lambda x:(x["surface"],x["key"])),
  "unknowns":["Repository-host rulesets, branch protection, and PR discussion patterns require a host-specific observer."],
  "safety":{"inferred_rules_do_not_weaken_verification":True,"explicit_disclosure_requirements_must_be_preserved":True,"harness_markers_blocked_on_external_surfaces":True}
 }

def profile_path(state:Path)->Path:return state/"team/profile.json"

def guard(surface:str,text:str,profile:dict)->dict:
 findings=[]
 for code,pat in MARKERS:
  if pat.search(text):findings.append({"severity":"block","code":code,"message":"Harness-internal detail would be exposed on a team-visible surface."})
 rules=profile.get("rules",[])
 if surface=="commit":
  if any(r.get("key")=="signoff.required" for r in rules) and not SIGNED_OFF.search(text):findings.append({"severity":"block","code":"TEAM_SIGNOFF_REQUIRED","message":"Explicit team guidance requires Signed-off-by."})
  if any(r.get("key")=="message.conventional-commits" and r.get("strength")=="strong-inferred" for r in rules) and not CONVENTIONAL.match(text.splitlines()[0] if text.splitlines() else ""):findings.append({"severity":"warning","code":"TEAM_COMMIT_STYLE_DIFFERENCE","message":"Commit subject differs from the strongly observed pattern."})
 if surface=="pull_request":
  heads=[]
  for r in rules:
   if r.get("key")=="template.present" and isinstance(r.get("value"),dict):heads.extend(r["value"].get("headings",[]))
  missing=[h for h in dict.fromkeys(heads) if h not in text]
  if missing:findings.append({"severity":"warning","code":"TEAM_PR_TEMPLATE_DIFFERENCE","message":"Pull-request body is missing observed template headings.","missing_headings":missing[:12]})
 if any(r.get("key")=="ai-disclosure.guidance" for r in rules) and not AI_TERM.search(text):findings.append({"severity":"block","code":"TEAM_AI_DISCLOSURE_CONFIRMATION_REQUIRED","message":"Explicit AI disclosure guidance was detected; preserve the team's disclosure requirement."})
 return {"schema_version":"1.0","surface":surface,"allowed":not any(f["severity"]=="block" for f in findings),"findings":findings}

def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--state-home",type=Path)
 sub=p.add_subparsers(dest="cmd",required=True)
 o=sub.add_parser("observe");o.add_argument("--history-limit",type=int,default=50)
 sub.add_parser("show")
 g=sub.add_parser("guard");g.add_argument("--surface",choices=("branch","commit","pull_request","comment"),required=True);g.add_argument("--text");g.add_argument("--file",type=Path)
 a=p.parse_args();root=a.repo.expanduser().resolve();state=get_state_root(root,a.state_home);state.mkdir(parents=True,exist_ok=True)
 if a.cmd=="observe":
  prof=observe(root,a.history_limit);path=profile_path(state);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(prof,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"profile":str(path),"rule_count":len(prof["rules"]),"source_count":len(prof["explicit_sources"])},ensure_ascii=False,indent=2));return 0
 path=profile_path(state)
 if not path.is_file():raise ValueError("no Team Profile; run observe first")
 prof=json.loads(path.read_text(encoding="utf-8"))
 if a.cmd=="show":print(json.dumps(prof,ensure_ascii=False,indent=2));return 0
 text=a.file.read_text(encoding="utf-8") if a.file else (a.text if a.text is not None else sys.stdin.read())
 result=guard(a.surface,text,prof);print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result["allowed"] else 2
if __name__=="__main__":raise SystemExit(main())
