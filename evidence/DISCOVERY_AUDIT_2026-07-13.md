# Autonomous Science Agents discovery audit — 2026-07-13

## Scope and method

This is the durable evidence summary for the protected local FAIR workspace. Three delegated discovery lanes covered cross-domain systems and benchmarks, biology/medicine, and chemistry/materials/physics/engineering. All candidates were deduplicated against the current name and alias set, then shuffled to a separate internal review lane for adversarial verification of paper identity and non-withdrawal, official artifact ownership, agent/benchmark scope, real versus simulated closure, access/licence wording, and A1–A5/B classification. This was internal delegated review, not external independent review.

The primary editor adjudicated disagreements conservatively. Acceptance means the system is real, in scope, and supported by the cited sources; it is not an endorsement of performance, safety, or fitness for a particular research programme. `verified: 2026-07-13` records the evidence-review date.

## Result

- Production baseline: 344 records.
- Strong early additions verified through a separate delegated lane: 6.
- Full-sweep additions after adversarial review: 25.
- Removed as duplicate, redundant, or out of scope: 6.
- Post-discovery snapshot: 369 records. Later release-audit corrections brought the canonical v2.0.0 catalog to 372 records.
- Existing rows materially corrected by the full-sweep migration: 19, in addition to earlier URL/platform corrections.
- Deterministic build: pass, 10 byte-stable generated artifacts.
- Validation at this discovery checkpoint: pass, 0 errors; resource licence and formal publisher were still explicit warnings and were resolved during later v2.0.0 release preparation.
- Post-refresh link audit: 636 unique URLs / 650 occurrences; 617 reachable, 19 access-restricted, 0 missing, and 0 network errors. Restricted responses are authentication, bot-protection, rate-limit, or redirect-gate outcomes and are not classified as broken.

## Accepted additions

### Early additions from a separate review lane

AIDO.Harness; MicroGrowAgents; SciTrace; AgentBuild for Rietveld refinement; Self-Evolving Scientific Agent for fluid control; AHOIS.

MicroGrowAgents' author-owned repository was checked in a separate audit lane but returned repository-not-found during the final link gate, so its final status was conservatively downgraded to paper-only and the unavailable link removed. The other rows are explicitly paper-only, project-site-only, or lab-gated where appropriate. AHOIS remains A5 because it controlled a real multimode-fibre platform, while its predefined human decision points and researcher-performed repetitive full-scale acquisition are disclosed.

### Cross-domain systems and benchmarks

AIRA-dojo; R&D-Agent (RD-Agent); MLE-bench; RE-Bench; ResearchClawBench; DeepResearch Bench / DeepResearch Bench II; PreScience; MLE-Dojo.

These include both research systems and benchmark/harness rows. MLE-bench and MLE-Dojo retain external Kaggle/competition data terms; AIRA-dojo is explicitly non-commercial despite source availability; PreScience is labelled as forecasting/simulation rather than experimental action.

### Biology and medicine

AutoMedBench; BioMedArena; FlowBench (agentic bioinformatics); AutoZyme; Simple Agent Optimization (biomedical imaging); MedGenesis; BehaveAgent.

FlowBench is disambiguated from both the unrelated older FlowBench and the FlowAgent system. BehaveAgent remains paper-only because the official repository states that end-user code is still forthcoming even though the placeholder repository carries an MIT licence. MedGenesis remains A4 because its demonstrated wet-lab handoff is not an autonomous physical loop.

### Chemistry, materials, physics and engineering

Autonomous mobile robots for exploratory synthetic chemistry; Flex-Cat; RoboChem-Flex; Self-driving physical vapor deposition system; SparksMatter; AI X-ray Scientist; CALMS scientific-instrument agents; ArgoLOOM; PDE-Agents; LLMSat.

Physical-loop classifications were checked directly. Six lab systems in that list control real instruments or robotics and are A5 where supported; SparksMatter, ArgoLOOM, PDE-Agents, and LLMSat are explicitly computational/simulated and do not imply physical deployment.

## Removed rows

- `FutureHouse / Edison agents` — redundant umbrella over the retained Robin, Edison-platform, PaperQA3/Edison Literature, and other specific identities.
- `Kosmos radiation-biology evaluation` — a valid case-study audit, but neither an autonomous system nor a reusable benchmark/harness artifact.
- `A mobile robotic chemist` — exact duplicate of the retained 2020 Liverpool/Cooper Mobile Robotic Chemist record.
- `BioMedTools` — a tool registry/chat/MCP infrastructure resource, not one autonomous research agent or agent benchmark.
- `Atlas` and `Gryffin` — Bayesian optimization components rather than autonomous agents or benchmarks. Honegumi was retained but downgraded to A1–A2 because it is an interactive code-generation assistant.

## Material existing-record corrections

- Google AI Co-Scientist: third-party reimplementation link removed; no official public implementation claimed.
- ScienceAgentBench: current verified split and corrected artifact guidance recorded without creating a duplicate benchmark row.
- FlowAgent: local/HPC execution, Nextflow/Snakemake, QC, checkpoint/resume, and recovery capabilities updated; FlowBench added separately.
- DrugAgent: third-party mirror removed and access changed to paper-only.
- CellVoyager: Nature Methods paper and official MIT repository recorded; autonomy updated to A4 for its in-silico hypothesis/analysis/replanning loop.
- BioAgents: Scientific Reports paper and Microsoft implementation recorded; autonomy reduced to A2 because it assists workflow design and troubleshooting rather than autonomous execution.
- HypoBench: official runnable code repository and project page correctly labelled.
- A-Lab: corrected Nature campaign result (36 compounds from 57 targets) replaces the superseded 41/58 claim; unqualified novelty is not asserted.
- AlphaFlow, Synbot, and CRESt: upgraded to A5 because their policies close real robotic experimentation loops.
- k-agents: moved from chemistry to physics, upgraded to A5, and marked lab-gated because it operated a real superconducting quantum processor.
- MADA and Dr.Sai: changed from lab-gated to paper-only because they close computational, not physical, loops.
- AutoLabs, MASTER, MATTERIX: publisher/version-of-record links added; MATTERIX remains computational A3.

## Held or rejected leads

- SGI-Bench — hold: gated datasets without a confirmed explicit dataset licence.
- FIRE-Bench — hold: official project still says code and benchmark are coming soon.
- FrontierScience — hold: static scientific-reasoning/reconstruction benchmarks were not clearly agentic and naming referred to multiple distinct resources.
- MLEvolve — hold: public repository lacks an explicit licence.
- AIRA_2 — hold: no official released implementation established; should later be handled as a family successor.
- PhySciBench / DelveAgent — hold: very recent and custom-restricted dataset terms need clearer benchmark/agent separation.
- BioXArena — hold: paper promises materials, but no released official runnable artifact was confirmed at the review gate.
- AutoBio — hold: simulator benchmark repository lacked an explicit licence; it must never be presented as a deployed physical lab.
- Open-Rosalind — hold: runnable source and a preprint are visible, but the repository's claimed MIT status lacks an explicit licence file at the review gate.
- BCI-Agent — hold: official repository lacks an explicit licence.
- SimAgents and ALL-FEM — hold: useful computational systems, but reusable implementation/licence status was not sufficiently clear.
- STAgent, GPT-Rosalind, BioSkillSafety, T21 Research Assistant, SpaCellAgent, ChatSpatial, RFIA, SimuAgent, LLM-Agent-Controller, and several narrow or artifact-poor leads — held/rejected for redundancy, scope, maturity, access, or evidence reasons.

## Evidence and reproducibility

Every accepted record stores its active paper and official project/repository links directly in `agents_final.json`. The exact applied set is `scripts/apply_2026_07_13_discovery_refresh.py`. Full post-refresh URL-resolution results are stored in `evidence/link_audit.tsv`.
