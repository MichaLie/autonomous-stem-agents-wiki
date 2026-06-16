#!/usr/bin/env python3
"""Build a single self-contained interactive HTML index of autonomous science agents.
Usage: python3 build_html.py [agents_final.json] [out.html]
"""
import json, sys, html, datetime
from collections import Counter

SRC = sys.argv[1] if len(sys.argv) > 1 else 'agents_final.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'autonomous_stem_agents_wiki.html'
items = json.load(open(SRC))

CAT_LABELS = {
    'crossdomain': 'Cross-domain', 'biology': 'Biology & Medicine',
    'chemistry': 'Chemistry & Materials', 'physics': 'Physics / Astronomy / Eng.',
    'benchmark': 'Benchmarks & Harnesses',
}
CAT_ORDER = ['crossdomain', 'biology', 'chemistry', 'physics', 'benchmark']

ACCESS_LABELS = {
    'open-source': 'Open source', 'open-data': 'Open data', 'platform': 'Platform / API',
    'lab-gated': 'Lab-gated', 'paper-only': 'Paper-only', 'list': 'List',
}
ACCESS_ORDER = ['open-source', 'open-data', 'platform', 'lab-gated', 'paper-only', 'list']

AUTON_LABELS = {
    'A1': 'A1 Assistant', 'A2': 'A2 Tool agent', 'A3': 'A3 Workflow agent',
    'A4': 'A4 In-silico scientist', 'A5': 'A5 Lab/physical scientist', 'B': 'B Benchmark/harness',
}
AUTON_ORDER = ['A1', 'A2', 'A3', 'A4', 'A5', 'B']

def auton_primary(a):
    a = (a or '').upper()
    best = None
    for d in ['1', '2', '3', '4', '5']:
        if 'A' + d in a:
            best = 'A' + d
    if best:
        return best
    if 'B' in a:
        return 'B'
    return 'A3'

def norm_access(a):
    a = (a or '').lower()
    if a in ACCESS_LABELS:
        return a
    if 'list' in a:
        return 'list'
    if 'lab' in a or 'institution' in a or 'hardware' in a or 'robot' in a:
        return 'lab-gated'
    if 'paper' in a or 'unclear' in a or 'concept' in a:
        return 'paper-only'
    if 'platform' in a or 'api' in a or 'commercial' in a or 'enterprise' in a or 'closed' in a:
        return 'platform'
    if 'data' in a or 'weights' in a or 'benchmark' in a:
        return 'open-data'
    if 'open' in a:
        return 'open-source'
    return 'paper-only'

norm = []
for m in items:
    acc = norm_access(m.get('access', ''))
    ap = auton_primary(m.get('autonomy', ''))
    rec = {
        'name': m.get('name', ''), 'category': m.get('category', 'crossdomain'),
        'domain': m.get('domain', ''), 'access': acc, 'access_raw': m.get('access', ''),
        'autonomy': m.get('autonomy', '') or ap, 'ap': ap,
        'inputs': m.get('inputs', ''), 'outputs': m.get('outputs', ''),
        'notes': m.get('notes', ''),
        'paper_links': m.get('paper_links', []), 'repo_links': m.get('repo_links', []),
        'new': bool(m.get('new', False)),
        'hasRepo': len(m.get('repo_links', [])) > 0,
    }
    rec['_s'] = ' '.join([rec['name'], rec['domain'], rec['notes'], rec['inputs'], rec['outputs'],
                          CAT_LABELS.get(rec['category'], '')]).lower()
    norm.append(rec)

ACC_RANK = {k: i for i, k in enumerate(ACCESS_ORDER)}
def sort_key(m):
    return (CAT_ORDER.index(m['category']) if m['category'] in CAT_ORDER else 99,
            ACC_RANK.get(m['access'], 9), m['name'].lower())
norm.sort(key=sort_key)

today = datetime.date.today().isoformat()
total = len(norm)
n_new = sum(1 for m in norm if m['new'])
n_cats = len(set(m['category'] for m in norm))
acc_c = Counter(m['access'] for m in norm)
ap_c = Counter(m['ap'] for m in norm)
n_open = acc_c.get('open-source', 0)
n_lab = sum(1 for m in norm if m['ap'] == 'A5')
n_bench = sum(1 for m in norm if m['category'] == 'benchmark')

QUICK = [
    ("Biomedical agent you can run", "Biomni, PaperQA2, TxAgent"),
    ("Literature-grounded QA", "PaperQA2, Asta, Elicit"),
    ("End-to-end ML research", "The AI Scientist, AI Scientist-v2, Agent Laboratory"),
    ("Autonomous discovery platform", "Kosmos, Google AI Co-Scientist, Robin"),
    ("Single-cell / omics analysis", "CellVoyager, SpatialAgent, CellAgent"),
    ("Chemistry tool-use agent", "ChemCrow, CACTUS, ChemToolAgent"),
    ("Self-driving chemistry lab", "Coscientist, Chemist-X, A-Lab"),
    ("Materials / DFT automation", "AtomAgents, VASPilot, MatClaw, ChemGraph"),
    ("Physics / simulation", "OpenFOAMGPT, MechAgents, cmbagent"),
    ("Protein / antibody design", "ProtAgents, The Virtual Lab, OriGene"),
    ("Evaluate an agent (benchmark)", "ScienceAgentBench, AstaBench, MLE-bench"),
]
quick_rows = "\n".join(
    f'<tr><td><button class="qcbtn" data-q="{html.escape(v.split(",")[0].strip())}">filter</button></td>'
    f'<td>{html.escape(n)}</td><td>{html.escape(v)}</td></tr>' for n, v in QUICK)

TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Autonomous Science Agents — Researcher Index</title>
<style>
:root{--bg:#f6f7f9;--panel:#fff;--ink:#1a1d24;--muted:#5b6472;--line:#e3e7ee;--accent:#2563eb;
--chip:#eef1f6;--chipline:#dce1ea;--rowhover:#f0f4fb;--detail:#f8fafc;
--open:#0f7a3d;--openbg:#e3f6ec;--data:#0e7490;--databg:#dcf2f6;--platform:#6d28d9;--platformbg:#efe7fc;
--lab:#9a5b00;--labbg:#fbeed5;--paper:#a13a3a;--paperbg:#fbe6e6;--list:#1763a6;--listbg:#e1eefb;--new:#d6336c;
--a1:#7a8699;--a2:#3f8fd0;--a3:#2563eb;--a4:#7b3fe4;--a5:#c026a6;--bb:#5b6472;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:13.5px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1340px;margin:0 auto;padding:16px 18px 90px}
header.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
h1{font-size:21px;margin:0 0 4px}.sub{color:var(--muted);font-size:12.5px;max-width:860px}
.toolbtn{background:var(--panel);border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:7px 12px;cursor:pointer;font-size:13px}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 2px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:7px 12px}
.stat b{font-size:17px}.stat span{color:var(--muted);font-size:11.5px;display:block}
.controls{position:sticky;top:0;z-index:30;background:var(--bg);padding:10px 0 8px;border-bottom:1px solid var(--line);margin-bottom:4px}
.searchrow{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
#q{flex:1;min-width:240px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink);font-size:14px}
.toolbtn.sm{padding:8px 11px}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px;align-items:center}
.chips .lbl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-right:2px}
.chip{background:var(--chip);border:1px solid var(--chipline);color:var(--ink);border-radius:999px;padding:4px 10px;font-size:12px;cursor:pointer;user-select:none}
.chip.on{background:var(--accent);color:#fff;border-color:var(--accent)}.chip .c{opacity:.6;margin-left:5px;font-size:10.5px}
.chip.tog.on{background:var(--open);border-color:var(--open)}
.countpill{font-size:12px;color:var(--muted);margin:9px 0 0}
details.qc{margin:12px 0;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:4px 14px}
details.qc summary{cursor:pointer;font-weight:600;padding:7px 0}
table.qct{width:100%;border-collapse:collapse;font-size:12.5px}
table.qct td{padding:5px 8px;border-top:1px solid var(--line);vertical-align:top}
table.qct td:nth-child(2){font-weight:600;white-space:nowrap}
.qcbtn{background:var(--chip);border:1px solid var(--chipline);border-radius:6px;color:var(--accent);font-size:11px;padding:1px 7px;cursor:pointer}
table.main{width:100%;border-collapse:collapse;font-size:13px}
table.main thead th{position:sticky;top:118px;background:var(--bg);text-align:left;padding:8px 8px;border-bottom:2px solid var(--line);font-size:11.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);cursor:pointer;white-space:nowrap;z-index:10}
table.main thead th.nosort{cursor:default}
table.main tbody td{padding:8px 8px;border-bottom:1px solid var(--line);vertical-align:top}
tr.row{cursor:pointer}tr.row:hover{background:var(--rowhover)}
tr.lead .nm{color:var(--muted);font-weight:600}
.exp{color:var(--muted);width:16px;display:inline-block;transition:transform .12s}tr.open .exp{transform:rotate(90deg)}
.nm{font-weight:700}.tag{font-size:10px;padding:1px 6px;border-radius:999px;font-weight:700;margin-left:5px}.tag-new{color:#fff;background:var(--new)}
.badge{font-size:11px;padding:2px 9px;border-radius:999px;font-weight:600;white-space:nowrap;display:inline-block}
.b-open{color:var(--open);background:var(--openbg)}.b-data{color:var(--data);background:var(--databg)}
.b-platform{color:var(--platform);background:var(--platformbg)}.b-lab{color:var(--lab);background:var(--labbg)}
.b-paper{color:var(--paper);background:var(--paperbg)}.b-list{color:var(--list);background:var(--listbg)}
.b-mod{color:var(--muted);background:var(--chip);font-weight:600}
.au{font-size:11px;padding:2px 8px;border-radius:6px;font-weight:700;color:#fff;white-space:nowrap}
.au-A1{background:var(--a1)}.au-A2{background:var(--a2)}.au-A3{background:var(--a3)}.au-A4{background:var(--a4)}.au-A5{background:var(--a5)}.au-B{background:var(--bb)}
td.io{max-width:340px}td.io .t{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted)}
td.dom{max-width:200px}td.dom .t{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td.lnk a{font-size:14px;margin-right:5px}
tr.detailrow td{background:var(--detail);padding:0 8px 14px 30px}
.detail .kv{font-size:12.5px;margin:3px 0}.detail .kv b{color:var(--muted);font-weight:600}
.detail .links a{display:inline-block;font-size:12px;border:1px solid var(--line);padding:3px 9px;border-radius:7px;margin:3px 6px 0 0;background:var(--panel)}
.grouprow td{background:var(--bg);font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);font-weight:700;padding:14px 8px 5px;border-bottom:1px solid var(--line)}
.empty{text-align:center;color:var(--muted);padding:50px 0}
footer{margin-top:30px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:14px}
.legend{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;font-size:11.5px;color:var(--muted)}
.hright{display:flex;flex-direction:column;align-items:flex-end;gap:12px}
.dedi{display:flex;align-items:center;gap:11px;text-decoration:none}
.dedi:hover{text-decoration:none}
.elixir-logo svg{height:50px;width:auto;display:block}
.elixir-logo .cls-2{fill:#4d4848}
.dedi-cap{font-size:12px;line-height:1.35;color:var(--muted);text-align:right}
.dedi-cap b{color:var(--ink);font-weight:700}
.dedi:hover .dedi-cap{color:var(--ink)}
</style></head><body><div class="wrap">
<header class="top"><div class="htext">
<h1>Autonomous Science Agents — Researcher Index</h1>
<div class="sub">A filterable index of AI systems that act as scientific agents: literature, hypothesis, experiment planning, code/simulation execution, lab automation, analysis, and reporting across STEM.
Answer fast: <b>what domain?</b> · <b>in → out?</b> · <b>accessible today?</b> · <b>how autonomous?</b>
Updated __TODAY__. Access tags are best-effort — <b>verify before relying on any system</b>. Rows tagged <b>Paper-only</b> are leads from papers with no confirmed public code. Click a row for detail.</div>
</div>
<div class="hright">
<a class="dedi" href="https://www.elixir-czech.cz/" target="_blank" rel="noopener" title="ELIXIR-CZ — Czech national node of ELIXIR">
<span class="elixir-logo">__ELIXIRSVG__</span>
<span class="dedi-cap">Dedicated to <b>ELIXIR-CZ</b><br>Czech national node of ELIXIR</span></a>
</div></header>
<div class="stats">
<div class="stat"><b>__TOTAL__</b><span>systems &amp; benchmarks</span></div>
<div class="stat"><b>__NOPEN__</b><span>open source</span></div>
<div class="stat"><b>__NLAB__</b><span>physical-lab (A5)</span></div>
<div class="stat"><b>__NBENCH__</b><span>benchmarks</span></div>
<div class="stat"><b>__NCATS__</b><span>domains</span></div>
</div>
<div class="controls">
 <div class="searchrow">
  <input id="q" type="search" placeholder="Search system, domain, in/out…  space = AND  (e.g. single-cell, retrosynthesis, cosmology)">
  <button class="toolbtn sm" id="reset">Reset</button>
 </div>
 <div class="chips" id="catchips"><span class="lbl">Domain</span></div>
 <div class="chips" id="accchips"><span class="lbl">Access</span></div>
 <div class="chips" id="auchips"><span class="lbl">Autonomy</span></div>
 <div class="chips" id="togchips"><span class="lbl">Only</span></div>
 <div class="countpill" id="count"></div>
</div>
<details class="qc"><summary>⚡ Best starting points — by need</summary>
<table class="qct"><tbody>__QUICK__</tbody></table></details>
<table class="main"><thead><tr>
<th class="nosort"></th><th data-k="name">System</th><th data-k="category">Domain</th>
<th data-k="access">Access</th><th data-k="ap">Autonomy</th>
<th class="nosort">Inputs → Outputs</th><th class="nosort">Links</th>
</tr></thead><tbody id="tb"></tbody></table><div id="empty"></div>
<footer><b>__TOTAL__</b> systems &amp; benchmarks across __NCATS__ domains. Autonomy scale: A1 assistant · A2 tool agent · A3 workflow agent · A4 in-silico autonomous scientist · A5 lab/physical autonomous scientist · B benchmark/harness.
A discovery index — verify each system's paper, repo, and access before relying on it.
<div class="legend">
<span><span class="badge b-open">Open source</span> public code</span><span><span class="badge b-data">Open data</span> data/weights</span>
<span><span class="badge b-platform">Platform/API</span> hosted/commercial</span><span><span class="badge b-lab">Lab-gated</span> needs lab/hardware</span>
<span><span class="badge b-paper">Paper-only</span> no confirmed code</span><span><span class="badge b-list">List</span> bibliography</span>
</div></footer></div>
<script>
const DATA=__DATA__;
const CAT_LABELS=__CATLABELS__,CAT_ORDER=__CATORDER__,ACCESS_LABELS=__ACCLABELS__,ACCESS_ORDER=__ACCORDER__,AUTON_LABELS=__AULABELS__,AUTON_ORDER=__AUORDER__;
const BC={'open-source':'b-open','open-data':'b-data','platform':'b-platform','lab-gated':'b-lab','paper-only':'b-paper','list':'b-list'};
const st={q:'',cats:new Set(),accs:new Set(),aus:new Set(),tog:new Set(),sort:'default',dir:1,openset:new Set()};
const esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function counts(f,order){const c={};order.forEach(k=>c[k]=0);DATA.forEach(m=>{if(c[m[f]]!==undefined)c[m[f]]++});return c}
const catC=counts('category',CAT_ORDER),accC=counts('access',ACCESS_ORDER),auC=counts('ap',AUTON_ORDER);
function chips(el,order,labels,cnts,set,cls){order.forEach(k=>{if(cnts&&!cnts[k])return;const d=document.createElement('div');d.className='chip'+(cls||'');d.dataset.k=k;d.innerHTML=labels[k]+(cnts?'<span class="c">'+cnts[k]+'</span>':'');d.onclick=()=>{set.has(k)?set.delete(k):set.add(k);d.classList.toggle('on');render()};el.appendChild(d)})}
chips(document.getElementById('catchips'),CAT_ORDER,CAT_LABELS,catC,st.cats,'');
chips(document.getElementById('accchips'),ACCESS_ORDER,ACCESS_LABELS,accC,st.accs,'');
chips(document.getElementById('auchips'),AUTON_ORDER,AUTON_LABELS,auC,st.aus,'');
chips(document.getElementById('togchips'),['hasRepo'],{hasRepo:'Has repo'},null,st.tog,' tog');
const qEl=document.getElementById('q');
qEl.addEventListener('input',e=>{st.q=e.target.value.toLowerCase();render()});
document.getElementById('reset').onclick=()=>{st.q='';qEl.value='';st.cats.clear();st.accs.clear();st.aus.clear();st.tog.clear();st.sort='default';document.querySelectorAll('.chip.on').forEach(c=>c.classList.remove('on'));render()};
document.querySelectorAll('th[data-k]').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(st.sort===k){st.dir*=-1}else{st.sort=k;st.dir=1}render()});
document.querySelectorAll('.qcbtn').forEach(b=>b.onclick=()=>{st.q=b.dataset.q.toLowerCase();qEl.value=b.dataset.q;render();document.querySelector('table.main').scrollIntoView({behavior:'smooth'})});
function tokens(q){return q.split(/\s+/).filter(Boolean)}
function match(m){if(st.cats.size&&!st.cats.has(m.category))return false;if(st.accs.size&&!st.accs.has(m.access))return false;if(st.aus.size&&!st.aus.has(m.ap))return false;for(const t of st.tog){if(!m[t])return false}for(const tk of tokens(st.q)){if(!m._s.includes(tk))return false}return true}
function links(m,all){let o=[];const ps=m.paper_links||[],cs=m.repo_links||[];if(all){ps.forEach(l=>o.push('<a href="'+l.url+'" target="_blank" rel="noopener">📄 '+esc(l.label)+'</a>'));cs.forEach(l=>o.push('<a href="'+l.url+'" target="_blank" rel="noopener">⚙️ '+esc(l.label)+'</a>'));return o.join('')}if(ps[0])o.push('<a href="'+ps[0].url+'" target="_blank" rel="noopener" title="paper">📄</a>');if(cs[0])o.push('<a href="'+cs[0].url+'" target="_blank" rel="noopener" title="repo">⚙️</a>');return o.join('')}
function rowHtml(m){const bc=BC[m.access]||'b-paper';const open=st.openset.has(m.name);
 let h='<tr class="row'+(open?' open':'')+(m.access==='paper-only'?' lead':'')+'" data-n="'+esc(m.name)+'">'
 +'<td><span class="exp">▸</span></td>'
 +'<td><span class="nm">'+esc(m.name)+'</span></td>'
 +'<td class="dom"><span class="badge b-mod">'+esc(CAT_LABELS[m.category]||m.category)+'</span> <span class="t" title="'+esc(m.domain)+'">'+esc(m.domain)+'</span></td>'
 +'<td><span class="badge '+bc+'" title="'+esc(m.access_raw||'')+'">'+esc(ACCESS_LABELS[m.access]||m.access)+'</span></td>'
 +'<td><span class="au au-'+m.ap+'" title="'+esc(m.autonomy||'')+(m.autonomy&&m.autonomy!==m.ap?' — ':'')+esc(AUTON_LABELS[m.ap]||'')+'">'+m.ap+'</span></td>'
 +'<td class="io"><span class="t">'+esc(m.inputs)+' → '+esc(m.outputs)+'</span></td>'
 +'<td class="lnk">'+links(m,false)+'</td></tr>';
 if(open){h+='<tr class="detailrow"><td colspan="7"><div class="detail">'
  +'<div class="kv"><b>What it does:</b> '+esc(m.notes)+'</div>'
  +'<div class="kv"><b>Inputs:</b> '+esc(m.inputs)+'</div>'
  +'<div class="kv"><b>Outputs:</b> '+esc(m.outputs)+'</div>'
  +'<div class="kv"><b>Autonomy:</b> '+esc(m.autonomy||m.ap)+' &nbsp; <b>Access:</b> '+esc(m.access_raw||ACCESS_LABELS[m.access])+'</div>'
  +'<div class="links">'+links(m,true)+'</div></div></td></tr>';}
 return h}
function render(){let rows=DATA.filter(match);document.getElementById('count').textContent=rows.length+' of '+DATA.length+' shown';
 const tb=document.getElementById('tb'),emp=document.getElementById('empty');
 if(!rows.length){tb.innerHTML='';emp.innerHTML='<div class="empty">No systems match. Clear a filter or the search box.</div>';return}emp.innerHTML='';
 if(st.sort==='default'){rows.sort((a,b)=>(CAT_ORDER.indexOf(a.category)-CAT_ORDER.indexOf(b.category))||(ACCESS_ORDER.indexOf(a.access)-ACCESS_ORDER.indexOf(b.access))||(a.name.toLowerCase()<b.name.toLowerCase()?-1:1));
  let h='',cur=null;rows.forEach(m=>{if(m.category!==cur){cur=m.category;const n=rows.filter(x=>x.category===cur).length;h+='<tr class="grouprow"><td colspan="7">'+esc(CAT_LABELS[cur])+' · '+n+'</td></tr>'}h+=rowHtml(m)});tb.innerHTML=h;
 }else{const k=st.sort;rows.sort((a,b)=>{let r;if(k==='category')r=CAT_ORDER.indexOf(a.category)-CAT_ORDER.indexOf(b.category);else if(k==='access')r=ACCESS_ORDER.indexOf(a.access)-ACCESS_ORDER.indexOf(b.access);else if(k==='ap')r=AUTON_ORDER.indexOf(a.ap)-AUTON_ORDER.indexOf(b.ap);else r=a.name.toLowerCase()<b.name.toLowerCase()?-1:1;return r*st.dir||(a.name.toLowerCase()<b.name.toLowerCase()?-1:1)});tb.innerHTML=rows.map(rowHtml).join('');}
 tb.querySelectorAll('tr.row').forEach(tr=>tr.onclick=e=>{if(e.target.tagName==='A')return;const n=tr.dataset.n;st.openset.has(n)?st.openset.delete(n):st.openset.add(n);render()});}
render();
</script></body></html>"""

try:
    _elixir_svg = open('assets/elixir-cz-logo.svg').read()
    if _elixir_svg.lstrip().startswith('<?xml'):
        _elixir_svg = _elixir_svg.split('?>', 1)[1]
except FileNotFoundError:
    _elixir_svg = ''

repl = {
    '__TODAY__': today, '__TOTAL__': str(total), '__NOPEN__': str(n_open), '__NLAB__': str(n_lab),
    '__NBENCH__': str(n_bench), '__NCATS__': str(n_cats), '__QUICK__': quick_rows,
    '__DATA__': json.dumps(norm, ensure_ascii=False), '__CATLABELS__': json.dumps(CAT_LABELS),
    '__CATORDER__': json.dumps(CAT_ORDER), '__ACCLABELS__': json.dumps(ACCESS_LABELS),
    '__ACCORDER__': json.dumps(ACCESS_ORDER), '__AULABELS__': json.dumps(AUTON_LABELS),
    '__AUORDER__': json.dumps(AUTON_ORDER),
    '__ELIXIRSVG__': _elixir_svg,
}
out = TEMPLATE
for k, v in repl.items():
    out = out.replace(k, v)
open(OUT, 'w').write(out)
print(f"Wrote {OUT}  ({total} systems, {n_new} new, {n_open} open-source)")
print("category:", dict(Counter(m['category'] for m in norm)))
print("access:", dict(acc_c)); print("autonomy primary:", dict(ap_c))
