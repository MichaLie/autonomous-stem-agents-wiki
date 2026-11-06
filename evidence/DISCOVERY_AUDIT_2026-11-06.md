# Autonomous Science Agents discovery audit — 2026-11-06

## Local preview and result

This is an unpublished **2.4.0 preview** on branch `agent/v2.4.0-2026-11-refresh`, derived from commit `46d0937` (the published 2.3.0 release; full SHA in `refresh-2026-11-06/decisions.json`). `release_ref` remains null. No push, release, tag or remote write was performed.

- Baseline: 542 records.
- Added: 68 systems and benchmarks (42 from discovery, 26 promoted from October's held leads).
- Corrected existing records: 17.
- Current catalog: **610 records**: 92 cross-domain, 138 biology, 105 chemistry, 125 physics and 150 benchmarks.

| Category | Added this cycle |
|---|---|
| Benchmarks (16) | Agent4Sci, Autonomous Science Bench, BioDesignBench, BioLitBench, BioXArena, CompMat-Bench, DISCERN, HEPTABench, Into the Unknown, Neurodata Without Boredom, OmicsBench, PaperBenchX, PhysClosureBench, RIDAR, SlowLab, WorldSolver |
| Biology (17) | Brieflow-auto, CellCanon, Chaperone, CryoPilot, DeepMAST, DiscoveryRSI, EMET, Findings Workflow, GENIE (paper-only), a genetic-disease severity classification agent, LPT, LabWeaver, Morpheus.AI, PEN-STACK, PRAXIS-VirtualCell, PaleoRigor, TrialAtlas |
| Chemistry (12) | AutoXRD, BEAVER, Gan Jiang, IRIS, MADDIE, MARS, Magnolia, MatEvolve, MatOS, MiMEDAL (lab-gated), SciKGExtract, ThermoML Agents |
| Cross-domain (4) | AfS (Agent for Science), IdeaScientist, SplatLab, The Agentic Scientist |
| Physics, engineering, maths (19) | Auctopus, AutoSR, Brilliance, CFD Forge, Euler, FUSION, GBClaw, HERA, Haiqu AgenticOS (QAOS), MOSAIC, a metasurface agent pipeline, PTagent, PhysKit, QMatSuite, QUANTA (paper-only), Qiushi Engine, QuantumMatterExplorer, SRHarness, Simjecture |

Access of the additions: 48 open-source (licence text confirmed), 11 source-available, 4 platform, 2 open-data, 2 paper-only, 1 lab-gated. Seven claim a physical loop: Auctopus, HERA, QUANTA and Qiushi Engine at A5; GENIE and MiMEDAL at A4–A5; PhysKit at A3–A5 (one of its six case studies ran a spectrometer unattended). Each A5 rests on closure reported in the paper, with human gates stated in the notes. The two paper-only additions (GENIE, QUANTA) both drove laboratory instruments in a closed loop, which is the bar for admitting paper-only systems.

New records carry `verified: 2026-11-06`. Corrected records carry `date_modified: 2026-11-06` and keep their earlier verification dates, because a targeted check is not a complete re-verification.

## Method

Five discovery lanes ran independently: cross-domain systems, benchmarks/harnesses, biology/medicine, chemistry/materials, and physics/engineering/mathematics. The main window was 2026-10-10 to 2026-11-06, with a second sweep back to 2026-09-11. Channels were the arXiv API, arXiv listing and advanced-search pages, Europe PMC (including bioRxiv, medRxiv and ChemRxiv preprints), the bioRxiv API, GitHub and a small number of web searches. Lanes reported about 20,000 screened metadata records; queries overlap, so this is not the number of distinct papers. Each lane checked candidates against a baseline of the 542 records and October's 220 held leads.

All 220 held leads from October were re-reviewed in 28 batches against their recorded conditions: 28 proposed for promotion, 176 kept on hold, 15 rejected on scope, 1 matched an existing record.

Every proposed addition and promotion went to a separate agent instructed to refute it. It re-fetched the primary sources and checked identity (including withdrawal notices and same-name collisions), scope, observed autonomy, licence and access, category, every URL and the wording. Of 71 such reviews, 69 confirmed the proposal (61 with corrections, which were applied) and 2 sent it back to hold. The orchestrator held one more confirmed proposal (PharmAgents2): it is paper-only and the agent did not itself close a physical loop. A refuted proposal was never admitted.

The refuters were tested with four planted known-bad proposals taken from October's own decisions: a general deep-research report writer, a foundation agentic model, a system whose arXiv paper carries a withdrawal notice, and a simulation-only design agent presented as A5 with fabricated devices. All four were caught (three rejected, one sent back to hold). They are not in any payload. The test shows the refuters catch clear errors; it does not measure subtle ones.

After review, every arXiv and bioRxiv identifier and every GitHub repository cited by an addition was resolved again at the source by a script; all resolve and the titles match.

Decisions, rationales, claim sources, and the proposing and reviewing agents' URL-level evidence are in [`refresh-2026-11-06/decisions.json`](refresh-2026-11-06/decisions.json). No system was executed. Every judgement rests on reading papers, repositories, licence files and documentation.

## Licence check

The GitHub licence API was queried for every repository linked from the catalog (785 repositories across this catalog and the foundation-model index). It flagged 30 records: 22 labelled open-source without a licence GitHub recognises, and 8 not labelled open-source whose repository now has a licence. An agent read the licence text of each, and a second agent re-checked every proposed change.

- **PUDA:** source-available → open-source. An MIT licence was committed on 2026-09-28 and every package manifest declares MIT.
- **BehaveAgent:** stays paper-only. The repository has an MIT licence file but still contains no code.
- All 22 flagged open-source records keep their label. GitHub reports NOASSERTION or no licence because of an appended note, a combined AGPL/GPL file, a custom header or a licence kept in a subfolder; the licence text itself is an OSI licence in each case. Ten records gained an `access_evidence` object naming the licence and its file; the rest already had one or kept their record unchanged.
- Six source-available benchmarks keep their label although their harness code is licensed: the benchmark's task data, graders or a required solver library carry restrictive, non-commercial or no terms (Modelica agent-workflow benchmark, OSWorld-Science, MolDesignBench, scBench, AutoMat, SimulCost).

## Other corrections

- **RoboRXN / IBM RXN for Chemistry:** platform → paper-only. The hosted RXN for Chemistry platform and its APIs, including RoboRXN cloud execution, went offline on 2026-10-28. The self-hostable successor named in the end-of-service notice covers prediction only, not the synthesis-to-robot system this record describes. Links now point to that successor and to the paper's code.
- **RE-Bench:** METR marked the task suite deprecated on 2026-10-20 and archived the repository; code and licence remain available.
- **The AI Scientist and The AI Scientist-v2:** the peer-reviewed Nature paper (2026) is now linked. **Google AI Co-Scientist:** its Nature paper (2026), which reports in vitro validation run by humans, is linked; autonomy stays A3.
- **OpenAI Deep Research:** the dedicated API models (o3-deep-research, o4-mini-deep-research) were shut down on 2026-07-23; the record now says so and drops the dead API guide. The ChatGPT capability remains. **Terminal-Bench-Science:** its archived Zenodo release is linked.

## Held and rejected candidates

- 310 holds: 131 new discovery leads, 176 October leads whose conditions are still unmet, the two proposals sent back by reviewers (2D-FET-Bench; DREAMS, a MOF discovery agent distinct from the existing `asa-dreams`), and PharmAgents2. Typical reasons are a missing or unlicensed release, an inaccessible full text, or unresolved scope. Holds are leads, not claims that a system or paper is flawed.
- 81 scope rejections (66 from discovery, 15 earlier leads).
- 5 candidates matched existing records and were not duplicated.

## Coverage limits

This is a broad discovery refresh with adversarial verification of every admission. It is **not an exhaustive systematic review**. The arXiv API returned HTTP 429 to most lanes; they fell back to listing and advanced-search pages, which screen titles or abstract phrases, so systems described in other vocabulary may be missed. GitHub repository search was rate-limited in several lanes. Web search was rationed. Only flagged existing records were re-checked; the other baseline records were not re-verified this cycle.

## Local checks

- The dated migration (`scripts/apply_2026_11_06_refresh.py`) is idempotent: a second run left every canonical JSON file, including the resource metadata, byte-identical.
- `build.py`: generated artifacts byte-stable. `validate_catalog.py`: pass (one expected warning, null release reference). `git diff --check`: clean.
- Full URL audit: 1,681 unique URLs across 2,924 occurrences: 2,749 reachable and 161 restricted (publisher and bioRxiv bot blocks, not verification). The 11 "missing" occurrences are GitHub licence-API URLs cited on purpose as evidence that a repository has no licence file. The 3 HTTP errors are FROGENT's lab site (Cloudflare 525 during the audit; HTTP 200 on a manual re-check the same day). Details: [`refresh-2026-11-06/link_recheck.json`](refresh-2026-11-06/link_recheck.json).
- `validate_catalog.py --release` is expected to fail only on the null release reference. Governance was not weakened.

Publication remains a separate step that needs the owner's explicit approval.
