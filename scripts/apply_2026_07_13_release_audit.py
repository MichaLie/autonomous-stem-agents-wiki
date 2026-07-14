#!/usr/bin/env python3
"""Apply the 2026-07-13 release-audit corrections idempotently."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "agents_final.json"
TOMBSTONES = ROOT / "deprecated_ids.json"
DATE = "2026-07-13"

def links(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"label": label, "url": url} for label, url in items]

def apply() -> None:
    records = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in records}

    by_id["asa-flowagent"]["paper_links"][0] = {
        "label": "FlowAgent bioRxiv", "url": "https://doi.org/10.1101/2025.03.06.641728"
    }

    remove_b = {
        "asa-agentrxiv": "A3", "asa-chemmcp": "A2", "asa-evomaster": "A4",
        "asa-eurekagent": "A4", "asa-scbasecount-sragent": "A3",
        "asa-chemspace-copilot": "A2", "asa-nanominer": "A2",
        "asa-dive": "A2", "asa-jutulgpt": "A3",
    }
    for record_id, autonomy in remove_b.items():
        by_id[record_id]["autonomy"] = autonomy

    for record_id in ("asa-bioplanner", "asa-gravity-bench"):
        by_id[record_id].update(category="benchmark", autonomy="B")

    by_id["asa-scitrace"].update(
        category="crossdomain",
        domain="Trajectory-aware safety framework integrated into scientific-agent pipelines",
        autonomy="A4",
        inputs="Scientific-agent reasoning trajectories and proposed multi-step tool chains",
        outputs="Cumulative risk state and pre-execution safety decisions inside an autonomous research pipeline",
        notes="Safety framework woven through a Thinker/Experimenter/Writer/Reviewer scientific-agent pipeline. The paper evaluates risk tasks, but does not release a reusable named benchmark; this row represents the framework, not a B-class benchmark.",
    )

    by_id["asa-aira-dojo"].update(
        access="source-available",
        access_evidence={
            "software_license": "CC-BY-NC-4.0", "commercial_use": False,
            "source_url": "https://github.com/facebookresearch/aira-dojo",
        },
    )

    by_id["asa-cascade"].update(
        name="CASCADE", category="chemistry", autonomy="A4", access="paper-only", repo_links=[],
        domain="Self-evolving scientific skill acquisition for chemistry and materials research",
        inputs="Chemistry/materials task, public documentation and external tools",
        outputs="Accumulated executable skills, knowledge-graph memory and solved scientific tasks",
        notes="Self-evolving agentic framework evaluated on SciSkillBench. No separate public CASCADE implementation was confirmed; the open Figshare artifact belongs to the benchmark record.",
    )
    additions = [{
        "id": "asa-sciskillbench", "date_added": DATE, "date_modified": DATE, "verified": DATE,
        "name": "SciSkillBench", "category": "benchmark",
        "domain": "Materials-science and chemistry agent skill benchmark",
        "paper_links": links([("CASCADE paper", "https://arxiv.org/abs/2512.23880")]),
        "repo_links": links([("Figshare dataset", "https://figshare.com/articles/dataset/SkillSciBench_CASCADE_Benchmark_for_Evaluating_LLM_Agents_on_Scientific_Tasks/30924998")]),
        "access": "open-data", "inputs": "116 materials-science and chemistry research tasks",
        "outputs": "Task-success and acquired-skill evaluation results", "autonomy": "B",
        "notes": "Named benchmark used to evaluate CASCADE; split from the scientific-agent system so B is reserved for the harness.",
    }]

    by_id["asa-grace"].update(
        name="GRACE", category="physics", autonomy="A4",
        domain="Simulation-native particle and nuclear physics experiment design",
        notes="Simulation-native autonomous design agent. The paper reports an evaluation suite but no stable separately named public benchmark artifact, so no speculative B record is created.",
    )

    by_id["asa-automat-stem2mat-bench"].update(
        name="AutoMat", aliases=["AutoMat / STEM2Mat-Bench"], category="physics", autonomy="A3",
        domain="Agent-assisted microscopy-to-atomistic structure reconstruction",
        inputs="Scanning transmission electron microscopy images",
        outputs="Reconstructed crystal structures, relaxed structures and predicted physical properties",
        notes="Agent-assisted pipeline coordinating denoising, template retrieval, atomic reconstruction, relaxation and property prediction. The accompanying STEM2Mat-Bench is represented separately.",
    )
    additions.append({
        "id": "asa-stem2mat-bench", "date_added": DATE, "date_modified": DATE, "verified": DATE,
        "name": "STEM2Mat-Bench", "category": "benchmark",
        "domain": "Microscopy-to-atomistic reconstruction benchmark",
        "paper_links": links([("AutoMat paper", "https://arxiv.org/abs/2505.12650")]),
        "repo_links": links([("Official repository and dataset", "https://github.com/yyt-2378/AutoMat")]),
        "access": "open-data", "inputs": "STEM images paired with reference crystal structures",
        "outputs": "Lattice RMSD, formation-energy MAE and structure-matching success rate", "autonomy": "B",
        "notes": "Dedicated benchmark introduced with AutoMat; split from the A3 pipeline so system capability and evaluation evidence are not flattened into one row.",
    })

    deep = by_id["asa-deepresearch-bench"]
    deep.update(
        name="DeepResearch Bench", paper_links=[deep["paper_links"][0]], repo_links=[deep["repo_links"][0]],
        notes="Original long-form deep-research benchmark with PhD-level tasks and RACE/FACT evaluation. Split from DeepResearch Bench II because the projects have distinct papers, repositories and task/evaluation identities.",
    )
    deep.pop("aliases", None)
    additions.append({
        "id": "asa-deepresearch-bench-ii", "date_added": DATE, "date_modified": DATE, "verified": DATE,
        "name": "DeepResearch Bench II", "category": "benchmark",
        "domain": "Long-form evidence-grounded deep-research agents",
        "paper_links": links([("arXiv", "https://arxiv.org/abs/2601.08536")]),
        "repo_links": links([("GitHub", "https://github.com/imlrz/DeepResearch-Bench-II")]),
        "access": "open-source", "inputs": "Expert-derived deep-research tasks and binary rubrics",
        "outputs": "Rubric-level research-report quality and evidence-grounding scores", "autonomy": "B",
        "notes": "Second independently released DeepResearch Bench project; separated from the original to preserve paper, code and benchmark identity.",
    })

    for addition in additions:
        by_id.setdefault(addition["id"], addition)

    changed = {
        "asa-flowagent", "asa-scitrace", "asa-aira-dojo", "asa-bioplanner", "asa-gravity-bench",
        "asa-cascade", "asa-sciskillbench", "asa-grace", "asa-automat-stem2mat-bench",
        "asa-stem2mat-bench", "asa-deepresearch-bench", "asa-deepresearch-bench-ii", *remove_b,
    }
    ordered = list(by_id.values())
    for record in ordered:
        record["sources"] = sorted(
            {link["url"] for field in ("paper_links", "repo_links") for link in record.get(field, [])}
            | set(record.get("sources", []))
        )
        if record["id"] in changed:
            record["date_modified"] = DATE
            record["verified"] = DATE
    DATA.write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    tombstones = [
        {"id": "asa-futurehouse-edison-agents", "removed": DATE, "reason": "Redundant umbrella over retained specific systems", "replacement_id": None},
        {"id": "asa-kosmos-radiation-biology-evaluation", "removed": DATE, "reason": "Case-study audit, not a reusable agent or benchmark", "replacement_id": None},
        {"id": "asa-a-mobile-robotic-chemist", "removed": DATE, "reason": "Exact duplicate", "replacement_id": "asa-mobile-robotic-chemist-liverpool-cooper-2020"},
        {"id": "asa-biomedtools", "removed": DATE, "reason": "Tool registry/infrastructure, not an autonomous research agent", "replacement_id": None},
        {"id": "asa-atlas", "removed": DATE, "reason": "Bayesian-optimization component, not an agent or benchmark", "replacement_id": None},
        {"id": "asa-gryffin", "removed": DATE, "reason": "Bayesian-optimization algorithm, not an agent or benchmark", "replacement_id": None},
    ]
    TOMBSTONES.write_text(json.dumps(tombstones, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    apply()
