# Autonomous Science Agents — Researcher Index

A filterable, public index of AI systems that act as scientific agents across STEM — literature, hypothesis, experiment/simulation planning, code execution, lab automation, analysis, reporting — plus the benchmarks that evaluate them. For each system: what domain, what goes in/out, how accessible it is, and **how autonomous** (A1 assistant → A5 physical-lab scientist).

**Live site:** https://michalie.github.io/autonomous-stem-agents-wiki/

321 systems across 5 domains (cross-domain, biology/medicine, chemistry/materials, physics/astronomy/eng., benchmarks). Rows tagged **Paper-only** are leads from papers with no confirmed public code — verify before relying on any system.

---

## How to update it

**`agents_final.json` is the single source of truth. Edit it, rebuild, push — the live site (served from `docs/`) updates.** Never hand-edit the `.html`/`.md` — they are generated.

### Option A — let an agent do it (your default)
Point Claude/Codex at this repo:
- **Add one system:** "Add `<name>` to `agents_final.json` (category, access, autonomy, links, in/out) after verifying its paper+repo resolve, then `python3 build_html.py agents_final.json docs/index.html`, commit and push."
- **Re-sweep the field:** re-run the discovery + adversarial-verification workflow, merge into `agents_final.json`, rebuild into `docs/`, commit, push.

### Option B — dump it in an Issue
Open a new Issue with the **"Add / fix an agent"** template; you or an agent turns it into a JSON entry.

### Option C — local
```bash
python3 build_html.py agents_final.json docs/index.html
python3 build_md.py
git commit -am "update agents" && git push
```

### Optional upgrade — browser-only editing
To edit `agents_final.json` in GitHub's web editor and have the site rebuild itself, grant the workflow scope once and enable the bundled Action:
```bash
~/.local/bin/gh auth refresh -h github.com -s workflow
mkdir -p .github/workflows && mv optional-github-action.yml .github/workflows/deploy.yml
# then Settings → Pages → Source = GitHub Actions, and push.
```

---

## Taxonomies

**Autonomy:** A1 assistant · A2 tool agent · A3 workflow agent · A4 in-silico autonomous scientist · A5 lab/physical autonomous scientist · B benchmark/harness.
**Access:** open-source · open-data · platform/API · lab-gated · paper-only · list.

## What's in here

| File | Role |
| --- | --- |
| `agents_final.json` | **Source of truth** — the catalog data |
| `build_html.py` | Generates the interactive HTML site |
| `build_md.py` | Generates the Markdown version |
| `merge_agents.py` | How the audit's existing + verified-new entries were combined (re-sweep reference) |
| `docs/` | The published site (Pages serves `docs/index.html`) |
| `optional-github-action.yml` | Opt-in auto-build Action (see upgrade above) |
| `CLAUDE.md` | Operating guide for AI agents maintaining this repo |

## Caveats

Access tags reflect code/availability, not license terms or operational/clinical approval. Autonomous outputs are leads, not results — validate with orthogonal methods and domain experts. A1–A5 physical-lab systems require institutional safety review before any real-world use.
