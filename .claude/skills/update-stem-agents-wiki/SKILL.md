---
name: update-stem-agents-wiki
description: Find autonomous AI science agents / self-driving labs / agent benchmarks not yet in the wiki, verify them, add them to agents_final.json, rebuild the site, and push. Use when asked to update, grow, maintain, refresh, or re-sweep the autonomous science agents wiki, add new agents/systems, fix entries, or keep the repo current and live.
---

# Update the Autonomous Science Agents Wiki

Keep this repo (`MichaLie/autonomous-stem-agents-wiki`, working dir `~/Desktop/wiki/Autonomous_Agents`) **complete, correct, and live**. Two modes: **quick add** (a few known systems) and **full re-sweep** (comprehensive periodic refresh). Read `CLAUDE.md` first — it has the schema, the autonomy/access taxonomies, and build/deploy commands.

## 0. Orient
- Read `CLAUDE.md`; load `agents_final.json`.
- Build the set of existing names + aliases, normalized (lowercase, strip punctuation/parens). Check every candidate against it — and watch for same-name/different-system collisions (e.g. two MARS, two ChemAgent).

## 1. Discover — find what's missing
Search per domain for autonomous science agents / self-driving labs / agent benchmarks MISSING from the wiki. A qualifying system does multi-step scientific work (literature, hypothesis, experiment/simulation planning, code execution, lab automation, analysis, reporting) OR is a benchmark/harness for such agents.
- Domains: cross-domain general scientists, biology/medicine, chemistry/materials (incl. self-driving labs), physics/astronomy/engineering/simulation, benchmarks.
- Prioritize WELL-KNOWN / impactful / verifiable systems and 2024–2026 releases. Do not pad with obscure unverifiable paper-only entries.
- **Full re-sweep:** use the **Workflow tool** (multi-agent) — fan out by domain to find missing systems, then a separate adversarial verification stage. This is the pattern that built the wiki.

## 2. Verify — adversarial, MANDATORY (this catalog must be trustworthy)
For each candidate use WebSearch/WebFetch (load via ToolSearch):
1. Confirm the system is REAL — the cited paper/page exists, the arXiv/DOI **resolves**, the title matches, and the paper is **not withdrawn**. (Past audits caught fabricated ChemRxiv DOIs and withdrawn arXiv papers.)
2. Confirm the repo/platform link resolves and belongs to it; correct it or set it empty.
3. Confirm it's genuinely an autonomous science agent / self-driving lab / agent benchmark, and not already in the wiki.
4. Default to **drop** when the ID doesn't resolve / is withdrawn / no repo or page is found. Never publish an unverified system as runnable.

## 3. Classify
- `category` ∈ crossdomain / biology / chemistry / physics / benchmark.
- `access` ∈ open-source / open-data / platform / lab-gated / paper-only / list (see CLAUDE.md mapping).
- `autonomy` on the A1–A5 / B scale (range allowed). Lab/robotic systems = A5; pure evaluation suites = B.

## 4. Write entries
- Append each verified system to `agents_final.json` per the schema in `CLAUDE.md`.
- Build `paper_links` / `repo_links` from verified URLs only, with short labels (arXiv, bioRxiv, Nature, GitHub, Hugging Face…).
- Dedupe by normalized name. No "new" tags / audit framing — the public site stays clean.

## 5. Rebuild, validate, publish
```bash
python3 build_html.py agents_final.json docs/index.html
python3 build_html.py agents_final.json autonomous_stem_agents_wiki.html
python3 build_md.py
```
- Validate: `agents_final.json` parses; every record has name/category/domain; sanity-check per-domain counts.
- Confirm it renders; commit with a clean message; push; **poll the live URL** until it serves the new content.

## 6. Maintenance — keep it alive
- Re-verify links periodically; drop systems whose papers were withdrawn; upgrade `access` when paper-only systems release code.
- Add genuinely-missing canonical systems as the field moves (weekly).

## Guardrails
Only real, verified systems — confirm the paper resolves, matches, and isn't withdrawn before adding. Verified links only. Clean public copy (no internal notes, no NEW tags). Paper-only rows are honest "unverified leads," not runnable tools. `agents_final.json` is the only file you edit by hand.
