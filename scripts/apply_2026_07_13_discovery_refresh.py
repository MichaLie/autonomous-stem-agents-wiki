#!/usr/bin/env python3
"""Apply the separately discovered and adversarially cross-checked 2026-07-13 refresh.

The migration is idempotent and local to the protected FAIR preview. It does
not publish. Held and rejected candidates are documented in the audit note.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "agents_final.json"
DATE = "2026-07-13"


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
) -> dict:
    item = {
        "id": record_id,
        "date_added": DATE,
        "verified": DATE,
        "name": name,
        "category": category,
        "domain": domain,
        "access": access,
        "autonomy": autonomy,
        "inputs": inputs,
        "outputs": outputs,
        "notes": notes,
        "paper_links": links(papers),
        "repo_links": links(repos),
    }
    if aliases:
        item["aliases"] = aliases
    return item


REMOVE_IDS = {
    "asa-futurehouse-edison-agents",  # redundant umbrella over Robin/Edison-specific rows
    "asa-kosmos-radiation-biology-evaluation",  # case-study audit, not reusable agent/harness
    "asa-a-mobile-robotic-chemist",  # exact duplicate of the Liverpool/Cooper 2020 record
    "asa-biomedtools",  # tool registry/infrastructure, not an autonomous research agent
    "asa-atlas",  # Bayesian optimizer component, not an agent or benchmark
    "asa-gryffin",  # Bayesian optimizer algorithm, not an agent or benchmark
}


UPDATES: dict[str, dict] = {
    "asa-microgrowagents": {
        "access": "paper-only",
        "repo_links": [],
        "notes": "Modular cultivation/media-design system combining knowledge graphs, metabolic modeling, and statistical design. Its author-owned repository was checked in a separate audit lane but returned repository-not-found during the final link gate, so no currently public implementation is claimed.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-google-ai-co-scientist": {
        "access": "paper-only",
        "repo_links": [],
        "notes": "Google Research multi-agent hypothesis-generation system evaluated in biomedical research. No official public implementation was confirmed; community reimplementations are not treated as evidence for the Google system.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-scienceagentbench": {
        "notes": "Benchmark for agents that generate and execute scientific-analysis code. The official repository released a verified dataset/artifact revision on 30 April 2026 to mitigate false negatives and directs users to the Hugging Face verified split and benchmark_verified.zip.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-flowagent": {
        "domain": "Autonomous bioinformatics workflow planning, execution, recovery, and interpretation",
        "inputs": "Bioinformatics goals, datasets, local/HPC environments, tool documentation, and workflow failures",
        "outputs": "Executed shell/Nextflow/Snakemake workflows, QC reports, checkpointed recovery, interpretations, and final results",
        "paper_links": links([
            ("FlowAgent paper", "https://arxiv.org/abs/2504.03847"),
            ("FlowBench bioRxiv", "https://www.biorxiv.org/content/10.64898/2026.06.12.731844v1"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-drugagent": {
        "access": "paper-only",
        "repo_links": [],
        "notes": "Multi-agent drug-discovery workflow described in arXiv:2411.15692. The previously cited repository was a third-party reconstruction, not an author-owned release; no official runnable implementation was confirmed.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-cellvoyager": {
        "access": "open-source",
        "autonomy": "A4",
        "paper_links": links([
            ("Nature Methods", "https://doi.org/10.1038/s41592-026-03029-6"),
        ]),
        "repo_links": links([
            ("GitHub", "https://github.com/zou-group/CellVoyager"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-bioagents": {
        "access": "open-source",
        "autonomy": "A2",
        "paper_links": links([
            ("Scientific Reports", "https://doi.org/10.1038/s41598-025-25919-z"),
        ]),
        "repo_links": links([
            ("GitHub", "https://github.com/microsoft/bioinformagus"),
        ]),
        "notes": "Microsoft multi-agent bioinformatics workflow-design and troubleshooting assistant with limited code generation; it does not autonomously execute complete scientific workflows. Official implementation is MIT-licensed.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-hypobench": {
        "access": "open-source",
        "repo_links": links([
            ("GitHub", "https://github.com/ChicagoHAI/HypoBench-code"),
            ("Project", "https://chicagohai.github.io/HypoBench/"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-a-lab-berkeley": {
        "outputs": "Autonomously synthesized 36 compounds from 57 targets in the corrected Nature record, with phase identification and campaign data",
        "notes": "Berkeley A-Lab closed the inorganic-synthesis loop across planning, robotics, characterization, and active learning. Nature issued an author correction on 19 January 2026 revising the campaign result to 36 compounds from 57 targets; novelty remains separately contested and is not asserted here.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-alphaflow": {
        "autonomy": "A5",
        "repo_links": links([
            ("GitHub", "https://github.com/AbolhasaniLab/AlphaFlow"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-synbot-ai-driven-robotic-chemist": {
        "autonomy": "A5",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-crest-copilot-for-real-world-experimental-scientists": {
        "autonomy": "A5",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-k-agents-self-driving-labs-for-quantum-computing": {
        "category": "physics",
        "access": "lab-gated",
        "autonomy": "A5",
        "paper_links": links([
            ("Patterns", "https://doi.org/10.1016/j.patter.2025.101372"),
            ("arXiv", "https://arxiv.org/abs/2412.07978"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-mada": {
        "access": "paper-only",
        "autonomy": "A4",
        "notes": "LLNL/NNSA computational agent that couples LLM reasoning, multiphysics codes, and ML surrogates on restricted HPC systems to explore inertial-confinement-fusion capsule designs. It does not operate a physical fusion experiment.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-dr-sai": {
        "access": "paper-only",
        "notes": "Computational agent for BESIII data analysis, simulation, reconstruction, and statistics. It does not control the collider or detector, so physical-lab gating is not claimed.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-honegumi": {
        "autonomy": "A1-A2",
        "notes": "Interactive Bayesian-optimization assistant that generates optimization skeleton code; it does not independently execute end-to-end scientific workflows and is not a benchmark.",
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-autolabs": {
        "paper_links": links([
            ("Scientific Reports", "https://doi.org/10.1038/s41598-026-45593-z"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-master": {
        "paper_links": links([
            ("npj Computational Materials", "https://doi.org/10.1038/s41524-026-02139-1"),
        ]),
        "date_modified": DATE,
        "verified": DATE,
    },
    "asa-matterix": {
        "paper_links": links([
            ("Nature Computational Science", "https://doi.org/10.1038/s43588-025-00924-4"),
        ]),
        "notes": "Agentic materials workflow with simulation/digital-twin closure and demonstrated sim-to-real transfer; it is not an autonomous physical laboratory.",
        "date_modified": DATE,
        "verified": DATE,
    },
}


NEW_RECORDS: list[dict] = [
    # Cross-domain systems and benchmarks.
    record(
        "asa-aira-dojo", "AIRA-dojo", "crossdomain",
        "Autonomous machine-learning research and experimentation", "open-source", "A4",
        "MLE-bench task specification, datasets, compute budget, and model backend",
        "Iteratively searched, executed, and scored ML solutions with full trajectories",
        "Meta/UCL framework formalizing research agents as search policies over candidate solutions, including greedy, MCTS, and evolutionary search. Public code is CC BY-NC 4.0 and therefore non-commercial.",
        [("arXiv", "https://arxiv.org/abs/2507.02554"), ("OpenReview", "https://openreview.net/forum?id=RwfrdKSgCE")],
        [("GitHub", "https://github.com/facebookresearch/aira-dojo")],
    ),
    record(
        "asa-rd-agent", "R&D-Agent (RD-Agent)", "crossdomain",
        "Autonomous data-driven AI research and development", "open-source", "A4",
        "Data-science or ML task, datasets, evaluation feedback, and model backends",
        "Research hypotheses, implemented solutions, experiments, and iteratively improved models",
        "Microsoft Research dual-agent framework in which a Researcher proposes ideas from performance feedback and a Developer implements and refines code across parallel evolving traces. MIT-licensed.",
        [("arXiv", "https://arxiv.org/abs/2505.14738")],
        [("GitHub", "https://github.com/microsoft/RD-Agent")],
        aliases=["RD-Agent"],
    ),
    record(
        "asa-mle-bench", "MLE-bench", "benchmark",
        "Machine-learning engineering agents", "open-source", "B",
        "Prepared Kaggle competition environments and agent submissions",
        "Competition scores, medal rates, grading reports, and agent trajectories",
        "OpenAI benchmark covering 75 real-world ML engineering competitions. MIT-licensed code, task preparation, and graders; competition data retain Kaggle/provider terms. The official leaderboard is public but paused new submissions on 24 April 2026 while comparison procedures are revised.",
        [("arXiv", "https://arxiv.org/abs/2410.07095")],
        [("GitHub", "https://github.com/openai/mle-bench")],
    ),
    record(
        "asa-re-bench", "RE-Bench", "benchmark",
        "Frontier AI research-and-development agents", "open-source", "B",
        "Open-ended ML research-engineering environments with fixed time budgets",
        "Objective task scores, human-expert comparisons, and agent trajectories",
        "METR benchmark comparing frontier agents with human experts on realistic long-horizon AI R&D tasks. MIT-licensed suite with protected solution material to limit contamination.",
        [("arXiv", "https://arxiv.org/abs/2411.15114")],
        [("GitHub", "https://github.com/METR/RE-Bench")],
    ),
    record(
        "asa-researchclawbench", "ResearchClawBench", "benchmark",
        "End-to-end autonomous scientific research across ten disciplines", "open-source", "B",
        "Raw data, related literature, and a research goal with the target paper hidden",
        "Executed analyses, figures, publication-style reports, and expert-rubric scores",
        "Forty real-science tasks requiring agents to work from raw data to research reports; includes a lightweight ResearchHarness baseline. MIT-licensed public repository.",
        [("arXiv", "https://arxiv.org/abs/2606.07591")],
        [("GitHub", "https://github.com/InternScience/ResearchClawBench"), ("Hugging Face", "https://huggingface.co/datasets/InternScience/ResearchClawBench")],
    ),
    record(
        "asa-deepresearch-bench", "DeepResearch Bench / DeepResearch Bench II", "benchmark",
        "Long-form evidence-grounded research agents across many fields", "open-source", "B",
        "Expert-authored research tasks requiring web evidence and long-form reports",
        "Report-quality, citation-grounding, information-recall, analysis, and presentation scores",
        "Benchmark family for deep-research agents. The original provides PhD-level tasks and RACE/FACT evaluation; Bench II adds expert-derived binary rubrics. Both official codebases are Apache-2.0; individual task data include multiple Creative Commons terms.",
        [("arXiv I", "https://arxiv.org/abs/2506.11763"), ("arXiv II", "https://arxiv.org/abs/2601.08536")],
        [("GitHub I", "https://github.com/Ayanami0730/deep_research_bench"), ("GitHub II", "https://github.com/imlrz/DeepResearch-Bench-II")],
        aliases=["DeepResearch Bench", "DeepResearch Bench II"],
    ),
    record(
        "asa-prescience", "PreScience", "benchmark",
        "Forecasting scientific contributions and research trajectories", "open-source", "B",
        "Temporally aligned paper, author, reference, and citation histories",
        "Collaborator, prior-work, contribution, and impact forecasts plus science-trajectory simulations",
        "Ai2/UChicago benchmark built from large-scale paper histories and a scientific graph. It evaluates forecasting and simulated scientific trajectories rather than laboratory action. Code is Apache-2.0 and data are ODC-BY 1.0.",
        [("arXiv", "https://arxiv.org/abs/2602.20459")],
        [("GitHub", "https://github.com/allenai/prescience"), ("Hugging Face", "https://huggingface.co/datasets/allenai/prescience")],
    ),
    record(
        "asa-mle-dojo", "MLE-Dojo", "benchmark",
        "Interactive machine-learning engineering environments", "open-source", "B",
        "Consolidated Kaggle tasks, agent actions, execution environments, and competition feedback",
        "Comparable interactive MLE trajectories and competition outcomes",
        "NeurIPS 2025 environment for evaluating machine-learning engineering agents. Code is MIT; benchmark data are non-commercial and each Kaggle competition retains its own terms.",
        [("arXiv", "https://arxiv.org/abs/2505.07782")],
        [("GitHub", "https://github.com/MLE-Dojo/MLE-Dojo")],
    ),

    # Biology/medicine systems and benchmarks.
    record(
        "asa-automedbench", "AutoMedBench", "benchmark",
        "Autonomous medical-AI research workflows", "open-source", "B",
        "Medical imaging and multimodal research task capsules",
        "Executable pipelines, predictions, and stage-level workflow scores",
        "Benchmark of planning, setup, validation, inference, and submission across 48 sandboxed tasks and seven tracks. MIT-licensed harness; source datasets retain provider licences.",
        [("arXiv", "https://arxiv.org/abs/2606.01961")],
        [("GitHub", "https://github.com/AutoMedBench/AutoMedBench"), ("Project", "https://automedbench.github.io/")],
    ),
    record(
        "asa-biomedarena", "BioMedArena", "benchmark",
        "Biomedical deep-research agent evaluation", "open-source", "B",
        "Registered benchmarks, model backends, tools, and harness configurations",
        "Scores, execution traces, and comparable agent evaluations",
        "MIT-licensed reproducible toolkit spanning benchmark loading, tool exposure, agent execution, context management, and scoring.",
        [("arXiv", "https://arxiv.org/abs/2605.06177")],
        [("GitHub", "https://github.com/AI-in-Health/BioMedArena")],
    ),
    record(
        "asa-flowbench-bioinformatics", "FlowBench (agentic bioinformatics)", "benchmark",
        "Autonomous bioinformatics workflow execution", "open-source", "B",
        "Bioinformatics tasks, datasets, workflow specifications, and induced failures",
        "Planning, recovery, interpretation, and output-fidelity scores",
        "Agentic-bioinformatics benchmark sharing FlowAgent's GPL-3.0 repository and reproducible corpus. Distinct from the unrelated 2024 benchmark also named FlowBench and from the FlowAgent system row.",
        [("bioRxiv", "https://doi.org/10.64898/2026.06.12.731844")],
        [("GitHub", "https://github.com/EnteloBio/flowagent")],
    ),
    record(
        "asa-autozyme", "AutoZyme", "biology",
        "Autonomous bioinformatics software optimization", "open-source", "A3",
        "Scientific software functions, tests, datasets, and optimization objectives",
        "Benchmarked, output-preserving optimized code and packaged patches",
        "MIT-licensed workflow that iteratively profiles, edits, tests, and retains performance improvements. It optimizes scientific software rather than autonomously generating biological hypotheses.",
        [("bioRxiv", "https://doi.org/10.64898/2026.06.12.731250")],
        [("GitHub", "https://github.com/ElliotXie/autozyme"), ("Project", "https://autozyme.com/"), ("Dataset", "https://huggingface.co/datasets/elliotxie/autozyme-datasets")],
    ),
    record(
        "asa-simple-agent-optimization-biomedical-imaging", "Simple Agent Optimization (biomedical imaging)", "biology",
        "Autonomous biomedical-imaging workflow optimization", "open-source", "A3",
        "Imaging datasets, validation metrics, and wrapped scientific models",
        "Iteratively generated preprocessing/postprocessing code and optimized workflows",
        "CVPR 2026 system for Polaris, Cellpose, and MedSAM workflows. Runnable implementation and tests are Apache-2.0.",
        [("arXiv", "https://arxiv.org/abs/2512.06006"), ("CVPR", "https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_Simple_Agents_Outperform_Experts_in_Biomedical_Imaging_Workflow_Optimization_CVPR_2026_paper.pdf")],
        [("GitHub", "https://github.com/xuefei-wang/simple-agent-opt")],
    ),
    record(
        "asa-medgenesis", "MedGenesis", "biology",
        "Autonomous clinical and translational research", "paper-only", "A4",
        "Research questions, clinical datasets, evidence resources, and institutional data handles",
        "Hypotheses, cohort analyses, evidence products, reproductions, and reports",
        "Eight-agent in-silico closed loop with a large skill library. Some functions depend on protected EHRs and institutional wrappers; code and benchmarks are promised only upon publication, and the demonstrated wet-lab handoff does not justify A5.",
        [("medRxiv", "https://doi.org/10.64898/2026.06.14.26355612")],
        [],
    ),
    record(
        "asa-behaveagent", "BehaveAgent", "biology",
        "Autonomous multimodal organism-behavior analysis", "paper-only", "A3",
        "Behavioral videos and research questions",
        "Tracking, temporal segmentation, generated analyses, and reports",
        "Cross-species behavior-analysis system that selects strategies, generates and executes analysis code, and reports results. The official repository is MIT-licensed but explicitly says end-user code is still forthcoming, so it is not classified as runnable open source.",
        [("bioRxiv", "https://doi.org/10.1101/2025.05.15.653585")],
        [("Project repository", "https://github.com/LiuLab-Bioelectronics-Harvard/BehaveAgent")],
    ),

    # Chemistry/materials and physics/engineering systems.
    record(
        "asa-autonomous-mobile-robots-exploratory-synthesis", "Autonomous mobile robots for exploratory synthetic chemistry", "chemistry",
        "Modular mobile-robot exploratory synthesis", "lab-gated", "A5",
        "Scientist-selected building blocks, reaction space, and general success criteria",
        "Robot-executed synthesis, NMR/UPLC-MS interpretation, reproducibility checks, and functional assays",
        "Distinct 2024 multi-robot successor to the 2020 Liverpool mobile robotic chemist. It ran a real multi-instrument physical workflow for four days; humans handled restocking and final anomaly interpretation. Author-owned control artifacts and workflow data are public on Zenodo.",
        [("Nature", "https://doi.org/10.1038/s41586-024-08173-7")],
        [("Decision/instrument code", "https://doi.org/10.5281/zenodo.11209893"), ("Data/workflows", "https://doi.org/10.5281/zenodo.11197259")],
    ),
    record(
        "asa-flex-cat", "Flex-Cat", "chemistry",
        "Autonomous homogeneous-catalyst discovery and optimization", "lab-gated", "A5",
        "Ligand library, reaction-variable ranges, and regioselectivity/turnover objectives",
        "Robotically executed pressurized reactions, adaptive Bayesian campaigns, catalyst-condition maps, and scale-up validation",
        "Glovebox-integrated physical closed loop completing 680 experiments across three campaigns. Public Zenodo materials include data, logs, digital twin, and optimization code under CC BY 4.0; the paper-declared GitHub was unavailable at verification time.",
        [("Nature Communications", "https://doi.org/10.1038/s41467-026-74425-x")],
        [("Zenodo", "https://doi.org/10.5281/zenodo.18930287")],
    ),
    record(
        "asa-robochem-flex", "RoboChem-Flex", "chemistry",
        "Modular self-driving reaction-optimization laboratory", "lab-gated", "A5",
        "Reaction, controllable parameter space, analytical method, and optimization target",
        "Automated experiments, online analysis, Bayesian optimization, and optimized conditions",
        "Real physical closed-loop reaction-optimization platform demonstrated across multiple chemistry cases; human-in-the-loop mode is optional. Apache-2.0 repository includes control software, firmware, CAD/PCB assets, and examples.",
        [("Nature Synthesis", "https://doi.org/10.1038/s44160-026-01053-0")],
        [("GitHub", "https://github.com/Noel-Research-Group/Robochem_Flex")],
    ),
    record(
        "asa-self-driving-pvd", "Self-driving physical vapor deposition system", "chemistry",
        "Autonomous sample-adaptive thin-film deposition", "lab-gated", "A5",
        "Requested optical properties, deposition variables, and per-sample calibration measurements",
        "Robotically deposited silver films, in-situ spectra, updated models, and sample-specific decisions",
        "Genuine autonomous physical PVD loop demonstrated across 72 samples without human intervention during campaigns. Code and data are available only from the authors on request.",
        [("npj Computational Materials", "https://doi.org/10.1038/s41524-025-01805-0")],
        [], aliases=["Self-driving PVD system"],
    ),
    record(
        "asa-sparksmatter", "SparksMatter", "chemistry",
        "Autonomous in-silico inorganic-materials discovery", "open-source", "A4",
        "Materials objective, Materials Project data, generative/predictive tools, and validation constraints",
        "Candidate structures, simulated-property evidence, critiques, validation plans, and research reports",
        "Apache-2.0 computational system that generates candidates and executes generative-model and surrogate workflows. DFT and physical synthesis are proposed follow-ups rather than performed closure. Distinct from the protein-design system Sparks.",
        [("npj Computational Materials", "https://doi.org/10.1038/s41524-026-02205-8")],
        [("GitHub", "https://github.com/lamm-mit/SparksMatter")],
    ),
    record(
        "asa-ai-x-ray-scientist", "AI X-ray Scientist", "physics",
        "Autonomous synchrotron diffraction alignment", "lab-gated", "A5",
        "Crystal information, beamline state, detector images, and experiment goal",
        "Reflection selection, motor-scan commands, anomaly diagnosis, and crystal-orientation matrix",
        "Developed in a virtual six-circle diffractometer and transferred to the real SSRL BL17-2 beamline, where it aligned crystals and adapted to an unexpected motor offset. A human relayed commands as a passive safety intermediary. Code MIT; data CC BY 4.0.",
        [("Nature Machine Intelligence", "https://doi.org/10.1038/s42256-026-01261-5")],
        [("Code", "https://doi.org/10.5281/zenodo.20017991"), ("Data", "https://doi.org/10.5281/zenodo.20017861")],
    ),
    record(
        "asa-calms-instrument-agents", "CALMS scientific-instrument agents", "physics",
        "Teachable multi-agent operation of scientific user-facility instruments", "lab-gated", "A5",
        "User task, instrument APIs/protocols, multimodal observations, and optional human corrections",
        "Generated and executed instrument workflows, persistent operational memories, and experiment results",
        "Human-teachable physical agents validated on an X-ray nanoprobe beamline and an autonomous materials-design robot. They close real instrument loops but are not fully self-motivated scientists. DOE software record identifies BSD-3-Clause.",
        [("npj Computational Materials", "https://doi.org/10.1038/s41524-026-02005-0")],
        [("GitHub", "https://github.com/AdvancedPhotonSource/CALMS/tree/sdl_agents"), ("DOE software record", "https://doi.org/10.11578/dc.20240410.1")],
    ),
    record(
        "asa-argoloom", "ArgoLOOM", "physics",
        "Cross-frontier fundamental-physics computation", "open-source", "A3",
        "Physics goal, theory constraints, literature knowledge base, and tool configurations",
        "Planned and executed cosmology, collider, deep-inelastic-scattering, and nuclear-physics analyses",
        "MIT-licensed computational pilot spanning several fundamental-physics domains. Demonstrations are small-scale and do not include physical experiment control.",
        [("arXiv", "https://arxiv.org/abs/2510.02426")],
        [("GitHub", "https://github.com/ML4HEP-Theory/ArgoLOOM")],
    ),
    record(
        "asa-pde-agents", "PDE-Agents", "physics",
        "Knowledge-graph-grounded autonomous PDE/FEM simulation", "open-source", "A3",
        "Natural-language simulation task, material data, scientific references, and prior-run graph",
        "Validated DOLFINx simulations, analyses, provenance-linked records, and reports",
        "MIT-licensed, containerized computational system with Simulation, Analytics, and Database agents. It performs runtime validation and debugging but does not control physical experiments.",
        [("arXiv", "https://arxiv.org/abs/2606.07850")],
        [("GitHub", "https://github.com/MatPro-IFE/pde-agents")],
    ),
    record(
        "asa-llmsat", "LLMSat", "physics",
        "Goal-oriented autonomous spacecraft control", "open-source", "A3",
        "Mission goal, spacecraft state, available actions, and operational constraints",
        "Mission plans, replanning decisions, and simulated spacecraft commands",
        "MIT-licensed implementation evaluated entirely in Kerbal Space Program. It demonstrates simulated spacecraft closure and has not been flight-tested.",
        [("arXiv", "https://arxiv.org/abs/2405.01392")],
        [("GitHub", "https://github.com/DM1122/LLMSat")],
    ),
]


def main() -> None:
    records = json.loads(DATA.read_text())
    by_id = {item["id"]: item for item in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate IDs exist before migration")

    missing_removals = sorted(REMOVE_IDS - set(by_id))
    if missing_removals and not all(item in {row["id"] for row in NEW_RECORDS} for item in missing_removals):
        # A repeat run is allowed after the rows have already been removed.
        already_migrated = all(item not in by_id for item in REMOVE_IDS)
        if not already_migrated:
            raise SystemExit(f"some removal targets missing unexpectedly: {missing_removals}")
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

    DATA.write_text(json.dumps(records, indent=1, ensure_ascii=False) + "\n")
    print(f"removed={len(REMOVE_IDS)} updated={len(UPDATES)} added={added} replaced={replaced} total={len(records)}")


if __name__ == "__main__":
    main()
