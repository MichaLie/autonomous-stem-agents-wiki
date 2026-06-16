#!/usr/bin/env python3
"""Merge existing + verified-new autonomous-agent entries into agents_final.json.
Applies existing-entry verdicts (drop/fix/confirm) and adds verified new agents."""
import json, re

existing = json.load(open('agents_existing.json'))
ver = json.load(open('wf_result.json'))['verify']          # existing-entry verdicts
try:
    vnew = json.load(open('wf_verify_new.json'))['results']  # new-candidate verdicts
except FileNotFoundError:
    vnew = []
    print("WARN: wf_verify_new.json not found — merging existing only")

def nk(n): return re.sub(r'[^a-z0-9]', '', re.sub(r'\(.*?\)', '', n.lower()))

def url_label(u):
    d = (u or '').lower()
    for k, lab in [('arxiv', 'arXiv'), ('biorxiv', 'bioRxiv'), ('medrxiv', 'medRxiv'), ('chemrxiv', 'ChemRxiv'),
                   ('nature.com', 'Nature'), ('science.org', 'Science'), ('pubs.acs', 'ACS'), ('pubs.rsc', 'RSC'),
                   ('openreview', 'OpenReview'), ('aclanthology', 'ACL'), ('mlr.press', 'PMLR'), ('pmc.ncbi', 'PMC'),
                   ('pubmed', 'PubMed'), ('huggingface', 'Hugging Face'), ('github.com', 'GitHub'),
                   ('zenodo', 'Zenodo'), ('inspirehep', 'INSPIRE'), ('figshare', 'figshare')]:
        if k in d:
            return lab
    return 'Link'

def mklinks(url):
    url = (url or '').strip()
    if not url.lower().startswith('http'):
        return []
    return [{'label': url_label(url), 'url': url}]

def norm_access(a):
    a = (a or '').lower()
    if a in ('open-source', 'open-data', 'platform', 'lab-gated', 'paper-only', 'list'):
        return a
    if 'list' in a: return 'list'
    if 'lab' in a or 'institution' in a or 'hardware' in a or 'robot' in a: return 'lab-gated'
    if 'paper' in a or 'unclear' in a or 'concept' in a: return 'paper-only'
    if 'platform' in a or 'api' in a or 'commercial' in a or 'enterprise' in a or 'closed' in a: return 'platform'
    if 'data' in a or 'weights' in a or 'benchmark' in a: return 'open-data'
    if 'open' in a: return 'open-source'
    return 'paper-only'

vmap = {nk(r['name']): r for r in ver}
DROP = {nk(r['name']) for r in ver if r['verdict'] == 'drop'}

out = []
counts = {'kept': 0, 'dropped': 0, 'fixed': 0, 'unverified_kept': 0}
for e in existing:
    k = nk(e['name'])
    if k in DROP:
        counts['dropped'] += 1
        continue
    v = vmap.get(k)
    rec = dict(e)
    rec['new'] = False
    if v:
        rec['access'] = norm_access(v.get('access', e.get('access', '')))
        rec['autonomy'] = v.get('autonomy', e.get('autonomy', ''))
        rec['inputs'] = v.get('inputs') or e.get('inputs', '')
        rec['outputs'] = v.get('outputs') or e.get('outputs', '')
        rec['notes'] = v.get('notes') or e.get('notes', '')
        rec['paper_links'] = mklinks(v.get('paper_url')) or e.get('paper_links', [])
        rec['repo_links'] = mklinks(v.get('repo_url'))   # empty if not verified
        if v['verdict'] == 'fix':
            counts['fixed'] += 1
        else:
            counts['kept'] += 1
    else:
        rec['access'] = norm_access(e.get('access', ''))
        counts['unverified_kept'] += 1
    out.append(rec)

# add verified-new
exk = {nk(r['name']) for r in out}
seen = set(exk)
added = {'confirmed': 0, 'fix': 0, 'dropped': 0, 'already': 0}
for c in vnew:
    vd = c['verdict']
    if vd in ('drop',):
        added['dropped'] += 1; continue
    if vd == 'already-covered':
        added['already'] += 1; continue
    k = nk(c['name'])
    if k in seen:
        added['already'] += 1; continue
    seen.add(k)
    out.append({
        'name': c['name'], 'category': c.get('category', 'crossdomain'), 'domain': c.get('domain', ''),
        'access': norm_access(c.get('access', '')), 'autonomy': c.get('autonomy', ''),
        'inputs': c.get('inputs', ''), 'outputs': c.get('outputs', ''), 'notes': c.get('notes', ''),
        'paper_links': mklinks(c.get('paper_url')), 'repo_links': mklinks(c.get('repo_url')),
        'new': True,
    })
    added['confirmed' if vd == 'confirmed' else 'fix'] += 1

json.dump(out, open('agents_final.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print("existing:", counts)
print("new:", added)
print("TOTAL:", len(out))
print("by category:", dict(Counter(r['category'] for r in out)))
print("by access:", dict(Counter(r['access'] for r in out)))
