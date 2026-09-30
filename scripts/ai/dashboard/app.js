let state=null;
let technicalNames=false;

const $=(id)=>document.getElementById(id);
const esc=(v)=>String(v??"").replace(/[&<>"']/g,(m)=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));
const fmtTime=(value)=>{if(!value)return "";try{return new Date(value).toLocaleString("ja-JP")}catch{return value}};
const fmtDuration=(ms)=>{if(ms==null)return "–";if(ms<1000)return ms+"ms";const s=Math.round(ms/1000);return s<60?s+"秒":Math.floor(s/60)+"分"+(s%60)+"秒"};

function stateLabel(v){
  return ({idle:"待機中",running:"作業中",complete:"最近の作業は完了",attention:"確認が必要"})[v]||v;
}
function stateClass(v){
  return v==="complete"?"good":v==="attention"?"bad":v==="running"?"warn":"neutral";
}
function row(icon,title,sub,klass=""){
  return '<div class="row '+klass+'"><div class="icon">'+icon+'</div><div><div class="row-title">'+esc(title)+'</div>'+(sub?'<div class="row-sub">'+esc(sub)+'</div>':"")+'</div></div>';
}
function renderWork(){
  const w=state.work;
  $("current-summary").textContent=w.current.summary||"作業履歴はまだありません";
  $("current-component").textContent=w.current.component?("現在: "+humanName(w.current.component)):"";
  const checks=w.attention||[];
  $("attention-list").innerHTML=checks.length
    ? '<div class="list">'+checks.map(c=>row("! ",c.summary,c.status,"warn")).join("")+'</div>'
    : '<div class="empty">現在、人による確認はありません。</div>';

  const v=w.verification||{};
  let vklass=v.state==="success"?"good":v.state==="failure"?"bad":"";
  let vicon=v.state==="success"?"✓":v.state==="failure"?"×":"○";
  $("verification-card").innerHTML='<div class="list">'+row(vicon,"自動確認",v.summary||statusHuman(v.state),vklass)+'</div>';

  $("changes-list").innerHTML=(w.recent_changes||[]).length
    ? '<div class="list">'+w.recent_changes.map(c=>row("•",c,"")).join("")+'</div>'
    : '<div class="empty">記録された変更はまだありません。</div>';
}
function humanName(id){
  const c=state?.harness?.components?.[id];
  if(!c)return id||"";
  return technicalNames?(c.technical_name||id):(c.label?.ja||id);
}
function statusHuman(v){return ({success:"成功",failure:"失敗",blocked:"停止",running:"実行中",pending:"未完了","not-run":"未実行",unknown:"不明"})[v]||v||"不明"}
function renderSystem(){
  const arch=state.harness.architecture||{};
  const active=new Set(state.harness.active_components||[]);
  const statuses=state.harness.component_states||{};
  const nodes=arch.nodes||[];
  $("architecture-map").innerHTML=nodes.map((node,i)=>{
    const id=node.id;
    const isActive=active.has(id)||id==="request"||id==="complete";
    const problem=["failure","blocked"].includes(statuses[id]);
    const c=state.harness.components[id];
    const label=technicalNames?(c?.technical_name||id):(node.label?.ja||c?.label?.ja||id);
    return '<div class="node-wrap"><button class="node '+(isActive?"active ":"")+(problem?"problem":"")+'" data-component="'+esc(id)+'"><div class="node-label">'+esc(label)+'</div>'+(technicalNames&&c?'<div class="node-tech">'+esc(id)+'</div>':"")+'</button>'+(i<nodes.length-1?'<span class="arrow">→</span>':"")+'</div>';
  }).join("");
  document.querySelectorAll(".node[data-component]").forEach(b=>b.onclick=()=>showComponent(b.dataset.component));

  const selected=state.harness.selected||[];
  $("selected-components").innerHTML=selected.length?selected.map(item=>{
    const c=state.harness.components[item.capability];
    return '<button class="component-card" data-component="'+esc(item.capability)+'"><div class="component-name">'+esc(technicalNames?(c?.technical_name||item.capability):(c?.label?.ja||item.capability))+'</div><div class="component-meta">'+esc(statusHuman(state.harness.component_states[item.capability]||"selected"))+' · '+esc(item.provider)+'</div></button>';
  }).join(""):'<div class="empty">実行計画はまだありません。</div>';
  document.querySelectorAll(".component-card").forEach(b=>b.onclick=()=>showComponent(b.dataset.component));
}
function showComponent(id){
  const c=state.harness.components[id]||{};
  $("component-title").textContent=technicalNames?(c.technical_name||id):(c.label?.ja||id);
  const selected=(state.harness.selected||[]).find(x=>x.capability===id);
  const reason=selected?.reason;
  const reasonText=state.harness.reason_codes?.[reason]?.ja||reason||"";
  $("component-detail").classList.remove("muted");
  $("component-detail").innerHTML=
    '<p>'+esc(c.summary?.ja||"この項目の説明はまだ登録されていません。")+'</p>'+
    (c.purpose?.ja?'<p><strong>役割</strong><br>'+esc(c.purpose.ja)+'</p>':"")+
    (selected?'<p><strong>今回の実装</strong><br>'+esc(selected.provider)+'</p>':"")+
    (reasonText?'<p><strong>なぜ使われた？</strong><br>'+esc(reasonText)+'</p>':"")+
    '<p class="muted">'+esc(c.technical_name||id)+' · '+esc(id)+'</p>';
}
function renderDiagnosis(){
  const d=state.diagnosis;
  const metrics=[
    ["実行時間",fmtDuration(d.duration_ms)],["再試行",d.retry_count],["方式切替",d.fallback_count],
    ["人の確認",d.human_check_count],["情報整理",d.context_compaction_count]
  ];
  $("metrics").innerHTML=metrics.map(([label,val])=>'<div class="metric"><div class="metric-value">'+esc(val)+'</div><div class="metric-label">'+esc(label)+'</div></div>').join("");
  const events=state.technical.events||[];
  $("timeline").innerHTML=events.length?events.map(e=>'<div class="timeline-item '+esc(e.status)+'"><span class="dot"></span><div><div class="timeline-type">'+esc(eventHuman(e.type,e.component))+'</div><div class="timeline-meta">'+esc(statusHuman(e.status))+' · '+esc(fmtTime(e.timestamp))+(e.details?.summary?' · '+esc(e.details.summary):"")+'</div></div></div>').join(""):'<div class="empty">Run履歴はまだありません。</div>';
  const anomalies=d.anomalies||[];
  $("anomalies").innerHTML=anomalies.length?'<div class="list">'+anomalies.map(a=>row("!",a.summary,a.kind,"warn")).join("")+'</div>':'<div class="empty">現在、目立った異常は記録されていません。</div>';
  $("plan-json").textContent=JSON.stringify(state.technical.plan,null,2);
  $("events-json").textContent=JSON.stringify(events,null,2);
}
function eventHuman(type,component){
  const names={
    "run.started":"作業を開始","run.completed":"作業を完了","run.failed":"作業に失敗",
    "capability.started":"機能を開始","capability.completed":"機能を完了","capability.failed":"機能に失敗",
    "verification.completed":"自動確認を完了","human_check.required":"人の確認が必要",
    "fallback.performed":"別の方法へ切替","retry.performed":"再試行","context.compacted":"会話情報を整理","change.recorded":"変更を記録"
  };
  return (names[type]||type)+(component?" · "+humanName(component):"");
}
function render(){
  if(!state)return;
  $("project-name").textContent=state.project.name;
  $("project-meta").textContent=[state.project.branch,state.project.revision,"Profile: "+state.project.profile].join(" · ");
  $("overall-state").textContent=stateLabel(state.work.state);
  $("overall-state").className="state-pill "+stateClass(state.work.state);
  $("last-updated").textContent="更新: "+fmtTime(state.generated_at);
  renderWork();renderSystem();renderDiagnosis();
}
async function refresh(){
  try{
    const response=await fetch("/api/state",{cache:"no-store"});
    state=await response.json();
    if(!response.ok)throw new Error(state.message||"dashboard state failed");
    render();
  }catch(err){
    $("overall-state").textContent="Dashboard error";
    $("overall-state").className="state-pill bad";
    console.error(err);
  }
}
document.querySelectorAll(".tab").forEach(button=>button.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===button));
  document.querySelectorAll(".view").forEach(x=>x.classList.remove("active"));
  $("view-"+button.dataset.view).classList.add("active");
});
document.querySelectorAll("[data-jump]").forEach(button=>button.onclick=()=>{
  document.querySelector('.tab[data-view="'+button.dataset.jump+'"]').click();
});
$("technical-toggle").onchange=(e)=>{technicalNames=e.target.checked;renderSystem()};
refresh();setInterval(refresh,2000);
