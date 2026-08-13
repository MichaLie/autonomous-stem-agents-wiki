#!/usr/bin/env python3
"""Apply the delegated and per-candidate verified 2026-08-13 content refresh.

Three discovery lanes (cross-domain/benchmarks, biology/medicine,
chemistry/materials/physics/engineering) were followed by a thirteen-slice
verification wave under anti-fabrication contracts; the per-claim evidence lives
in `evidence/additions-2026-08-13/`. This migration is idempotent and local to
the protected FAIR preview. It does not publish. Held and rejected candidates
are documented in `evidence/DISCOVERY_AUDIT_2026-08-13.md`.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "agents_final.json"
DEPRECATED = ROOT / "deprecated_ids.json"
DATE = "2026-08-13"


def links(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"label": label, "url": url} for label, url in items]


def record(
    record_id: str,
    name: str,
    category: str,
    domain: str,
    access: str,
    autonomy: str,
    inputs: str,
    outputs: str,
    notes: str,
    papers: list[tuple[str, str]],
    repos: list[tuple[str, str]],
    *,
    aliases: list[str] | None = None,
    access_evidence: dict | None = None,
    extra_sources: list[str] | None = None,
) -> dict:
    urls = [url for _, url in papers] + [url for _, url in repos]
    urls += list(extra_sources or [])
    item: dict = {"id": record_id, "date_added": DATE}
    if aliases:
        item["aliases"] = aliases
    item.update({
        "name": name,
        "category": category,
        "domain": domain,
        "paper_links": links(papers),
        "repo_links": links(repos),
        "access": access,
        "inputs": inputs,
        "outputs": outputs,
        "autonomy": autonomy,
        "notes": notes,
        "verified": DATE,
        "sources": sorted(set(urls)),
    })
    if access_evidence:
        item["access_evidence"] = access_evidence
    return item


def unlicensed(source_url: str, detail: str) -> dict:
    return {
        "software_license": detail,
        "commercial_use": False,
        "source_url": source_url,
    }


# Availability-based removal; see evidence/additions-2026-08-13/asa_fars_diligence.json.
REMOVE_IDS = {"asa-fars"}

TOMBSTONES = [
    {
        "id": "asa-fars",
        "removed": DATE,
        "reason": (
            "Availability: the record's only official source (analemma.ai and its subdomains) "
            "has refused connections since the last live capture on 2026-06-23 and no live "
            "official replacement was found; the archived snapshot "
            "http://web.archive.org/web/20260623231233/https://analemma.ai/ documents the system "
            "historically. Reversible if an official live source reappears."
        ),
        "replacement_id": None,
    }
]


# Adjudicated update lead; see evidence/additions-2026-08-13/update_checks_result.json.
UPDATES: dict[str, dict] = {
    "asa-el-agente-q": {
        "aliases": ["El Agente Quntur"],
        "paper_links": links([
            ("arXiv", "https://arxiv.org/abs/2505.02484"),
            ("arXiv (Quntur)", "https://arxiv.org/abs/2602.04850"),
        ]),
        "notes": (
            "Autonomous multi-agent quantum-chemistry workflow agent (Aspuru-Guzik group); "
            "published in Matter. Successor system El Agente Quntur (2026, same Aspuru-Guzik "
            "group, Pérez-Sánchez lead) generalizes the line to the full ORCA 6.0 calculation "
            "range with hierarchical reasoning-driven planning; no separate code release located."
        ),
        "sources": [
            "https://arxiv.org/abs/2505.02484",
            "https://arxiv.org/abs/2602.04850",
        ],
        "date_modified": DATE,
    },
}


NEW_RECORDS: list[dict] = [
    # ---------------------------------------------------------------- biology
    record(
        "asa-ecoxai", "EcoXAI", "biology",
        "Knowledge-graph-grounded biomedical analysis and drug repurposing", "open-source", "A4",
        "Biomedical datasets, biomedical knowledge graphs, and a user-set research goal and budget",
        "Executed analysis pipelines, hypotheses with predictive-model evidence, and tracked experiment reports",
        "Containerized multi-agent system whose bioinformatics agents generate and execute analysis code in isolated Docker containers while an orchestrator dispatches hypotheses to parallel evaluation agents until a user-set budget or cycle limit. An Alzheimer's repurposing case study ranked 79 of 103 candidates above a randomized baseline; the maraviroc hypothesis was supported by later literature, not by experiment. Apache-2.0.",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.08.737358v1")],
        [("GitHub", "https://github.com/EpistasisLab/EcoXAI")],
    ),
    record(
        "asa-chatgem", "ChatGEM", "biology",
        "Genome-scale metabolic model simulation and microbial strain design", "lab-gated", "A3",
        "Natural-language requests in a chat interface, GEM/ecGEM model files, and omics data",
        "Generated and executed COBRApy code with simulation results and natural-language interpretation",
        "PNNL chat system built on the openly licensed ADEPT multi-agent framework (BSD-2-Clause text under a DOE/Battelle disclaimer); a RAG store of 52 curated scripts grounds generated code, raising the mean overall performance score from 2.63 to 4.20. ChatGEM's own codebase and ecGEMs sit on an internal EMSL GitLab that does not resolve publicly. Closure is computational: the P. putida succinate prediction was compared against separately performed experimental work.",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.20.739662v1")],
        [("ADEPT framework", "https://github.com/pnnl/adept-agentic")],
    ),
    record(
        "asa-mechainistic", "MechAInistic", "biology",
        "Constraint-based metabolic model reasoning and drug-target hypotheses", "platform", "A3",
        "A natural-language biological question plus paired healthy/disease constraint-based metabolic models",
        "Model-grounded workflows, COBRApy-derived evidence, cited literature, and reports nominating drug hypotheses",
        "A planning Architect agent is scored by an independently configured Reviewer against pre-specified rubrics that trigger re-planning or re-execution, giving an auditable chain from question to model-derived evidence. Available only as a hosted web interface, with no source repository. Case studies nominated devimistat and ivosidenib with vorasidenib; one intermediate identifier error is disclosed, and the authors state that expert modelling and experimental validation are not replaced.",
        [
            ("arXiv", "https://arxiv.org/abs/2607.18249"),
            ("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.05.11.723319v4"),
        ],
        [("Link", "https://mechainistic.dtih.org/")],
    ),
    record(
        "asa-scta", "SCTA", "biology",
        "Single-cell RNA-seq therapeutic target discovery", "source-available", "A3",
        "Public scRNA-seq datasets (AnnData) plus a disease-focused target-discovery objective",
        "Executed preprocessing, annotation, and differential-expression pipelines with prioritized target hypotheses",
        "Decomposes target discovery into agents aligned with single-cell pipeline decision points, each restricted to a disjoint predefined tool set with no ability to define new tools; a Reviewer agent fires only on execution errors and performs bounded repair under retry limits without changing the biological objective. Stability was assessed by repeated autonomous runs on public GEO datasets. The public repository carries no licence file and its last commits predate the preprint.",
        [("arXiv", "https://arxiv.org/abs/2607.23821")],
        [("GitHub", "https://github.com/silviachen46/SCTA")],
        aliases=["Single-Cell Target Agent"],
        access_evidence=unlicensed(
            "https://github.com/silviachen46/SCTA",
            "None: public repository with no licence file at verification (2026-08-13)",
        ),
    ),
    record(
        "asa-graphrarebench", "GraphRareBench", "benchmark",
        "Phenotype-driven rare-disease diagnosis with graph-defined confounders", "open-source", "B",
        "Coarsened HPO phenotype queries with fixed candidate pools, graph-defined confounders, and evidence bundles",
        "Ranked disease predictions scored by MRR/Hit@k with bootstrap intervals, tool-trace and evidence-coverage audits",
        "Frozen MIT release of 2,365 ontology-derived cases with a gene-component-disjoint test split and 18,093 target-confounder pairs, shipped with loader, validator, evaluator, bootstrap, and agent-audit utilities. Reported baselines mix supervised rankers on a shared feature interface with tool-using agents whose paired MRR difference was not significant while target-evidence coverage differed substantially.",
        [("arXiv", "https://arxiv.org/abs/2607.24878")],
        [
            ("GitHub", "https://github.com/GUI0609/GraphRareBench"),
            ("Hugging Face", "https://huggingface.co/datasets/gcc009/GraphRarebench"),
        ],
    ),
    record(
        "asa-scbench-long", "scBench-Long", "benchmark",
        "Long-horizon single-cell agent tasks recovering published conclusions", "open-data", "B",
        "Compact scientific questions with raw or near-raw single-cell data and no prescribed method",
        "Structured claims graded against controlled answer vocabularies, plus trajectory diagnostics and cost metadata",
        "21 evaluations spanning melanoma tumour-reactive CD8 T cells, RNA+ATAC regulatory inference, chimera development, KRAS-driven lung tumour aging, and lethal COVID-19 lung pathology; across 1,068 completed trajectories the strongest model-harness pair passed 16 of 63 runs. The authors' company org released only 4 of the 21 evaluations plus example trajectories under Apache-2.0, the grading harness and remaining evaluations are unreleased, and the paper itself carries no availability statement.",
        [("arXiv", "https://arxiv.org/abs/2606.26563")],
        [("GitHub", "https://github.com/latchbio/scbench-long")],
        aliases=["SCBench-Long"],
    ),
    record(
        "asa-protopilot", "ProtoPilot", "biology",
        "Wet-lab protocol generation, instrument-code synthesis, and robotic execution", "paper-only", "A4-A5",
        "Natural-language experimental objective plus laboratory context supplied through multi-turn clarification",
        "Validated protocols and SOPs, SDK-compliant instrument code, executed workflows, and feedback-revised versions",
        "Self-evolving multi-agent system with an Orchestrator over a five-layer representation from intent to instrument code, rubric validators, and a runtime-updated skill library; 294 benchmark tasks give 90.2% Top@3 expert preference. Physical closure is real but partial and human-gated: disclosed checkpoints confirm materials and instruments, wet-lab work involved off-deck human steps, and the paper does not state that the agent triggers instrument runs itself.",
        [("arXiv", "https://arxiv.org/abs/2606.31763")],
        [],
        aliases=["A Self-Evolving Agentic System for Automated Generation and Execution of Biological Protocols"],
    ),
    record(
        "asa-pepcraft", "PepCraft", "biology",
        "Antimicrobial peptide design, filtering, and database verification", "source-available", "A3",
        "Peptide design objective with target activity class and allowed chemistry, including non-canonical residues",
        "Generated peptide sequences, filter verdicts, DBAASP/SwissProt novelty checks, and a ranked prioritization report",
        "A Planning Agent orchestrates executors for generation (AMPGAN v3, a two-discriminator conditional GAN covering D-amino acids and terminal modifications), filtering, and database verification. The released repository carries agent prompts, specs, and tools but no licence. Wet-lab closure is human-run and retrospective: five AMPGAN v3 candidates were synthesized and assayed by the authors, and the paper calls prospective evaluation of PepCraft's selection future work.",
        [("arXiv", "https://arxiv.org/abs/2606.17127")],
        [("GitHub", "https://github.com/marszzibros/AMPGANv3")],
        aliases=["AMPGAN v3"],
        access_evidence=unlicensed(
            "https://github.com/marszzibros/AMPGANv3",
            "None: public repository with no licence file at verification (2026-08-13)",
        ),
    ),
    record(
        "asa-deepbd", "DeepBD", "biology",
        "Variant prioritization and diagnostic interpretation for birth defects", "paper-only", "A3",
        "Sequencing-derived candidate variants, phenotype descriptions mapped to HPO, and heterogeneous evidence sources",
        "Ranked patient-specific candidate variants with provenance-preserving evidence records and a diagnostic synthesis",
        "Four-part workflow combining LLM-assisted case structuring, a pretrained evidence engine over phenotype-conditioned biological context, specialist evidence modules, and a grounded agentic review layer; the central ranking substrate is supervised rather than LLM-driven. Developed on an in-house cohort of 18,622 fetal and infant cases with Recall@1 0.658 on an internal held-out benchmark. Retrospective and single-institution by the authors' own account, with no code or data released.",
        [("arXiv", "https://arxiv.org/abs/2606.24779")],
        [],
    ),
    record(
        "asa-rescue", "RESCUE", "biology",
        "Rare-disease screening and genomic-testing escalation across an EHR", "paper-only", "A3",
        "Institutional EHR diagnosis and test codes and clinical notes, plus a target rare-disease definition",
        "A genetic-evidence code taxonomy, a trained classifier, a ranked candidate list, and chart-review judgements",
        "Ontology, Modeling, Screening, and Review agents run end to end on pediatric-hospital data: holdout AUC 0.808, and flagged candidates were 7.4-fold more likely to receive subsequent genomic assessment. Human gates are load-bearing: blinded chart review by a study author established the 80% precision figure, and the workflow escalates candidates for clinician decision rather than ordering tests. The repository named in the v2 availability statement did not exist at verification.",
        [
            ("medRxiv", "https://www.medrxiv.org/content/10.64898/2026.06.24.26356357v2"),
            ("PubMed", "https://pubmed.ncbi.nlm.nih.gov/42428098/"),
        ],
        [],
        aliases=["Rare Disease Detection and Escalation Support via a Learning Health System"],
    ),
    record(
        "asa-agenteye", "AgentEYE", "biology",
        "Multimodal ophthalmic diagnosis (clinical decision support)", "open-source", "A2",
        "Ocular images (fundus photography, B-scan ultrasonography) plus a diagnostic query",
        "Evidence-grounded, citation-auditable diagnostic reports synthesized from imaging tools and guideline retrieval",
        "Auditable multimodal agent that routes ocular images to specialized fundus and B-scan tools and retrieves guideline and web evidence; a blinded 200-case evaluation by three ophthalmologists showed improved correctness, completeness, safety, and citation grounding over LLM-only baselines. Positioned as a decision-support prototype with the clinician as final decision-maker; the MIT release is metadata-only, without raw images or model weights.",
        [("Cell Reports Medicine", "https://doi.org/10.1016/j.xcrm.2026.102969")],
        [("GitHub", "https://github.com/OpenMedAILab/AgentEYE")],
        extra_sources=["https://pubmed.ncbi.nlm.nih.gov/42556343/"],
    ),
    record(
        "asa-ensemble-qsp", "Ensemble QSP", "biology",
        "Quantitative systems pharmacology and PBPK-PD model building", "paper-only", "A3-A4",
        "Long-horizon QSP/PBPK modeling objective with pharmacokinetic-pharmacodynamic data and physical constraints",
        "Autonomously constructed and selected PK-PD models, recovered parameters, and bounded persistent project state",
        "Five specialist worker agents operate under domain-expert principal-investigator agents, and a three-layer hierarchical memory keeps mid-term project state bounded (median 301 tokens), enabling autonomous multi-session model building and model selection with improved parameter recovery over single-agent baselines. No code release was located.",
        [("arXiv", "https://arxiv.org/abs/2607.07666")],
        [],
        aliases=["A hierarchical memory architecture overcomes context limits in long-horizon multi-agent computational modeling"],
    ),
    record(
        "asa-prompt-to-paper", "Prompt-to-Paper", "biology",
        "End-to-end bioinformatics research automation (prompt to manuscript)", "paper-only", "A4",
        "A research prompt or topic in bioinformatics",
        "A manuscript grounded in 60-100 retrieved papers, executed analyses, and eight-dimensional quality scores",
        "Multi-agent system combining deterministic RAG grounding, an autonomous coding agent that runs real analyses rather than synthesizing results, and an eight-dimensional scorer with hallucination penalties; five bioinformatics case studies averaged 7.0/10 from human reviewers at roughly $0.31 per paper. Evaluation is largely self-defined and no code was released.",
        [("arXiv", "https://arxiv.org/abs/2607.05456")],
        [],
    ),
    record(
        "asa-gemma-curation-agent", "Gemma curation agent (v1.1)", "biology",
        "Genomics dataset curation and experimental-design annotation", "open-source", "A3",
        "GEO study metadata, sample characteristics, and source publications for Gemma transcriptomic datasets",
        "Ontology-anchored sample- and experiment-level annotations for curator review, plus a 500-study benchmark set",
        "LLM-supported agentic pipeline curating datasets for the 23,000-dataset Gemma resource at near-curator accuracy, roughly one twentieth of the cost and over a hundred times the speed; annotations are proposals reviewed in a curator UI, with triage routing likely errors to human review. Code Apache-2.0 and benchmark data CC BY-NC 4.0; full operation requires a Gemma 2.0 REST endpoint that is not public. Unrelated to Google's Gemma language models.",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.07.30.741874v1")],
        [
            ("GitHub (agents)", "https://github.com/PavlidisLab/gemma-curation-agents-v1.1"),
            ("GitHub (benchmark data)", "https://github.com/PavlidisLab/gemma-curation-benchmark-data"),
        ],
        aliases=["Gemma curation agents"],
    ),
    record(
        "asa-omics-data-discovery-agents", "Omics Data Discovery Agents", "biology",
        "Retrieval and reanalysis of published proteomics and RNA-seq datasets", "open-source", "A2",
        "Published open-access articles, public omics repositories, and containerized quantification tools over MCP",
        "Retrieved datasets with extracted metadata, reanalysis quantifications, and cross-study syntheses",
        "Cedars-Sinai framework that autonomously locates, retrieves, and reanalyzes published omics data; five end-to-end reanalyses reproduced author-deposited abundances with per-sample correlations of 0.85-0.997 and differential-expression agreement of 0.88-0.91. Computational only, with no physical experiment loop and humans posing the research questions. GPL-3.0.",
        [
            ("arXiv", "https://arxiv.org/abs/2603.10161"),
            ("PubMed", "https://pubmed.ncbi.nlm.nih.gov/42539124/"),
        ],
        [("GitHub", "https://github.com/xomicsdatascience/odda")],
        aliases=["ODDA"],
    ),
    record(
        "asa-geneknow", "GeneKnow", "biology",
        "Source-grounded literature evidence synthesis for gene function", "paper-only", "A1",
        "Gene-context questions plus retrieved literature for multi-paper discovery and single-paper inspection",
        "Source-grounded evidence syntheses with claim-to-passage provenance links and deterministic bibliographies",
        "Auditable framework separating deterministic evidence-critical operations - retrieval, passage selection, provenance tracking, bibliography construction - from generative steps constrained to semantic analysis, and benchmarked above general-purpose and scientific AI systems on claim support and citation fidelity. Literature synthesis only, with no data analysis or experiment execution; code or platform availability could not be verified.",
        [("bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.05.28.728511v1")],
        [],
    ),
    record(
        "asa-veritas", "VERITAS", "biology",
        "Biomedical imaging hypothesis testing (cardiac and glioma MRI)", "open-source", "A3",
        "Natural-language hypotheses and medical imaging cohorts, with segmentation and sandboxed statistical analysis",
        "An auditable evidence trail with verdicts classified as Supported, Refuted, Underpowered, or Invalid",
        "Multi-agent co-scientist that tests image-derived hypotheses end to end through role-specialized agents, sandboxed statistics, and a deterministic Evidence Classification Operator rather than post-hoc LLM grading; 81.4% verdict accuracy with frontier models and 71.2% with open-weight models on a 64-hypothesis benchmark. Computational loop over existing imaging data, with no physical experimentation. Apache-2.0.",
        [("arXiv", "https://arxiv.org/abs/2604.12144")],
        [("GitHub", "https://github.com/LucZot/veritas")],
    ),
    record(
        "asa-naturebench", "NatureBench", "benchmark",
        "Scientific machine-learning tasks distilled from Nature-family papers", "open-source", "B",
        "Coding agents evaluated in standardized per-task containers built automatically from source papers",
        "Task success and beyond-reproduction metrics recording whether agents surpass the published state of the art",
        "MIT benchmark of 90 tasks across six domains that tests whether coding agents can move beyond reproducing to beating published results; the strongest agent surpassed the state of the art on 17.8% of tasks, with failures driven mainly by incorrect methodology selection. NatureGym, the automated environment-construction pipeline, ships in the same repository.",
        [("arXiv", "https://arxiv.org/abs/2606.24530")],
        [("GitHub", "https://github.com/FrontisAI/NatureBench")],
        aliases=["NatureGym"],
    ),

    # ------------------------------------------------------ chemistry and materials
    record(
        "asa-pace-sims", "PACE-SIMS", "chemistry",
        "Autonomous time-of-flight secondary ion mass spectrometry characterization", "paper-only", "A4",
        "Researcher-specified scientific questions and quality requirements, plus a physical ToF-SIMS instrument",
        "Autonomously acquired SIMS measurements with checkpoint quality assessments and corrective decisions",
        "Human-AI workflow in which the researcher sets objectives and approves the AI-generated plan before the agent autonomously executes acquisition on the instrument under checkpoint-gated quality control; validated on 18O-enriched WOx films. No code repository is disclosed on the paper page.",
        [("arXiv", "https://arxiv.org/abs/2608.12277")],
        [],
    ),
    record(
        "asa-crafts", "CRAFTS", "chemistry",
        "Chemical process engineering (equation-oriented process simulation)", "open-source", "A3",
        "Natural-language process request, process flowsheet diagram evidence, and curated engineering knowledge",
        "Typed intermediate artifacts, executable solved IDAES/Pyomo process models, and eligible optimization results",
        "Seven role-bounded agents, three of them LoRA-fine-tuned, build executable chemical-process models through typed intermediate representations with deterministic engineering gates between stages and bounded allowlisted repair; invalid trajectories fail closed. Computational closure with no human in the execution loop. Introduces the OpenIDAES-450 dataset with a frozen 82-case held-out split. MIT.",
        [("arXiv", "https://arxiv.org/abs/2608.01369")],
        [("GitHub", "https://github.com/Galigeigei-Z/CRAFTS-Multi-agent-for-Equation-oriented-PSE")],
        aliases=["Collaborative Role-Adaptive Fine-Tuning of LLM Agents for Chemical Process Simulation"],
    ),
    record(
        "asa-puda", "PUDA", "chemistry",
        "Self-driving laboratory hardware orchestration harness", "source-available", "A3-A4",
        "Agent-issued CLI/JSON protocol commands and experiment campaign specifications",
        "Deterministic, atomic hardware executions with provenance-linked state, responses, and data records",
        "AI-native hardware harness rather than a science agent: agents observe, decide, and act through a command-line runtime while hardware execution stays deterministic and auditable, deployed across sample-handling, synthesis, and device-measurement workflows. Researchers can inspect, approve, or revise hardware actions mid-campaign; the public repositories carry no licence file.",
        [("arXiv", "https://arxiv.org/abs/2607.26464")],
        [
            ("GitHub", "https://github.com/PUDAP/puda"),
            ("Docs", "https://docs.puda.co/"),
        ],
        aliases=["Physical Unified Device Architecture"],
        access_evidence=unlicensed(
            "https://github.com/PUDAP/puda",
            "None: public repository with no licence file at verification (2026-08-13)",
        ),
    ),
    record(
        "asa-llm4mof", "LLM4MOF", "chemistry",
        "Interpretable inverse design of metal-organic frameworks", "paper-only", "A2-A3",
        "Target MOF property or design task and a MOF candidate space",
        "Interpretable design hypotheses and simulation-validated candidate frameworks",
        "Two agents iterate in a closed loop: one proposes interpretable hypotheses over metal nodes, linkers, pore geometry, and functional chemistry, the other translates them into constraints selecting candidates for simulation testing, converging within roughly 400 property evaluations. From the Kim group behind ChatMOF but a distinct system; no code released at verification.",
        [("arXiv", "https://arxiv.org/abs/2606.29459")],
        [],
        aliases=["Interpretable Inverse Design of Metal-Organic Frameworks with Large Language Model Agents"],
    ),
    record(
        "asa-adsmind", "AdsMind", "chemistry",
        "Catalyst adsorption configuration discovery", "paper-only", "A3",
        "An adsorbate and a heterogeneous catalyst surface",
        "Self-corrected lowest-energy surface-adsorbate configurations from machine-learning force-field relaxation",
        "Closed-loop multi-agent framework in which machine-learning force-field relaxation feedback lets the agents autonomously correct erroneous initial configuration guesses. Distinct lineage from the catalogued Adsorb-Agent, against which it is compared; computational closure only, and no code released at verification.",
        [("arXiv", "https://arxiv.org/abs/2606.19152")],
        [],
        aliases=["Adsorption configuration discovery with Machine intelligence and relaxation feedback"],
    ),
    record(
        "asa-unilabos", "UniLabOS", "chemistry",
        "Autonomous-laboratory orchestration operating system", "open-source", "A4-A5",
        "Experiment goals or protocols and heterogeneous instrument configurations behind typed device abstractions",
        "Orchestrated physical experiment execution with transactional safeguards, characterization data, and audit trails",
        "AI-native laboratory operating system from the DP Technology and deepmodeling ecosystem, demonstrated on four real hardware settings including an organic synthesis run confirmed by 1H NMR and a computation-intensive closed loop that autonomously switched electrolysis mode on a sensor trigger. Humans stay in the loop for goals, approvals, and governance. The core framework is GPL-3.0 while the device drivers carry a DP Technology proprietary licence.",
        [("arXiv", "https://arxiv.org/abs/2512.21766")],
        [
            ("GitHub", "https://github.com/deepmodeling/Uni-Lab-OS"),
            ("Docs", "https://deepmodeling.github.io/Uni-Lab-OS/"),
        ],
        aliases=["Uni-Lab-OS"],
    ),
    record(
        "asa-agapi-agents", "AGAPI-Agents", "chemistry",
        "Materials design and characterization tool agents", "open-source", "A2",
        "Natural-language or Python materials-design queries routed to agent tools",
        "Tool-augmented materials predictions and analyses: properties, band structures, diffraction, structure retrieval",
        "Apache-2.0 agentic platform from AtomGPTLab in the JARVIS lineage, integrating eight open-source LLMs with 18 REST endpoints, 28 agent tools, and 50 web apps; the paper characterizes when tool access improves accuracy, finding tool-augmented agents strongly outperform tool-free LLMs on unfamiliar materials properties. Also usable as a hosted platform.",
        [("arXiv", "https://arxiv.org/abs/2512.11935")],
        [
            ("GitHub", "https://github.com/atomgptlab/agapi"),
            ("Platform", "https://atomgpt.org"),
        ],
        aliases=["AGAPI"],
    ),
    record(
        "asa-chatbattery", "ChatBattery", "chemistry",
        "Lithium-ion cathode materials discovery", "open-source", "A3-A4",
        "A starting cathode material formula given as text",
        "Novel cathode candidates, DFT-validated structures, and synthesized materials with measured performance",
        "Seven-agent framework, including an explicit Human agent, that steers LLM reasoning with domain knowledge for cathode design; its three predicted materials were synthesized and characterized, exceeding NMC811 capacity by 28.8%, 25.2%, and 18.5%. Disclosed human gates: expert judgment at problem conceptualization, and human experimentalists performing the wet-lab synthesis and verification. MIT.",
        [("arXiv", "https://arxiv.org/abs/2507.16110")],
        [("GitHub", "https://github.com/chao1224/ChatBattery")],
    ),
    record(
        "asa-aria-molecular-simulations", "ArIA", "chemistry",
        "LLM-driven quantum-chemistry simulation with ORCA", "paper-only", "A2",
        "Natural-language user instructions describing a molecular-simulation problem",
        "Executed ORCA simulations, visualizations, generated reports, and question answering over the results",
        "University of Groningen (Pollice group) agent built on open-source LLMs deployable on standard personal computers: it interprets a prompt, runs ORCA simulations, and produces a report the user can query. Each task is human-initiated and human-interpreted, with computational execution only. The abstract states a fully open-source release, but no repository URL could be verified, so access remains paper-only.",
        [("ChemRxiv", "https://chemrxiv.org/doi/full/10.26434/chemrxiv.15002344/v2")],
        [],
        aliases=["Molecular Simulations Assisted by an Artificial Intelligence Agent"],
    ),
    record(
        "asa-bunsen", "Bunsen", "chemistry",
        "Agentic co-scientist for molecular discovery", "platform", "A2-A3",
        "Natural-language research requests plus project structures and molecules",
        "Validated multi-stage computational workflows with monitored jobs and results",
        "Schrodinger's agentic co-scientist converts natural-language instructions into computational pipelines on the Schrodinger platform - protein preparation, Glide docking, FEP+, Desmond MD, ADMET prediction, AutoDesigner generation - autonomously chaining stages, submitting and monitoring jobs, and self-correcting, while the researcher directs each request and reviews outputs. Closed beta as of August 2026, deployed single-tenant on customer infrastructure.",
        [("Link", "https://www.schrodinger.com/bunsen")],
        [],
        aliases=["Schrodinger Bunsen"],
    ),

    # -------------------------------------------------- physics and engineering
    record(
        "asa-multi-agent-qldpc-code-discovery", "Multi-agent qLDPC code discovery", "physics",
        "Quantum error correction (quantum LDPC code design)", "paper-only", "A4",
        "Design constraints for finite-length qLDPC codes plus persistent memory of lessons and candidate lineage",
        "Executable code-family generator programs, discovered code instances, and BP-OSD-verified logical failure rates",
        "Closed-loop computational discovery in which a researcher council and curator synthesize hypotheses into tasks while a worker agent evolves executable code-family programs against a deterministic construction and evaluation pipeline with MAP-Elites archiving and persistent lessons and anti-lessons memory. Fully computational closure with no in-loop human gates disclosed; construction, search, and evaluation code are promised publicly on publication.",
        [("arXiv", "https://arxiv.org/abs/2608.08996")],
        [],
        aliases=["Multi-agent discovery of practical quantum LDPC codes"],
    ),
    record(
        "asa-opera", "OPERA", "physics",
        "Autonomous optical experimentation with operator-residual feedback", "open-source", "A4",
        "Optical experiment tasks in digital twins plus a library of optical operators and interpretable residuals",
        "Operator protocols evaluated against withheld references and frozen protocols executed on three optical instruments",
        "The agent closes an iterative operator-selection loop in digital twins using physics-grounded residuals instead of hackable scores; score-only feedback produced non-physical score gains in 23.6-39.0% of decisions against 0.9-1.9% with residuals. Not a physical closed loop: protocols were frozen before transfer to the three optical instruments and hardware residuals were not returned to the agent, so physical execution is open-loop validation. MIT, with a Zenodo archive.",
        [("arXiv", "https://arxiv.org/abs/2608.05990")],
        [
            ("GitHub", "https://github.com/ningxu1995/OPERA"),
            ("Zenodo", "https://doi.org/10.5281/zenodo.21504254"),
        ],
        aliases=["Operator-residual feedback for reliable autonomous optical experiments"],
    ),
    record(
        "asa-clvisc-agent", "CLVisc Agent", "physics",
        "Relativistic viscous hydrodynamics of the quark-gluon plasma", "paper-only", "A3",
        "Natural-language physics study goals plus a CLVisc source checkout reachable through a meta-skill",
        "Agent-authored specialized skills, parameter scans, executed GPU ensembles, and publication-ready figures",
        "A meta-skill inspects the scientific source code and writes the agent's own specialized tool skill, after which it runs end-to-end quark-gluon plasma simulation campaigns on temperature-dependent shear viscosity and nuclear-structure effects in O+O collisions. Disclosed gates: user confirmation is required in the skill-generation loop, and physical interpretations require expert verification. Closure is computational on HPC, not physical.",
        [("arXiv", "https://arxiv.org/abs/2607.27822")],
        [],
    ),
    record(
        "asa-pasqal-neutral-atom-qpu-workflow", "Pasqal neutral-atom QPU agentic workflow", "physics",
        "Neutral-atom quantum hardware experimentation", "paper-only", "A3-A4",
        "A published paper or patent plus a scientific objective and Pasqal cloud QPU access",
        "Structured experiment specifications, executable Pulser sequences, emulation checks, and QPU campaign results",
        "Unnamed Pasqal workflow that goes from a published paper or patent to overnight campaigns on two real cloud neutral-atom QPUs across three case studies in many-body physics and optimization. Disclosed gates: no protocol reaches the QPU without emulation validation, the researcher stays in the decision loop, and domain-expert review caught two agent failures. Workflow code is not released.",
        [("arXiv", "https://arxiv.org/abs/2607.25834")],
        [],
        aliases=["Lowering the implementation barrier of neutral-atom quantum computing with agentic workflows"],
    ),
    record(
        "asa-nv-center-quantum-sensing-agent", "Autonomous NV-center quantum sensing agent", "physics",
        "NV-center quantum sensing experiments", "open-source", "A4",
        "Experiment goal, persistent project records, quantitative analysis tools, and verified hardware-control requests",
        "Executed NV measurements (ODMR, Ramsey, CPMG), calibrations, T2* results, and analysis records",
        "Cappellaro-group agent workflow that autonomously ran a real NV-center experiment on a home-built confocal microscope, selecting a centre, calibrating resonance, measuring T2* by Ramsey, and adding a CPMG check. Disclosed gates: the agent has no direct instrument-driver access, a deterministic verifier enforces parameter ranges and safety rules on every hardware request, and one case study involved human advice during reanalysis. Code MIT, documentation and data CC BY 4.0.",
        [("arXiv", "https://arxiv.org/abs/2607.25145")],
        [("GitHub", "https://github.com/takuyaisogawa/nv-autonomous-experiments")],
        aliases=["Agentic AI for Scientific Reasoning in Autonomous Quantum Sensing Experiments"],
    ),
    record(
        "asa-labbench-robotic-chemistry", "LabBench (robotic chemistry)", "benchmark",
        "Embodied chemistry-lab agent evaluation", "source-available", "B",
        "32 locked chemistry task prompts plus machine-readable skill contracts for 45 robotic workstations",
        "Agent-generated workflows scored for expert-assessed physical executability, dispatch, and replanning",
        "USTC/CAS stress test of LLM agents against a real 45-workstation robotic chemistry laboratory: 4,608 trials across 48 harness-model configurations, of which only 3.3% produced expert-assessed executable workflows, with a physically executed closed-loop subset over five feedback rounds. Agents could not bypass laboratory identity, schema, state, or dispatch checks. Skill library and scoring code are public but the repository carries no licence file. Distinct from the FutureHouse LAB-Bench biology benchmark.",
        [("arXiv", "https://arxiv.org/abs/2607.23045")],
        [("GitHub", "https://github.com/pic-ai-robotic-chemistry/LabBench")],
        aliases=[
            "LabBench",
            "Robotic chemistry laboratory LLM-agent stress test",
            "Stress-testing large language model agents in a robotic chemistry laboratory",
        ],
        access_evidence=unlicensed(
            "https://github.com/pic-ai-robotic-chemistry/LabBench",
            "None: public repository with no licence file at verification (2026-08-13)",
        ),
    ),
    record(
        "asa-aecroscopywave", "AEcroscopyWave", "physics",
        "Scanning-probe microscopy orchestration for agentic AI", "lab-gated", "A3-A4",
        "Human or agent experiment plans, MCP tool calls, registered workflows, and custom waveform scripts",
        "Executed scanning-probe experiments, job results posted over REST, and validated workflow records",
        "ORNL CNMS successor to AEcroscopy: a distributed server-client platform whose FastMCP tool server lets agents plan and run real scanning-probe experiments across DriveAFM, Cypher, and Nanonis STM backends. Disclosed gates: agents may execute only registered handlers, registry workflows, or human-approved custom scripts, which must first pass digital-twin validation. Only user documentation is publicly released and the linked repository carries no licence.",
        [("arXiv", "https://arxiv.org/abs/2607.22975")],
        [
            ("GitHub", "https://github.com/yongtaoliu/aecroscopy.pyae"),
            ("Docs", "https://yongtaoliu.github.io/aecroscopy.pyae/welcome_intro.html"),
        ],
        aliases=["AEcroscopy Wave"],
    ),
    record(
        "asa-smeft-pheno-agent", "SMEFT-Pheno-Agent", "physics",
        "SMEFT collider phenomenology", "open-source", "A3",
        "Natural-language SMEFT analysis intent and nine interactively collected configuration parameters",
        "Simulation samples, ML-based event selections, Wilson-coefficient constraints, phase manifests, and prose drafts",
        "Twelve-phase workflow in which the agent proposes kinematic observables and machine-learning algorithms while all numerics are delegated to validated domain tools; configuration intake is the only interactive stage, after which the remaining phases run unattended with physical parameters locked. Distributed as a portable MIT-licensed skill under the Agent Skills open standard.",
        [("arXiv", "https://arxiv.org/abs/2607.22331")],
        [
            ("GitHub", "https://github.com/NBAlexis/SMEFT-Pheno-Agent"),
            ("Gitee", "https://gitee.com/NBAlexis/automated-smeft-ml-pheno"),
        ],
        aliases=["automated-smeft-ml-pheno"],
    ),
    record(
        "asa-lean-quantumalg-bench", "Lean-QuantumAlg-Bench / Lean-QIT-Bench", "benchmark",
        "Lean 4 theorem proving for quantum algorithms and quantum information", "open-source", "B",
        "Lean 4 theorem-completion tasks with paired TeX statements and optional hints in a fixed environment",
        "Machine-checked Lean proofs with difficulty-weighted scores, plus cost and completion-rate comparisons",
        "Paired 36-task and 40-task Lean 4 benchmarks whose difficulty weights were assigned before model execution, scored by deterministic proof checking plus targeted semantic review. Library-augmented deduction, giving access to a verified domain library, improved all eight model-benchmark comparisons. Both Apache-2.0 repositories are published mirrors of the reviewed public benchmark surface.",
        [("arXiv", "https://arxiv.org/abs/2607.21533")],
        [
            ("GitHub (QuantumAlg)", "https://github.com/QudeLeap/Lean-QuantumAlg-Bench"),
            ("GitHub (QIT)", "https://github.com/QuAIR/Lean-QIT-Bench"),
        ],
        aliases=["Lean-QuantumAlg-Bench", "Lean-QIT-Bench"],
    ),
    record(
        "asa-iterasim-rag", "IteraSim RAG", "physics",
        "OpenFOAM computational fluid dynamics case setup and troubleshooting", "lab-gated", "A3",
        "Natural-language OpenFOAM case requests for zero-shot setup, parameter modification, or troubleshooting",
        "Mutually consistent OpenFOAM input decks, plus compiled and executed cases with log-driven corrections",
        "A multi-stage retrieval back-end feeds Architect, InputWriter, and Reviewer agents over a canonical-knowledge layer, with the Reviewer compiling, running the simulation, and iterating in a corrective loop bounded to ten cycles. The retrieval engine and orchestrator are commercial IP of IteraSim - a single-author paper with a disclosed financial interest - available for academic collaboration or licensing on request; only the 28-case benchmark, rubric, and figure scripts are MIT.",
        [("arXiv", "https://arxiv.org/abs/2607.20346")],
        [("GitHub (benchmark)", "https://github.com/iterasim/iterasim-rag-public")],
    ),
    record(
        "asa-lqcdmaster", "LQCDMaster", "physics",
        "Lattice quantum chromodynamics measurement code generation and HPC execution", "source-available", "A3",
        "Natural-language lattice-QCD research tasks",
        "Executable PyQUDA measurement scripts, Slurm submission artifacts, execution logs, and numerical observables",
        "Planner-Executor agent pair with expert-annotated lattice-QCD skills and a deterministic Wick-contraction tool; a disclosed human checkpoint lets physicists review and refine the plan before execution, after which code generation, static analysis, and auto-debugging proceed autonomously. Reproduces expert implementations at machine precision on 63 of 70 benchmark tasks. The README declares MIT but the repository carried no standalone LICENSE file at verification, so the code is recorded as source-available.",
        [("arXiv", "https://arxiv.org/abs/2607.15001")],
        [("GitHub", "https://github.com/sjtu-sai-agents/LQCD_Master")],
        aliases=["LQCD Master", "LQCD_Master"],
        access_evidence={
            "software_license": "MIT declared in the README; no LICENSE file in the repository at verification (2026-08-13)",
            "commercial_use": True,
            "source_url": "https://github.com/sjtu-sai-agents/LQCD_Master",
        },
    ),
    record(
        "asa-nnstar", "NNStar", "physics",
        "Nuclear matter and neutron-star equation-of-state inference", "source-available", "A3",
        "Relativistic mean-field Lagrangian specifications with coupling parameters and natural-language task requests",
        "Saturation properties, beta-equilibrium equations of state, TOV predictions, and Bayesian joint-analysis scores",
        "Delivered not as a standalone program but as a self-describing skill installed into an open LLM agent platform; the paper states the agent can read a model, fit its parameters, and report all observables without human intervention, with computational closure only. The companion repository bundles the skill and a 100-task with/without-skill benchmark harness, but its LICENSE file is an unresolved placeholder and the harness targeted a private remote machine.",
        [("arXiv", "https://arxiv.org/abs/2607.13930")],
        [("GitHub", "https://github.com/AaronMahn/NM-rmf-benchmark-scheme")],
        aliases=["RMF Skill Benchmark"],
        access_evidence=unlicensed(
            "https://github.com/AaronMahn/NM-rmf-benchmark-scheme",
            "None: LICENSE file is an unresolved placeholder at verification (2026-08-13)",
        ),
    ),
    record(
        "asa-quantum-circuit-vision", "Quantum Circuit Vision (QCV)", "benchmark",
        "Quantum programming from circuit diagrams (multimodal)", "open-data", "B",
        "Quantum circuit diagrams: 132 circuits, 13 categories, 1-10 qubits, in five modalities",
        "Executable Amazon Braket code verified by unitary fidelity, with accuracy and cost metrics per model",
        "Cost-aware benchmark testing whether multimodal models can read circuit diagrams and emit verified Braket code; it finds that circuit depth rather than qubit count predicts failure. The MIT-licensed QCV-Dataset is released on Hugging Face, but the evaluation-code repository is anonymized in the v1 preprint, so only the dataset is publicly verifiable.",
        [("arXiv", "https://arxiv.org/abs/2607.10057")],
        [("Hugging Face", "https://huggingface.co/datasets/QuantBlockchain/qcv-dataset")],
        aliases=["QCV", "QCV-Dataset"],
    ),
    record(
        "asa-onnes", "Onnes", "physics",
        "Dilution-refrigerator fault diagnosis for quantum-computing infrastructure", "open-source", "A3",
        "Simulated dilution-refrigerator telemetry from a physics forward model with noise learned from real logs",
        "Fault detection and classification with diagnosis rationale, comparison metrics, and released run logs",
        "Digital-twin simulator driving a live five-role multi-agent operations layer; few-shot demonstrations plus self-consistency voting lift classification accuracy from 0.685 to 0.990, with full recall on physics faults at a 6.4% false-alarm rate on real hardware logs. Closure is simulated and log-replayed, with no physical actuation of the refrigerator. Code, data, and run logs are MIT.",
        [("arXiv", "https://arxiv.org/abs/2607.05805")],
        [("GitHub", "https://github.com/Onnes-Research/onnes")],
    ),
    record(
        "asa-physminer", "PhysMiner", "physics",
        "Turbulence and fluid-mechanics discovery from CFD data", "open-source", "A3",
        "CFD flow fields plus a literature corpus for the knowledge base",
        "Triple-decomposition statistics, vortex-line extractions, flow mechanisms, and modeling recommendations",
        "Agentic framework pairing a physics-discovery agent with a validation agent over triple decomposition of the velocity-gradient tensor, demonstrated on periodic hill flow with improved Reynolds-stress predictions. Source code and the Triple Decomposition Library are released under MIT with a community contribution mechanism for new flow cases.",
        [("arXiv", "https://arxiv.org/abs/2607.04009")],
        [("GitHub", "https://github.com/iDesign-Lab/PhysMiner")],
    ),
    record(
        "asa-orbit-q", "ORBIT-Q", "benchmark",
        "Research-level quantum programming for autonomous coding agents", "open-source", "B",
        "Twelve containerized research-level quantum-workflow tasks across four quantum programming frameworks",
        "Dual-axis agent-framework scores from a multi-tier verification pipeline ending in expert review",
        "Harbor-based benchmark that varies framework at fixed agent and agent at fixed framework, verifying functional correctness, runtime execution, policy compliance, and LLM audits before human expert review. A substantial gap to expert human implementations remains. Tasks, verifiers, and evaluation code are Apache-2.0.",
        [("arXiv", "https://arxiv.org/abs/2607.03105")],
        [("GitHub", "https://github.com/sxzgroup/ORBIT-Q")],
        aliases=["Open Research Benchmark for Integrated Tasks in Quantum Computing"],
    ),
    record(
        "asa-embodied-cad", "Embodied CAD", "physics",
        "Parametric B-Rep CAD assembly modeling", "paper-only", "A3",
        "Natural-language design specifications plus structured parameters",
        "Executed parametric B-Rep assemblies in a FreeCAD backend with iterative repair from solver diagnostics",
        "Closed-loop agent that iteratively selects skills from a hierarchical L0-L4 library, resolves typed geometric operations, executes them in a CAD kernel, and repairs from solver feedback; evaluated on bearing, press-machine, cooling-tower, manifold, and mould-core assembly tasks. No public repository is referenced in the v1 preprint.",
        [("arXiv", "https://arxiv.org/abs/2606.31252")],
        [],
    ),
    record(
        "asa-nqs-agent", "NQS-Agent", "physics",
        "Neural-network quantum state and variational Monte Carlo campaign management", "paper-only", "A3",
        "Running optimization campaigns: energy trajectories, checkpoints, and hyperparameter candidates",
        "Intervention decisions, adjusted learning-rate schedules, and anomaly-aware candidate rankings",
        "LangGraph-based agentic campaign manager for neural quantum-state hyperparameter optimization that decides when to stop, modify, or resume from safe checkpoints; on a Heisenberg model it outperformed baselines and surfaced competitive alternative architectures. The repository promised on publication was not public at verification, so access is paper-only pending release.",
        [("arXiv", "https://arxiv.org/abs/2606.30464")],
        [],
        aliases=["NQS-Agents"],
    ),
    record(
        "asa-metadatagenagent", "MetaDataGenAgent", "physics",
        "Metamaterials literature-to-database extraction", "paper-only", "A2",
        "Unstructured metamaterials literature, including text and figures",
        "Executable, simulation-validated metamaterial structure-response databases",
        "Multimodal multi-agent framework establishing a literature-to-simulation pipeline through coordinated specialized agents with iterative, feedback-driven validation; outputs were validated by generating electromagnetic functions such as beam deflection and holographic imaging. A data-extraction loop with simulation validation rather than a physical experiment loop; no code released at verification.",
        [("arXiv", "https://arxiv.org/abs/2606.22774")],
        [],
        aliases=["Autonomous Generation of Metamaterial Databases Based on Multimodal Agents"],
    ),
    record(
        "asa-vibe-calibration", "Vibe Calibration", "physics",
        "Autonomous superconducting quantum processor calibration", "paper-only", "A5",
        "A 112-qubit superconducting processor and decision-tree Skills packaging parameterized measurement code",
        "Autonomous calibration of 108 of 112 qubits in 4.7 hours with auditable Skill execution traces",
        "Skill-orchestrating language agent that autonomously brought up a real frequency-tunable transmon processor 4-5 times faster than manual bring-up, with expert agreement on 14 of 16 validated qubits. Disclosed human gates: Skills were distilled from expert tacit knowledge through a three-phase human-in-the-loop process, and the model was fine-tuned on validated trajectories before autonomous operation. A distinct team and system from k-agents.",
        [("arXiv", "https://arxiv.org/abs/2606.22376")],
        [],
        aliases=["Vibe Calibration: Autonomous Bring-up of a 112-Qubit Superconducting Quantum Processor by a Skill-Orchestrating Language Agent"],
    ),
    record(
        "asa-asys", "ASYS (Agentic Symbolic Search)", "physics",
        "Symbolic characterization of PDE solutions", "paper-only", "A2-A3",
        "PDE theory, problem constraints, and accumulated search experience",
        "Testable differentiable symbolic programs and interpretable analytical characterizations",
        "Prior-guided framework in which an agent converts PDE theory and constraints into differentiable symbolic programs refined by evolutionary search with gradient-based parameter fitting; it recovered known analytical solutions and produced new interpretable representations across five problems, including finite-time blow-up and free-boundary focusing. Computational discovery loop; no code released at verification.",
        [("arXiv", "https://arxiv.org/abs/2606.20467")],
        [],
        aliases=["ASYS", "Agentic Symbolic Search"],
    ),
    record(
        "asa-physcibench", "PhySciBench", "benchmark",
        "Deep-research agent evaluation in the physical sciences", "open-source", "B",
        "200 expert-curated physics and chemistry questions across six research-workflow task categories",
        "Deep-research agent performance scores per task category",
        "Benchmark for deep-research agents on real physical-science research workflows, introduced alongside DelveAgent, a modular multi-agent framework with an adaptive planning loop, dual-granularity memory, and hierarchical physics-grounded reflection. Evaluation code is Apache-2.0 with the dataset released separately on Hugging Face; the DelveAgent framework was announced but not released at verification.",
        [("arXiv", "https://arxiv.org/abs/2606.18648")],
        [("GitHub", "https://github.com/yigengjiang/physci-deepresearch")],
        aliases=["DelveAgent", "Deep Research in Physical Sciences"],
    ),
    record(
        "asa-lewron", "LeWRON", "physics",
        "Electroweak phase-transition analysis from a BSM Lagrangian", "open-source", "A3",
        "A beyond-Standard-Model Lagrangian or a literature target-paper specification",
        "Effective potentials, thermal histories, nucleation temperatures, gravitational-wave spectra, notes, and plots",
        "Fermilab single-author agentic pipeline that automates the full electroweak-phase-transition analysis, pairing a zero-temperature coding model with a reasoning auditor and an Explorer module for scans and plots. Human checkpoints after each major stage, where the user inspects artifacts and corrects assumptions, are built in. MIT.",
        [("arXiv", "https://arxiv.org/abs/2606.19425")],
        [("GitHub", "https://github.com/quarkquartet/LeWRON")],
        aliases=["Learning ElectroWeak phase tRansitiON"],
    ),
    record(
        "asa-phynex", "PhyNex", "physics",
        "Computational physics discovery over scorable tasks", "paper-only", "A3-A4",
        "A scorable computational-physics task plus domain-specific computational tools",
        "Iteratively improved solutions and scores across spectra prediction, circuit design, and quantum control",
        "Autonomous agent coupling LLM-guided search with domain computational tools to explore solution spaces of scorable tasks, reporting gains of 3.8% in spectral similarity, 15.0% in Max-Cut performance, and 5.9% in ergotropy across its three physics case studies. No public implementation was found during review.",
        [("arXiv", "https://arxiv.org/abs/2606.14266")],
        [],
    ),
    record(
        "asa-engineering-ai", "Engineering.ai", "physics",
        "Computational engineering design (aerodynamic, structural, acoustic)", "paper-only", "A3",
        "Natural-language engineering design specifications",
        "CAD geometries, meshes, CFD, structural and acoustic results, and optimized designs with file-mediated provenance",
        "A Chief Engineer agent coordinates aerodynamics, structural, acoustic, and optimization specialists over FreeCAD, Gmsh, OpenFOAM, and CalculiX, reporting complete success and zero mesh failures across more than 400 parametric UAV-wing configurations. Problem formulation, constraint definition, and interpretation remain human, and the simulation workflow closes computationally. No public code or platform link appears in the paper.",
        [("arXiv", "https://arxiv.org/abs/2511.00122")],
        [],
    ),
    record(
        "asa-omniqec", "OmniQEC", "physics",
        "Quantum error-correcting code discovery", "paper-only", "A3",
        "Code-family search spaces, hardware constraints, physical-qubit budgets, and LLM backends",
        "Candidate quantum error-correcting codes with screening metrics and circuit-level decoder validation",
        "An LLM orchestrator coordinates a dual-loop workflow - fast screening on code-level metrics and slower circuit-level validation with syndrome extraction and decoder evaluation - discovering hardware-friendly codes that outperform established baselines at given qubit budgets. Fully in-silico with human-launched runs; no code released at verification.",
        [("arXiv", "https://arxiv.org/abs/2607.25865")],
        [],
    ),
    record(
        "asa-agent-md-gcmc-md", "Agent-MD (GCMC-MD campaigns)", "physics",
        "Stateful molecular-simulation campaign agent (GCMC-MD)", "paper-only", "A3",
        "Campaign specification covering systems and a humidity or state schedule",
        "Completed segmented GCMC-MD campaigns with analysis, archiving, and state progression",
        "Selective LLM intervention with event-driven escalation: routine production runs proceed under deterministic rule-based control while LLM reasoning is invoked at campaign construction and at event-triggered review; demonstrated on 120 segmented cycles across 15 montmorillonite states. Distinct from the catalogued clinical AgentMD, which is a different system by different authors; no code release located.",
        [("arXiv", "https://arxiv.org/abs/2608.07637")],
        [],
    ),

    # ------------------------------------------------ cross-domain and benchmarks
    record(
        "asa-claude-science", "Claude Science", "crossdomain",
        "General scientific analysis workbench with life-science and chemistry presets", "platform", "A2",
        "Natural-language research direction, user data and code in persistent kernels, database connectors, HPC jobs",
        "Executed analyses, figures, database query results, and reproducible artifacts with code and environment history",
        "Anthropic research application in beta - a free desktop download, with enterprise access on request - that runs multi-step analyses under researcher direction over managed Python and R kernels, 60+ scientific database connectors, and cluster jobs over SSH, with an automatic background reviewer flagging citation, number, and figure-code mismatches as a disclosed verification layer. No launch date appears on the official pages, so none is recorded here.",
        [],
        [("Link", "https://claude.com/product/claude-science")],
        extra_sources=["https://www.anthropic.com/news"],
    ),
    record(
        "asa-chemworld", "ChemWorld", "benchmark",
        "Programmable simulated chemical worlds for agent evaluation", "open-source", "B",
        "Agent-issued typed chemical operations against a compiled world: reactions, separations, instrument use",
        "Public observations, evaluator-side full state trajectories, and exactly replayable audit-trailed episodes",
        "MIT environments in which evaluator-controlled hidden chemical laws can be varied one at a time while the agent-facing task stays fixed, supporting deterministic replay and fail-closed compilation, preflight, and commit gates. Simulation closure only, with no physical instruments; researchers author world compositions and freeze protocols before agent runs.",
        [("arXiv", "https://arxiv.org/abs/2608.10792")],
        [("GitHub", "https://github.com/sunyrain/ChemWorld-Public")],
    ),
    record(
        "asa-mdarena", "MDArena", "benchmark",
        "Molecular-dynamics workflow evaluation for coding agents", "open-source", "B",
        "50 containerized tasks spanning 29 molecular systems and 14 research protocols, driven through a CLI harness",
        "Automated verifier scores: binary Strict-Pass@1, deterministic correctness reward, and process reward per task",
        "MIT benchmark of coding agents on realistic multi-step molecular-dynamics workflows - system preparation, parameterization, trajectory analysis, umbrella sampling, and free-energy protocols across GROMACS, AMBER, OpenMM, and PLUMED - drawn from active research projects. The best evaluated configuration reaches 24 of 50 on Strict-Pass@1; membrane-protein preparation and alchemical free-energy setup remain essentially unsolved.",
        [("arXiv", "https://arxiv.org/abs/2608.02642")],
        [("GitHub", "https://github.com/weitse-hsu/MDArena")],
    ),
    record(
        "asa-shinkaevolve", "ShinkaEvolve", "crossdomain",
        "Sample-efficient program and algorithm discovery", "open-source", "A3",
        "Task specification, an initial program, and a fitness or evaluation program; runs locally or on Slurm",
        "Evolved programs and solutions, solution archives with island-based knowledge transfer, and run monitoring",
        "Sakana AI Apache-2.0 framework using an LLM ensemble as mutation operators over evolving program populations, reporting a new state-of-the-art circle-packing solution in roughly 150 samples alongside applications to mathematical reasoning, competitive programming, mixture-of-experts load balancing, and circuit design. The user defines the problem and the evaluation function; the evolutionary loop then closes computationally with no physical loop.",
        [("arXiv", "https://arxiv.org/abs/2509.19349")],
        [("GitHub", "https://github.com/SakanaAI/ShinkaEvolve")],
    ),
    record(
        "asa-agon", "Agon", "crossdomain",
        "Omnidisciplinary autonomous research orchestration", "open-source", "A3",
        "Small natural-language starting research topics, with no human-written experimental code",
        "Generated experimental code, executed experiment iterations, and research artifacts with in-workflow validation",
        "Research orchestrator built on a 'Prompt Economy' of six principles including Zero-Code and Massive Parallelism, which ran 444 loop iterations across more than ten disciplines and validates whatever can be checked inside the workflow. Disclosed human gates: humans choose the questions, judge the evidence, and act as the final adversary who can block any artifact from advancing. Computational closure only. MIT, implemented as a coding-agent plugin.",
        [("arXiv", "https://arxiv.org/abs/2606.24177")],
        [("GitHub", "https://github.com/AutoResearch-Factory/Agon")],
    ),
    record(
        "asa-sciagentarena", "SciAgentArena", "benchmark",
        "Biomedical agent tasks from molecular to patient scale", "source-available", "B",
        "Agent submissions through a web interface against roughly 200 stepwise-verified tasks in seven families",
        "Standardized scores, stepwise verification results, and a community leaderboard",
        "Living benchmark spanning drug discovery, single-cell and spatial omics, EHR modeling, and clinical genetics in an interactive, agent-agnostic environment, shipping 16 agent implementations. The repository was public but carried no licence file at verification, so it is not classified as open-source; the access label should be revisited if a licence is added.",
        [("arXiv", "https://arxiv.org/abs/2606.12736")],
        [
            ("GitHub", "https://github.com/HelloWorldLTY/SciAgentArena"),
            ("Project", "https://sciagentarena.github.io/"),
            ("Hugging Face", "https://huggingface.co/datasets/iLOVE2D/SciAgentArena"),
        ],
        aliases=["Benchmarking AI Agents for Addressing Scientific Challenges Across Scales"],
        access_evidence=unlicensed(
            "https://github.com/HelloWorldLTY/SciAgentArena",
            "None: public repository with no licence file at verification (2026-08-13)",
        ),
    ),
    record(
        "asa-openscience-synthetic-sciences", "OpenScience (Synthetic Sciences)", "crossdomain",
        "Open-source autonomous research workbench", "open-source", "A4",
        "A research goal plus user-supplied model or API keys; model-agnostic across commercial and open-weight backends",
        "Literature review, hypotheses, written and executed code, database queries, analyses, and written-up results",
        "Apache-2.0 research workbench with a browser workspace UI that runs the full research loop from a stated goal, with critique and literature-review sub-agents, 290+ skills, and roughly 30 scientific-database integrations; positioned as an open alternative to hosted science workbenches. No default human checkpoints are disclosed beyond the user-set goal. Verified independent of the same-day ai4s-research/open-science: disjoint contributors, a different stack, and neither is a fork. No paper.",
        [],
        [("GitHub", "https://github.com/synthetic-sciences/openscience")],
        aliases=["OpenScience", "synsci/openscience"],
    ),
    record(
        "asa-open-science-desktop", "Open Science Desktop", "crossdomain",
        "Local-first desktop autonomous research workbench", "open-source", "A3-A4",
        "Research goal, local files and data, and model-provider credentials or custom endpoints",
        "Exploration documents, literature surveys, experiment designs with executable code and results, and paper drafts",
        "MIT-licensed desktop application with a bundled coding-agent sidecar runtime; stage skills for exploration, literature survey, experiment suite, and paper writing each emit inspectable artifacts with append-only provenance logs, keeping the human in the loop between stages. GitHub reports NOASSERTION only because the MIT licence appends a third-party-skills note. Verified independent of the same-day synthetic-sciences/openscience; the maintainers are pseudonymous.",
        [],
        [
            ("GitHub", "https://github.com/ai4s-research/open-science"),
            ("Zenodo", "https://doi.org/10.5281/zenodo.21351225"),
        ],
        aliases=["ai4s-research/open-science", "AI4S Workbench"],
    ),
    record(
        "asa-mechanist", "Mechanist", "crossdomain",
        "Autonomous discovery of mechanisms in AI systems", "paper-only", "A3-A4",
        "Research questions about model behaviour, a large interpretability knowledge graph, and analysis methods",
        "Generated and validated mechanism hypotheses, discovered model behaviours, and control interventions",
        "Agentic system that uses AI as a scientific instrument for the science of AI, working over a knowledge graph of roughly 13,000 interpretability papers and a library of 32 foundational analysis methods. The preprint is flagged as work in progress, no code is released, and author affiliations could not be verified from the abstract page.",
        [("arXiv", "https://arxiv.org/abs/2608.12036")],
        [],
    ),
    record(
        "asa-evigraph", "EviGraph", "crossdomain",
        "Evidence-graph-validated autonomous research", "paper-only", "A3-A4",
        "A research problem or goal plus literature and experimental context",
        "A typed evidence graph with validated chains, executed experiments, and manuscript drafts grounded in them",
        "Framework targeting unsupported claims and cross-stage inconsistency in autonomous research systems: it validates evidence chains across problem, gap, hypothesis, experiment, finding, and claim nodes and regenerates weak portions before writing, reporting a 40.19% claim-support improvement over the strongest baseline and 87.73% experimental-data consistency. No public code was found.",
        [("arXiv", "https://arxiv.org/abs/2608.04738")],
        [],
    ),
    record(
        "asa-aria-coreweave", "ARIA (CoreWeave AI Research and Iteration Agent)", "crossdomain",
        "Autonomous machine-learning experiment analysis and iteration", "platform", "A3",
        "Experiment data across thousands of runs and production traces, plus training infrastructure reachable by launch",
        "Performance-driver analyses, visualizations, hypotheses, launched experiments, and next-iteration recommendations",
        "CoreWeave and Weights & Biases agent in public preview that closes the machine-learning iteration loop - analysing runs, forming hypotheses, designing and launching experiments, evaluating against baselines, and recommending the next move - with a disclosed human gate: researchers approve launches.",
        [],
        [
            ("Link", "https://wandb.ai/site/agent/"),
            ("Announcement", "https://www.coreweave.com/blog/the-ai-loop-launch-day-is-day-one"),
        ],
        aliases=["AI Research and Iteration Agent", "CoreWeave ARIA", "W&B ARIA"],
    ),
    record(
        "asa-k-dense-scientific-agent-skills", "K-Dense scientific-agent-skills", "crossdomain",
        "Scientific-agent skills library", "open-source", "A2",
        "Agent tasks requiring scientific skills or scientific database access",
        "Executable skill invocations and queries across 100+ scientific databases",
        "MIT-licensed Agent Skills library of 158 skills across bioinformatics, cheminformatics, clinical research, and machine learning, compatible with common coding agents and the open Agent Skills standard. A component library included under the ToolUniverse and ChemMCP precedent, not a standalone agent.",
        [],
        [("GitHub", "https://github.com/K-Dense-AI/scientific-agent-skills")],
        aliases=["scientific-agent-skills", "K-Dense Scientific Agent Skills"],
    ),
]


def load(path: Path) -> list:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: list) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    records = load(DATA)
    by_id = {item["id"]: item for item in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate IDs exist before migration")

    known_ids = set(by_id) | {entry["id"] for entry in load(DEPRECATED)}
    colliding = sorted({item["id"] for item in NEW_RECORDS} & (known_ids - set(REMOVE_IDS)))
    reruns = {item["id"] for item in NEW_RECORDS} & set(by_id)
    if colliding and colliding != sorted(reruns):
        raise SystemExit(f"new IDs collide with existing or tombstoned IDs: {colliding}")

    removed = sorted(REMOVE_IDS & set(by_id))
    records = [item for item in records if item["id"] not in REMOVE_IDS]
    by_id = {item["id"]: item for item in records}

    missing_updates = sorted(set(UPDATES) - set(by_id))
    if missing_updates:
        raise SystemExit(f"update targets missing: {missing_updates}")
    for record_id, patch in UPDATES.items():
        by_id[record_id].update(patch)

    added = 0
    replaced = 0
    for item in NEW_RECORDS:
        record_id = item["id"]
        if record_id in by_id:
            by_id[record_id].clear()
            by_id[record_id].update(item)
            replaced += 1
        else:
            records.append(item)
            by_id[record_id] = item
            added += 1

    if len({item["id"] for item in records}) != len(records):
        raise SystemExit("duplicate IDs after migration")
    display_names = [item["name"].casefold().strip() for item in records]
    if len(set(display_names)) != len(display_names):
        raise SystemExit("exact duplicate display names after migration")

    deprecated = load(DEPRECATED)
    deprecated_ids = {entry["id"] for entry in deprecated}
    tombstoned = 0
    for entry in TOMBSTONES:
        if entry["id"] not in deprecated_ids:
            deprecated.append(entry)
            tombstoned += 1

    write(DATA, records)
    write(DEPRECATED, deprecated)
    print(
        f"removed={len(removed)} tombstoned={tombstoned} updated={len(UPDATES)} "
        f"added={added} replaced={replaced} total={len(records)}"
    )


if __name__ == "__main__":
    main()
