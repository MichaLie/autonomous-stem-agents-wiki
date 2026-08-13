# Autonomous Science Agents discovery audit — 2026-08-13

## Scope and method

This is the durable evidence summary for the v2.1.0 content refresh of the protected local FAIR workspace. Three delegated discovery lanes covered the window 2026-06-15 to 2026-08-13: cross-domain systems and benchmarks, biology and medicine, and chemistry, materials, physics and engineering. Candidates were deduplicated against the current name and alias set, then shuffled into a thirteen-slice verification wave in which each candidate was checked individually under an anti-fabrication contract: resolve the paper or DOI, confirm that it matches the system and is not withdrawn, confirm that any repository or platform is author-owned or author-endorsed, read the licence rather than the badge, and separate real physical closure from simulation. Per-claim source URLs for every verdict are stored in `evidence/additions-2026-08-13/`.

`verified: 2026-08-13` records the evidence-review date. Acceptance means the system is real, in scope, and supported by the cited sources; it is not an endorsement of performance, safety, or fitness for a particular research programme.

### Honest constraints

- The shared web-search quota was exhausted mid-sweep. Later verification stages ran on direct page fetches, publisher and repository APIs, and archive queries instead of a search index, which is shallower for discovering systems that are only announced in prose.
- Company-blog sweeps are undersampled for the same reason. Commercial systems announced only on vendor blogs are therefore under-represented in this cycle relative to preprint-announced systems.
- Several publisher hosts returned 403 to automated fetches (ChemRxiv, RSC, some institutional pages). Where a claim could not be reached from a primary source it was marked UNVERIFIED and left out of the record rather than paraphrased.
- One agent wave was interrupted by a session limit and relaunched. Every interrupted slice was re-run in full rather than resumed, so no candidate carries a partially completed verification.

## Result

- Baseline before this refresh: 372 records.
- Candidates adjudicated in the verification wave: 79 across thirteen slices, plus a separate update-check lane and a separate availability diligence on one existing record.
- Accepted: 66. Held: 4. Rejected: 6. Slice 12 additionally proved that two same-day workbenches with near-identical names are independent projects, and both were accepted.
- Added from the update-check lane: 1 new record (Agent-MD, GCMC-MD campaigns).
- Total additions: 67. Amendments to existing records: 1. Removals: 1.
- Post-refresh catalog: 438 records.

## Accepted additions

### Cross-domain systems (9)

Claude Science; ShinkaEvolve; Agon; OpenScience (Synthetic Sciences); Open Science Desktop; Mechanist; EviGraph; ARIA (CoreWeave AI Research and Iteration Agent); K-Dense scientific-agent-skills.

OpenScience (Synthetic Sciences) and Open Science Desktop are separate repositories created on the same day under confusingly similar names. Slice 12 verified independence directly — disjoint contributors, different stacks, and neither repository is a fork of the other — so both are catalogued rather than merged. K-Dense scientific-agent-skills is a component skills library admitted under the existing ToolUniverse and ChemMCP precedent, not a standalone agent.

### Benchmarks and harnesses (11)

GraphRareBench; scBench-Long; NatureBench; LabBench (robotic chemistry); Lean-QuantumAlg-Bench / Lean-QIT-Bench; Quantum Circuit Vision (QCV); ORBIT-Q; PhySciBench; ChemWorld; MDArena; SciAgentArena.

PhySciBench was held in the 2026-07-13 audit pending clearer benchmark and agent separation; its evaluation code is now Apache-2.0 and its companion DelveAgent framework remains unreleased, which the record states. LabBench (robotic chemistry) is a USTC/CAS artifact unrelated to the catalogued FutureHouse LAB-Bench; the display name was disambiguated at review so that the two cannot be conflated.

### Biology and medicine (15)

EcoXAI; ChatGEM; MechAInistic; SCTA; ProtoPilot; PepCraft; DeepBD; RESCUE; AgentEYE; Ensemble QSP; Prompt-to-Paper; Gemma curation agent (v1.1); Omics Data Discovery Agents; GeneKnow; VERITAS.

ProtoPilot is the only biology addition with any physical closure, recorded as A4–A5 with its human gates spelled out: the paper documents confirmation checkpoints and off-deck human wet-lab steps and does not state that the agent triggers instrument runs itself. RESCUE and DeepBD are retrospective, single-institution clinical systems whose escalation and ranking outputs are reviewed by clinicians; neither releases code.

### Chemistry and materials (10)

PACE-SIMS; CRAFTS; PUDA; LLM4MOF; AdsMind; UniLabOS; AGAPI-Agents; ChatBattery; ArIA; Bunsen.

UniLabOS carries a split licence — GPL-3.0 core framework with proprietary device drivers — and is recorded as A4–A5 for its real hardware closure with human approval gates. PUDA is a hardware orchestration harness rather than a science agent, and its record says so.

### Physics and engineering (22)

Multi-agent qLDPC code discovery; OPERA; CLVisc Agent; Pasqal neutral-atom QPU agentic workflow; Autonomous NV-center quantum sensing agent; AEcroscopyWave; SMEFT-Pheno-Agent; IteraSim RAG; LQCDMaster; NNStar; Onnes; PhysMiner; Embodied CAD; NQS-Agent; MetaDataGenAgent; Vibe Calibration; ASYS (Agentic Symbolic Search); LeWRON; PhyNex; Engineering.ai; OmniQEC; Agent-MD (GCMC-MD campaigns).

Physical-versus-computational closure was checked per record. Vibe Calibration is the only A5 in this cycle: a skill-orchestrating agent that autonomously brought up a real 112-qubit processor, with its human-in-the-loop skill distillation disclosed. The NV-center sensing agent and PACE-SIMS operate real instruments under verifier or plan-approval gates and are recorded as A4. OPERA is explicitly not a physical loop — protocols were frozen before hardware transfer and residuals were not returned to the agent — and Onnes is simulated and log-replayed with no actuation.

## Amended record

- **El Agente Q** — the successor system El Agente Quntur (arXiv:2602.04850) comes from the same Aspuru-Guzik group and releases no artifact of its own. It is recorded as an alias plus an additional paper link and a notes extension rather than a second row, keeping one identity for one line of work. `date_modified: 2026-08-13`; the record's `verified` date is unchanged because only the new paper claim was checked, not the whole record.

## Removed row

- **FARS** (`asa-fars`) — removed on availability grounds and tombstoned in `deprecated_ids.json`. The record's only official source, `analemma.ai`, refuses connections at the network level; the same is true of its `fars-live` and `lemma` subdomains, all of which resolve to a single unresponsive cloud address. The last live Wayback capture is 20260623231233, so the outage began in the seven-week window before this audit. The organisation is not demonstrably defunct — its Discord server was live with members online on 2026-08-13 and its LinkedIn page is up but dormant — yet neither hosts the FARS papers, code, or deployment archive, its GitHub org contains no public repositories, and no shutdown or relocation notice exists anywhere. The X account could not be checked from this environment (HTTP 402 on all unauthenticated fetches) and is recorded as unverifiable rather than absent. Third-party OpenFARS reconstructions exist and are not acceptable as record sources. The archived snapshot `http://web.archive.org/web/20260623231233/https://analemma.ai/` documents the system historically. **The removal is explicitly reversible** if an official live source reappears; the stable ID is retained as a tombstone with a null replacement.

## Held candidates (watchlist)

- **IOBRpy** — held on scope, not evidence. Preprint and MIT repository both verify, but its agent layer is a directory of prompt and command assets that drive an existing bulk RNA-seq pipeline from inside third-party coding agents, with no runtime of its own. Reconsider if the index decides to admit skill packs that wrap existing pipelines, or if IOBRpy ships its own agent runtime.
- **TCellAlign** — held on scope plus missing artifact. A nomenclature-guided label-harmonisation and curation workflow with expert annotation central to it; it neither generates hypotheses nor executes analyses, and its benchmark evaluates label-alignment quality rather than agents. No official repository or dataset release located. Reconsider if the index broadens to data-harmonisation agents, or the benchmark and code are released officially.
- **LabRobFail** — held on partial and unlicensed release. The paper verifies and the author-endorsed repository redirect resolves, but the repository carries no licence, and neither the 20k-trajectory dataset nor the evaluation harness is evident in it. Reconsider when the repository gains a licence and actually ships LabRobFail-Data and LabRobFail-Bench.
- **Sakana Marlin** — held on scope. The system is real and verified on the vendor page, but Sakana scopes it explicitly to business and strategy research ("Virtual CSO"), which places it on the business side of the index's multi-step-scientific-work boundary; the AI Scientist lineage is technology provenance, not a science use case. Its reported launch date is press-derived and unverified on the vendor site. Reconsider if scientific-research use is documented officially, or the owner extends the general deep-research precedent to domain-scoped commercial business agents.

## Rejected candidates

- **PathFound** — a trained pathology foundation-model stack with multi-turn evidence-seeking inference, not a multi-step scientific agent; it belongs to the foundation-model catalog. Distinct in class from the catalogued PathFinder.
- **OntoCodex** — a semi-automated ontology-enrichment component with a human feedback loop; structured knowledge engineering rather than multi-step scientific work, and no released artifact could be verified in the full text.
- **Auto Research for Materials** — a methodology paper proposing a validation protocol for auto-research decisions, demonstrated in one case study. No named released system and no repository anywhere in the full text.
- **ChemBot** — a long-term-memory mechanism for embodied VLA agents demonstrated on human-specified teaching-lab chemistry manipulations; execution method paper, not an autonomous science agent, and no code release.
- **Safe-SDL** — a safety framework proposal (operational design domains, control barrier functions, a transactional protocol) evaluated on an existing benchmark. Neither performs scientific work nor introduces its own harness.
- **Autonomous Research Agents: A Survey of AI Scientists and the Verification Gap** — a survey with a reporting checklist and no released harness, dataset, or site. The catalog is not a list of surveys.

## Update leads closed without change (watchlist)

- **Plato-Bio** — an independent third-party derivative of the open Plato/Denario architecture with no shared authorship, so it is not an alias of Denario. Not added this cycle: single-author derivative without independent adoption evidence.
- **Argonne multi-agentic atomistic simulation framework** — Crossref confirms it shares no authors with ChemGraph, so no ChemGraph amendment. Not added: unnamed system, primary pages 403-blocked, and no artifact verifiable from primary sources.
- **MadAgents (v3) / Agentic Re-Casting** — no MadAgents record exists, so no alias question arises. The paper is a method demonstration with a physicist in the loop and no located code release.
- **OpenDDE** — the existing record already carries the full-release paper, official repository, ungated weights, and an accurate status string, all reconfirmed. Nothing to change.
- **IgGM2** — no official artifact exists; the expected repository returns 404 and the reported successor preprint was not independently fetched, so nothing was added and no note cites it.
- **Edison Finch** — the claim that the platform-agents record omits a current agent named Finch is not supported: the vendor site lists no such product today. No amendment.

## Editorial posture

The verification wave accepted 66 of 75 adjudicated discovery candidates, an acceptance rate of roughly 88%. Every accepted record is individually primary-source-verified and in scope under `MAINTENANCE.md`, and the rejects and holds show the gate was applied rather than waved through. The rate is nonetheless high, and the reason is structural: the discovery lanes fed the verification wave pre-filtered leads, so most obviously out-of-scope material was dropped before a verifier ever saw it. **The owner may reasonably wish to apply a stricter notability bar at review than in-scope-and-verified**, in particular to paper-only systems resting on a single preprint with no released artifact and no independent adoption evidence.

To make that trim easy, these 24 additions are `access: paper-only`:

ASYS (Agentic Symbolic Search); AdsMind; Agent-MD (GCMC-MD campaigns); ArIA; CLVisc Agent; DeepBD; Embodied CAD; Engineering.ai; Ensemble QSP; EviGraph; GeneKnow; LLM4MOF; Mechanist; MetaDataGenAgent; Multi-agent qLDPC code discovery; NQS-Agent; OmniQEC; PACE-SIMS; Pasqal neutral-atom QPU agentic workflow; PhyNex; Prompt-to-Paper; ProtoPilot; RESCUE; Vibe Calibration.

Several of these are worth keeping regardless of any notability trim because their evidence is unusually strong for their class — Vibe Calibration operated a real 112-qubit processor, ProtoPilot and PACE-SIMS document real laboratory work, and RESCUE ran across a full hospital population — so the list is a starting point for review, not a deletion queue.

Seven additions are `access: source-available` because their public repositories carry no usable licence, which under `MAINTENANCE.md` is not open source: SCTA, PepCraft, PUDA, LabBench (robotic chemistry), NNStar, and SciAgentArena have no licence file at all, and LQCDMaster declares MIT in its README without shipping a LICENSE file. Each carries explicit `access_evidence`, and each should be revisited if a licence lands.

The wave also corrected its own inputs. The **scBench-Long** lead reached verification with the premise that no code or data had been released anywhere; the verifier checked directly, found an official Apache-2.0 repository in the authors' own company org created three days before the arXiv posting, and confirmed ownership through the organisation record and matching evaluation identifiers. The record was accepted with the corrected premise and classified `open-data` rather than `open-source`, because the release is a partial subset — 4 of 21 evaluations, without the grading harness — and the paper itself never cites the repository. Discovery-lane claims are treated as leads, not findings.

## Evidence and reproducibility

Every accepted record stores its active paper and official project or repository links directly in `agents_final.json`. Record `sources` hold primary, human-readable evidence URLs; the complete fetch trail behind each verdict, including API endpoints and negative checks, stays in the per-slice files under `evidence/additions-2026-08-13/`. The exact applied set is `scripts/apply_2026_08_13_refresh.py`, which is idempotent — a second run is a byte-level no-op. Full post-refresh URL-resolution results are stored in `evidence/link_audit.tsv`.
