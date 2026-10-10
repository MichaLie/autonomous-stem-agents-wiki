# Autonomous Science Agents discovery audit — 2026-10-10

## Local preview and result

This is an unpublished **2.3.0 preview** on branch `agent/v2.3.0-2026-10-refresh`, derived from commit `2a9298a` (full SHA in `refresh-2026-10-10/decisions.json`). `release_ref` remains null. No push, release, tag or remote write was performed.

- Baseline: 458 records.
- Added: 82 systems and benchmarks (66 from discovery, 16 promoted from earlier held leads).
- Restored under their reserved IDs: Periodic Labs and FARS.
- Corrected existing records: 76, most of them access labels after a licence check.
- Current catalog: **542 records**: 88 cross-domain, 121 biology, 93 chemistry, 106 physics and 134 benchmarks.

New and restored records carry `verified: 2026-10-10`. Corrected records carry `date_modified: 2026-10-10` and keep their earlier verification dates, because a targeted licence or claim check is not a complete re-verification.

## Method

Five discovery lanes ran independently: cross-domain systems, benchmarks/harnesses, biology/medicine, chemistry/materials, and physics/engineering/mathematics. Each lane searched the arXiv API by submission date (main window 2026-09-11 to 2026-10-10, with a second sweep of 2026-08-13 to 2026-09-11 for misses), GitHub, and a small number of web searches. The biology lane also searched the bioRxiv and medRxiv APIs. Lanes reported about 23,000 screened metadata records in total. That figure counts screened titles and abstracts, which overlap across queries; it is not the number of distinct papers. All 54 held leads from earlier cycles were re-reviewed in 11 batches against their recorded conditions.

Every proposed addition, promotion and restoration then went to a separate agent instructed to refute it. That agent re-fetched the primary sources and checked identity, scope, observed autonomy, licence and access, category, every URL and the wording. Of 90 such reviews, 84 confirmed the proposal (82 with corrections, which were applied) and 6 sent it back to hold. A refuted proposal was never admitted.

Decisions, rationales, claim sources, and both the proposing and the reviewing agent's URL-level evidence (HTTP status, access level, short excerpts) are in [`refresh-2026-10-10/decisions.json`](refresh-2026-10-10/decisions.json). No system was executed. Every judgement rests on reading papers, repositories, licence files and documentation.

## Licence check of every open-source record

The `open-source` label requires a confirmed software licence. A mechanical sweep queried the GitHub licence API for all 262 records then labelled open-source. It flagged 80: 51 repositories without a detected licence file, 26 with a licence GitHub could not identify, 2 without a GitHub repository and 1 whose repository no longer exists. Because monorepos keep licences in subfolders and some licences are custom, a separate agent checked each flagged record (together with five records whose lanes had proposed other corrections).

Outcome: 58 records move from `open-source` to `source-available` (no licence text, a README-only declaration, or non-commercial or custom terms). Three move to `paper-only` because their code is no longer public. Two move to `open-data` because their main artifact is a dataset under a content licence. The others keep `open-source` with licence evidence recorded. Where a README declares a licence without licence text, the record follows the September SCTA precedent (`source-available` with `access_evidence`). These relabels describe today's repository state, not the authors' intent; a record returns to `open-source` once a licence file appears.

## Other corrections and reclassifications

- **InternAgent (formerly NovelSeek):** A4–A5 → A4. All twelve reported tasks are computational; no physical loop is reported.
- **OpenClaw / Claw AI Lab / LabClaw:** benchmark (B) → cross-domain A4. The cited paper and repository describe a multi-agent research platform, not an evaluation harness.
- **Lila Sciences:** A5 kept. The earlier label rested on a press release, the weakness that put Periodic Labs on hold in September. A first-party September 2026 preprint now describes an AI-guided, human-supervised closed loop for oxygen-evolution catalysts, with its human steps disclosed in the record.
- Paper versions, moved repositories and wording corrections are listed per record in `decisions.json`.

## Restorations

- **Periodic Labs** (`asa-periodic-labs`): restored as lab-gated, A2–A3. First-party technical posts dated 2026-09-15 describe a concrete system (the Periodic Neon model in the Periodic Harness, used to analyse XRD results in the company's labs). They do not demonstrate an autonomous physical loop, so the earlier A5 label is not restored.
- **FARS** (`asa-fars`): restored as open-data, A4. The original site is still unreachable. Three live first-party sources document the system and its released outputs: an arXiv paper by the Analemma team, a Hugging Face review dataset and a GitLab group of per-project artifacts. All three predate the August removal; the August search missed them. The tombstone rested on the absence of any live official source, which no longer holds.

Both tombstones were removed from `deprecated_ids.json`; the original `date_added` values are kept.

## Held and rejected candidates

- 220 holds: 190 new discovery leads plus 30 earlier leads whose conditions are still unmet. Typical reasons are a missing or unlicensed release, an inaccessible full text, or unresolved scope. Holds are leads, not claims that a system or paper is flawed.
- Six proposals were sent back to hold by their reviewing agent: FUSION (scope contested), OpenDiscoveryTrace (public release out of sync with the paper), BioSecBench-Surveillance (data and graders not released), MetagenomicsBench, RepurAgent and APOD (no licence file).
- 73 scope rejections, including six earlier leads: Avatar (workflow-management reference architecture), HyGRAIL (link-prediction method), MACROS (modality-specific generative models rather than agents), a formal laboratory-representation framework, a single crystal-plausibility campaign, and Sakana Marlin (a business-strategy research product, now settled on its official pages).
- Seven candidates matched existing records and were not duplicated. AutoMat (the Johns Hopkins reproduction benchmark) is a different system from the existing AutoMat microscopy pipeline; it was added under a disambiguated name without the bare alias.

## Coverage limits

This is a broad discovery refresh with adversarial verification of every admission. It is **not an exhaustive systematic review**. Specific limits:

- Several arXiv API queries returned HTTP 429 under shared load. Affected lanes fell back to arXiv web search (title-level) and to the September identifier inventory, so misses in the 2026-08-13 to 2026-09-11 window remain possible.
- Web search was rationed across all agents; company announcements were sampled, not enumerated.
- The benchmark lane did not search bioRxiv/medRxiv or PubMed. The biology lane did.
- Only flagged existing records were re-checked. The other 373 baseline records were not re-verified in this cycle.

## Local checks

- The dated migration (`scripts/apply_2026_10_10_refresh.py`) is idempotent: a second run left the catalog and tombstones byte-identical.
- `build.py`: 14 generated artifacts byte-stable. `validate_catalog.py`: pass (one expected warning, null release reference). `git diff --check`: clean.
- Full URL audit: 1,316 unique URLs across 2,369 occurrences. 2,219 occurrences reachable and 63 restricted (publisher bot blocks, not verification). 85 occurrences are GitHub file pages that returned 503 under burst load; the authenticated GitHub contents API confirmed every one of those files exists. One Zenodo DOI (two occurrences) timed out; the Zenodo REST API confirmed the record. Details: [`refresh-2026-10-10/link_recheck.json`](refresh-2026-10-10/link_recheck.json).
- `validate_catalog.py --release` is expected to fail only on the null release reference. Governance was not weakened.

Publication remains a separate step that needs the owner's explicit approval.
