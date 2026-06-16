# CLAUDE.md — Autonomous Science Agents Wiki

Operating guide for any Claude/Codex instance working in this repo. **Read this first.**

## What this is
A public, filterable index of AI systems that act as scientific agents across STEM — literature, hypothesis, experiment/simulation planning, code execution, lab automation, analysis, reporting — plus the benchmarks that evaluate them.

- **Live site:** https://michalie.github.io/autonomous-stem-agents-wiki/
- **Repo:** https://github.com/MichaLie/autonomous-stem-agents-wiki
- **Scope:** 321 systems across 5 domains (cross-domain, biology, chemistry/materials, physics/astronomy/eng., benchmarks).
- **Owner:** Michaela (GitHub: `MichaLie`).

## Golden rules
1. **`agents_final.json` is the only source of truth.** Edit it. **Never** hand-edit the generated `.html` / `.md`.
2. **Always rebuild after editing data, then push.** Pages serves `docs/`, so a rebuilt `docs/index.html` must be committed.
3. **Keep the public site clean.** No "NEW" tags, no audit/process framing, no "Second-Pass Audit Register" — the public page is one clean catalog per domain. Do not reintroduce internal notes.
4. **Verify every entry. This catalog must be trustworthy.** Prior audits found fabricated DOIs and *withdrawn* arXiv papers presented as real. Never add a system whose paper/repo you have not confirmed resolves and matches. If you can't confirm, mark it `paper-only` (a visible "unverified lead") or drop it.
5. **Don't commit the local-only provenance** (`agents_existing.json`, `wf_*.json`, `_*.json`) — gitignored, kept on Michaela's machine.

## Build & deploy
```bash
python3 build_html.py agents_final.json docs/index.html                       # the PUBLISHED site
python3 build_html.py agents_final.json autonomous_stem_agents_wiki.html       # downloadable copy
python3 build_md.py                                                            # markdown copy
git add -A && git commit -m "update agents" && git push
```
Python 3 only, no dependencies. Pages = GitHub Pages from `main:/docs` (branch deploy, not an Action — token lacks `workflow` scope; the unused Action sits in `optional-github-action.yml`). On Michaela's machine `gh` is at `~/.local/bin/gh`, authed as `MichaLie`. After pushing, Pages redeploys in ~1–2 min — verify by curling the live URL.

## Data schema (one record in `agents_final.json`)
```json
{ "name": "A-Lab (Berkeley)", "category": "chemistry",
  "domain": "Autonomous inorganic-materials synthesis",
  "access": "lab-gated", "autonomy": "A5",
  "inputs": "Target compositions from Materials Project",
  "outputs": "Robotic synthesis recipes, XRD-characterized products",
  "notes": "Closed-loop robotic lab; synthesized 41 of 58 targets in 17 days.",
  "paper_links": [{"label":"Nature","url":"https://..."}],
  "repo_links":  [{"label":"GitHub","url":"https://..."}],
  "new": false }
```
- `category` ∈ `crossdomain biology chemistry physics benchmark` (the domain facet).
- `access` ∈ `open-source open-data platform lab-gated paper-only list` (the build colour-codes these).
- `autonomy`: the A1–A5 / B scale, range allowed (e.g. `A3-A4`). The build derives the primary level (max A, else B) for the badge + filter. **A1** assistant · **A2** tool agent · **A3** workflow agent · **A4** in-silico autonomous scientist · **A5** lab/physical autonomous scientist · **B** benchmark/harness.
- `repo_links`: include **only verified** repos. A missing repo is honest signal, not a gap to fill with a guess.

## Adding or maintaining agents
Use the skill **`update-stem-agents-wiki`** (`.claude/skills/update-stem-agents-wiki/SKILL.md`). In short: discover → adversarially verify (paper resolves + matches, repo exists, not withdrawn/duplicate) → classify (domain, access, autonomy) → append to `agents_final.json` → rebuild → push.

## Keeping it alive
- **Periodic re-sweep** — agentic science moves weekly. The skill covers a quick add and a full multi-agent sweep + verification.
- **Maintenance:** re-verify links, upgrade `access` when paper-only systems release code, drop systems whose papers get withdrawn, prune duplicates (watch for same-name-different-system collisions, e.g. two MARS, two ChemAgent).
