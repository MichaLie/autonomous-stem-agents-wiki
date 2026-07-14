#!/usr/bin/env python3
"""Regenerate the clean markdown wiki from agents_final.json."""
import json
from collections import Counter
from pathlib import Path
M = json.load(open('agents_final.json'))
resource_meta = json.load(open('resource_metadata.json'))

CAT_TITLE = {
    'crossdomain': 'Cross-Domain Scientific Agents', 'biology': 'Biology and Medicine',
    'chemistry': 'Chemistry, Materials, and Molecular Discovery',
    'physics': 'Physics, Astronomy, Engineering, and Simulation',
    'benchmark': 'Benchmarks, Harnesses, and Infrastructure',
}
CAT_ORDER = ['crossdomain', 'biology', 'chemistry', 'physics', 'benchmark']
ACC_RANK = {'open-source': 0, 'source-available': 1, 'open-data': 2, 'platform': 3, 'lab-gated': 4, 'paper-only': 5, 'list': 6}
ACC_LABEL = {'open-source': 'Open source', 'source-available': 'Source available', 'open-data': 'Open data', 'platform': 'Platform/API',
             'lab-gated': 'Lab-gated', 'paper-only': 'Paper-only', 'list': 'List'}

def links_md(rec):
    out = [f"[{l['label']}]({l['url']})" for l in rec.get('paper_links', [])]
    out += [f"[{l['label']}]({l['url']})" for l in rec.get('repo_links', [])]
    return ' · '.join(out) if out else '—'

def cell(s): return (s or '').replace('|', '\\|').replace('\n', ' ').strip()

today = resource_meta['modified']
o = []
o.append('# Autonomous AI Researchers and Scientific Agents for STEM')
o.append('')
o.append(f'Last full sweep: {today}  ·  {len(M)} systems across {len(CAT_ORDER)} domains.')
o.append('')
o.append('A catalog of AI systems that act as scientific agents: literature search, hypothesis generation, '
         'experiment/simulation planning, code execution, lab automation, data analysis, and reporting across '
         'STEM. Practical triage for researchers: what exists, what it is for, whether it is accessible, what '
         'goes in, what comes out, and how autonomous it is. An interactive filterable version is in '
         '`autonomous_stem_agents_wiki.html` (open in any browser, works offline).')
o.append('')
o.append('Rows tagged **Paper-only** are leads from papers/preprints with no confirmed public implementation — '
         'treat as leads, not runnable tools. Always verify a system before relying on it.')
o.append('')
o.append('## Autonomy Scale')
o.append('')
o.append('| Level | Meaning |')
o.append('| --- | --- |')
for lv, mng in [('A1', 'Assistant — helps with retrieval/drafting/local reasoning; human is primary operator.'),
                ('A2', 'Tool agent — chooses and calls tools for a bounded task.'),
                ('A3', 'Workflow agent — executes multiple research stages, usually with checkpoints.'),
                ('A4', 'In-silico autonomous scientist — loops idea → code/simulation → analysis → report.'),
                ('A5', 'Lab/physical autonomous scientist — plans and triggers physical/robotic experiments.'),
                ('B', 'Benchmark/harness — evaluates or hosts agents rather than doing science itself.')]:
    o.append(f'| {lv} | {mng} |')
o.append('')
o.append('## Access Labels')
o.append('')
o.append('| Label | Meaning |')
o.append('| --- | --- |')
for lab, mng in [('Open source', 'Public code/package (may still need paid LLM/API keys).'),
                 ('Source available', 'Public source with reuse restrictions; not OSI open source.'),
                 ('Open data', 'Weights/datasets/benchmark data public, not necessarily a full agent stack.'),
                 ('Platform/API', 'Hosted service, API, commercial, or enterprise account.'),
                 ('Lab-gated', 'Needs robotic lab, institutional infrastructure, or special hardware.'),
                 ('Paper-only', 'Paper/preprint exists; no usable public implementation confirmed.'),
                 ('List', 'Curated bibliography / awesome-list, not a single system.')]:
    o.append(f'| {lab} | {mng} |')
o.append('')
o.append('## Contents')
o.append('')
c = Counter(r['category'] for r in M)
for cat in CAT_ORDER:
    o.append(f"- {CAT_TITLE[cat]} — {c.get(cat,0)}")
o.append('')

for cat in CAT_ORDER:
    items = [r for r in M if r['category'] == cat]
    if not items:
        continue
    items.sort(key=lambda r: (ACC_RANK.get(r['access'], 9), r['name'].lower()))
    o.append(f'## {CAT_TITLE[cat]}')
    o.append('')
    o.append('Sorted: most-accessible first, then by name.')
    o.append('')
    o.append('| System | Domain / area | Access | Autonomy | Inputs → Outputs | Links | Notes |')
    o.append('| --- | --- | --- | --- | --- | --- | --- |')
    for r in items:
        io = cell(r.get('inputs', '')) + ' → ' + cell(r.get('outputs', ''))
        o.append('| {nm} | {dom} | {acc} | {au} | {io} | {lnk} | {notes} |'.format(
            nm=cell(r['name']),
            dom=cell(r.get('domain', '')), acc=ACC_LABEL.get(r['access'], r['access']),
            au=cell(r.get('autonomy', '')), io=io, lnk=links_md(r), notes=cell(r.get('notes', ''))))
    o.append('')

o.append('## Practical Operation Patterns')
o.append('')
o.append('- **Literature/evidence agents** (PaperQA2, Elicit, Consensus, STORM, Asta): give a question + corpus/web '
         'access; get cited answers, reviews, contradiction checks. Verify citations — grounding varies.')
o.append('- **Code/data-analysis agents** (Biomni, CellVoyager, AutoBA, cmbagent): give data + a task; get executed '
         'notebooks, figures, and interpretation. Check the code and re-run; treat conclusions as hypotheses.')
o.append('- **Hypothesis-to-experiment agents** (AI Co-Scientist, Robin, BioDiscoveryAgent, Coscientist): give an '
         'objective; get ranked hypotheses, designs, and (for A5 lab systems) executed experiments. Human review and '
         'safety gates are essential before wet-lab action.')
o.append('- **Benchmarks/harnesses** (ScienceAgentBench, MLE-bench, AstaBench, SciCode): use to judge whether a '
         'system actually works on your task class before adopting it.')
o.append('')
o.append('## Safety and Reproducibility Notes')
o.append('')
o.append('- Lab/physical (A5) systems can trigger real experiments — they require institutional safety review, '
         'biosafety/chemical-safety gates, and human oversight; none are turnkey.')
o.append('- Autonomous outputs (hypotheses, designs, code) are leads, not results — validate with orthogonal '
         'methods and domain experts before acting.')
o.append('- Access tags reflect code/availability, not license terms or clinical/operational approval. Confirm '
         'licenses and intended-use restrictions before any real-world use.')
o.append('- Catalog data, metadata, and original documentation are CC BY 4.0; maintenance/build code is MIT. External resources and logos retain their own terms.')
o.append('')

rendered = '\n'.join(o).rstrip() + '\n'
Path('autonomous_stem_agents_wiki.md').write_text(rendered, encoding='utf-8')
Path('docs').mkdir(exist_ok=True)
Path('docs/autonomous_stem_agents_wiki.md').write_text(rendered, encoding='utf-8')
print('Wrote autonomous_stem_agents_wiki.md —', len(M), 'systems')
print('per domain:', dict(c))
