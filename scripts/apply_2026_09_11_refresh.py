#!/usr/bin/env python3
"""Apply evidence-reviewed September preview data; never publish.

Idempotent, preserves stable IDs, and leaves untouched evidence dates intact.
Decisions and source locators: evidence/refresh-2026-09-11/decisions.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-11'
BASELINE = '601e7e49fa4c6d28c1124c92015f15812c76272c'

def rec(key, name, category, domain, access, autonomy, inputs, outputs, notes, paper, repo, license_url=None, license_text=None, commercial=True, aliases=None):
    papers = [{'label': 'arXiv', 'url': 'https://arxiv.org/abs/' + paper}] if paper else []
    repos = [{'label': 'GitHub', 'url': repo}] if repo else []
    urls = [x['url'] for x in papers + repos]
    if license_url:
        urls.append(license_url)
    row = dict(id='asa-'+key, date_added=DATE, name=name, category=category, domain=domain,
               paper_links=papers, repo_links=repos, access=access, inputs=inputs,
               outputs=outputs, autonomy=autonomy, notes=notes, verified=DATE, sources=sorted(set(urls)))
    if aliases:
        row['aliases'] = aliases
    if license_text:
        row['access_evidence'] = dict(software_license=license_text, commercial_use=commercial, source_url=license_url or repo)
    return row

NEW_RECORDS = [
    rec('terminal-bench-science', 'Terminal-Bench-Science', 'benchmark', 'Expert-authored research workflows across life, physical, earth, mathematical and engineering sciences', 'open-source', 'B',
        'Scientific task instructions, containerized environments and required output artifacts', 'Task resolution scores against executable reference checks',
        'Stanford-led scientific branch of Terminal-Bench. The 0.1 release contains 70 expert-curated workflows executed through Harbor; the public repository provides tasks and reference solutions. Apache-2.0. Benchmark performance concerns computational workflows, not autonomous laboratory operation.', None,
        'https://github.com/harbor-framework/terminal-bench-science', 'https://github.com/harbor-framework/terminal-bench-science/blob/main/LICENSE'),
    rec('asi-bench', 'ASI-Bench', 'benchmark', 'Project-level computational research with progressively reduced methodological guidance', 'open-source', 'B',
        'Scientific objectives and task data under four levels of methodological guidance', 'Executable research artifacts, task scores and guidance-level comparisons',
        '60 research tasks across 11 domains; holds the scientific objective fixed while removing methods and adding distractors. The public runner produces artifacts, while official scoring uses the submission service. The repository LICENSE is Apache-2.0 despite a stale MIT footer on the project site. The title does not establish artificial superintelligence.',
        '2608.17271', 'https://github.com/apexin-ai/ASI-Bench', 'https://github.com/apexin-ai/ASI-Bench/blob/main/LICENSE'),
    rec('bixbench3', 'BixBench3', 'benchmark', 'Research-study-scale computational biology', 'open-data', 'B',
        'Raw study data, a biological objective, methodological guidance and structured artifact contracts', 'Analysis artifacts graded against published-study references plus process-quality diagnostics',
        'Edison benchmark with 20 study-scale tasks, distinct from the earlier question/capsule-based BixBench. Public runner and deterministic grader are provided; task manifests are on Hugging Face and raw inputs/reference artifacts use Google Cloud Storage. Running the documented harness requires a configured GCP project. Edison-authored code and materials are CC BY-SA 4.0; upstream scientific data retain their own terms.',
        '2608.25286', 'https://github.com/EdisonScientific/BixBench3', 'https://github.com/EdisonScientific/BixBench3/blob/main/LICENSE'),
    rec('earthverse', 'EarthVerse', 'benchmark', 'Earth-system and natural-hazard scientific investigations', 'source-available', 'B',
        'Heterogeneous event packages and 405 research tasks covering 199 events and 19 hazard families', 'Evidence-grounded answers, calculation traces, answer-unit accuracy and strict completion scores',
        'Agents inspect event evidence, choose tools, calculate and reconcile observations. Public tasks, reference answers, tools and evaluation code are released. Mixed licensing matters: original software is Apache-2.0, original task annotations are CC BY-NC 4.0, and third-party evidence retains provider-specific terms. Simulated/computational evaluation, not field actuation.',
        '2608.23525', 'https://github.com/CuiZHIQ/Earth-Verse', 'https://github.com/CuiZHIQ/Earth-Verse/blob/main/LICENSE.md', 'Apache-2.0 original software; CC-BY-NC-4.0 original task annotations; separate upstream evidence terms', False),
    rec('frontierchallenge', 'FrontierChallenge', 'benchmark', 'Complete scientific workflows across chemistry, materials and life science', 'open-source', 'B',
        'Fixed scientific input data and bundles of required end-to-end deliverables', 'Full-completion pass rates, partial scores and process diagnostics',
        'The paper describes 300 workflows but releases and evaluates 97; the record refers to that released subset. Evaluation code is within the Apache-2.0 FrontierAgent repository; task data are separately distributed on Hugging Face. Completion and partial progress are separate measures, and reported success is not proof of independent scientific discovery.',
        '2608.24979', 'https://github.com/ApodexAI/FrontierAgent/tree/main/benchmarks/frontierchallenge', 'https://github.com/ApodexAI/FrontierAgent/blob/main/LICENSE'),
    rec('truthinsightbench', 'TruthInsightBench', 'benchmark', 'Evidence quality in open-ended scientific data analysis', 'open-source', 'B',
        '40 blind research objectives with frozen data across ten scientific domains', 'Reproducible claims and artifacts scored by a 29-item evidence rubric',
        'Withholds source-study conclusions and analysis paths. The public release includes task data, four harness adapters and scoring code under Apache-2.0, with upstream attribution and licenses preserved separately. The fixed LLM judge measures rubric-defined evidentiary maturity; its scores do not certify the scientific truth of a discovery.',
        '2609.05079', 'https://github.com/TruthInsight-stack/TruthInsightBench', 'https://github.com/TruthInsight-stack/TruthInsightBench/blob/main/LICENSE'),
    rec('science-sandboxes', 'Science Sandboxes (MPRAbox / CodonBox)', 'benchmark', 'Agent experimentation against biological surrogate models and invented biological worlds', 'open-source', 'B',
        'Sealed sequence-design or sequence-to-fitness environments and tool budgets', 'Experiment trajectories and oracle-scored scientific exploration outcomes',
        'MPRAbox uses a pretrained empirical surrogate; CodonBox uses invented biological rules. Both provide computational experimental feedback and neither is a physical wet-lab loop. MIT code; Malinois model weights retain the separate boda2 license. The public repository includes the harnesses and results.',
        '2608.30165', 'https://github.com/asr2210/science-sandbox', 'https://github.com/asr2210/science-sandbox/blob/main/LICENSE', aliases=['MPRAbox', 'CodonBox']),
    rec('dr-claw', 'Dr. Claw', 'crossdomain', 'Human-supervised research workspace and executor orchestration', 'open-source', 'A3',
        'Research goals, project data, existing coding-agent executors and researcher decisions', 'Persistent task graphs, executed analyses, writing artifacts and recoverable audit trails',
        'A research workspace that coordinates existing executors through persistent state and explicit human decisions. It implements the research workflow layer rather than a new underlying autonomous model. AGPL-3.0 with GPL-3.0 upstream components; private medical datasets used in the study are not included in the release.',
        '2609.00365', 'https://github.com/OpenLAIR/dr-claw', 'https://github.com/OpenLAIR/dr-claw/blob/main/LICENSE'),
    rec('arcticswarm', 'ArcticSwarm', 'crossdomain', 'Long-horizon evidence retrieval and research synthesis', 'open-source', 'A3',
        'Research questions, web or corpus retrieval and configured model backends', 'Cross-examined findings, cited answers and inspectable research trajectories',
        'Snowflake research framework with independent exploration followed by peer challenge and verification before synthesis. The released harness supports live-web and corpus-based research under Apache-2.0. Demonstrated closure is information gathering and synthesis, not laboratory experiments.',
        '2609.01870', 'https://github.com/Snowflake-AI-Research/ArcticSwarm', 'https://github.com/Snowflake-AI-Research/ArcticSwarm/blob/main/LICENSE'),
    rec('evomap-autoresearch', 'AutoResearch (EvoMap)', 'crossdomain', 'Evidence-reviewed AI and machine-learning research', 'open-source', 'A4',
        'Research ideas or recent research signals, domain knowledge and compute resources', 'Experiment plans, implemented code, run logs, analyses and independent review reports',
        'Two-stage idea generation and execution workflow that persists research state and uses separate models to review plans and evidence. Pilot outcomes can trigger continuation, revision or termination. Apache-2.0. Disambiguated from other systems and informal workflows named autoresearch; the release describes computational experiments.',
        '2608.17906', 'https://github.com/EvoMap/AutoResearch', 'https://github.com/EvoMap/AutoResearch/blob/main/LICENSE', aliases=['EvoMap AutoResearch']),
    rec('station', 'The Station (Dualverse)', 'crossdomain', 'Open-world multi-agent computational and mathematical discovery', 'open-source', 'A4',
        'A shared scorable research task, an executable evaluator and model-provider configuration', 'Candidate constructions, evaluated solutions and persistent collaborative research records',
        'An open-world research environment with persistent agents, shared scientific records and executable evaluation. The v2 paper documents autonomous mathematical exploration; Apache-2.0 code and public trajectories are linked by the authors. Requires task-specific scoring and sufficiently fast iterations. Computational discovery does not imply a physical loop.',
        '2608.23691', 'https://github.com/dualverse-ai/station', 'https://github.com/dualverse-ai/station/blob/main/LICENSE', aliases=['Station v2']),
    rec('scienceflow', 'ScienceFlow', 'crossdomain', 'Long-horizon machine-learning and computational scientific research', 'open-source', 'A4',
        'Research task packages, model credentials, isolated workspaces and compute budgets', 'Recoverable experiment states, validated results, search branches and execution records',
        'Huawei Noah’s Ark Lab framework that couples persistent research workspaces, evidence gates and adaptive continuation or re-anchoring with compute scheduling. The author-owned noah-research monorepo releases the framework, tasks and documentation under MIT. The paper’s physical jobs are compute jobs, not laboratory actuation.',
        '2608.14354', 'https://github.com/huawei-noah/noah-research/tree/master/ScienceFlow', 'https://github.com/huawei-noah/noah-research/blob/master/ScienceFlow/LICENSE'),
    rec('brain-researcher', 'Brain Researcher', 'biology', 'Auditable neuroimaging analysis', 'open-source', 'A3',
        'Research questions, admissible neuroimaging datasets and approved analysis plans', 'Versioned analysis episodes, artifacts, provenance and condition-tagged review verdicts',
        'Connects evidence, analysis choices and tool execution through a workspace with a researcher commitment gate. Public MIT code includes the CLI, MCP contracts, service stack and examples. Private benchmark corpora, knowledge-graph contents and site-specific launchers are excluded; the paper’s broad archive wording must not be read as public access to every study asset. Interpretation remains with researchers.',
        '2608.19902', 'https://github.com/brain-researcher/brain-researcher-public', 'https://github.com/brain-researcher/brain-researcher-public/blob/main/LICENSE'),
    rec('orchestra-regulatory', 'Orchestra (regulatory discovery)', 'biology', 'Corroborated gene-regulatory candidate analysis', 'open-source', 'A3',
        'Gene/network comparison queries and configured RegNetAgents and CASCADE evidence services', 'Regulator candidates with independent-source support and source-level evidence flags',
        'MIT LangGraph workflow composing regulatory-topology and experimental-evidence MCP services. Tests whether agreement between evidence sources enriches known cancer-gene annotations; it does not establish causal regulation or prospective wet-lab discovery. This CASCADE dependency is Jose Bird’s bioinformatics service, distinct from the catalogued scientific skill-learning CASCADE.',
        '2609.05496', 'https://github.com/jab57/Orchestra', 'https://github.com/jab57/Orchestra/blob/main/LICENSE'),
    rec('arche', 'ARCHE', 'chemistry', 'Computational chemical-mechanism discovery', 'source-available', 'A4',
        'Mechanistic research questions, chemistry tools and configured reasoning models', 'Prioritized mechanisms, executed computational investigations and evidence-revised conclusions',
        'The paper combines general and chemistry-specialized models with a tool registry for iterative mechanistic investigation. Its author-linked Arche-Harness release is a later investigation_v2 implementation, not the paper’s earlier Planner/Execution/Reflection system. ARCHE-Chem weights, reward model, training corpus and training pipeline are absent; the public code and selected case data do not reproduce the complete paper configuration. A custom academic/non-commercial license applies. Closure is computational; reviewed sources were the primary abstract and repository documentation, not inaccessible HTML full text.',
        '2609.11147', 'https://github.com/JetAstra/Arche-Harness', 'https://github.com/JetAstra/Arche-Harness/blob/main/LICENSE', 'Academic and Non-Commercial Research License v1.0', False),
    rec('la-agente-optima', 'La Agente Óptima', 'chemistry', 'Agentic Bayesian-optimization campaigns on digital and physical laboratories', 'paper-only', 'A4-A5',
        'Scientific objectives, experiment search spaces, BO-MCP optimizers and connected laboratory platforms', 'Executable campaigns, measurements, repaired constraints and feedback-guided experiments',
        'Demonstrated on five digital tasks and two physical platforms. A real contact-angle loop executed measurements and revised a failing campaign, with operator approval for constraint changes and restarts; physical deck preparation requires a named human certification. Public research artifacts include data, conversations and plotting code, not a verified complete deployable Óptima system. The artifacts repository has no confirmed license, so public visibility is not an open-source claim.',
        '2609.04564', 'https://github.com/the-matter-lab/La-Agente-Optima-artifacts'),
    rec('modelica-agent-workflow-benchmark', 'Modelica Agent Workflow Benchmark', 'benchmark', 'Modelica model repair, generation and parameter tuning', 'source-available', 'B',
        'Faulty models, engineering requirements or tuning targets with OpenModelica validation', 'Executable and behavioral task checks under a shared agent evaluation protocol',
        'Companion benchmark to Pufibara. Public v0.2 provides Apache-2.0 code, protocol and schemas plus a small demo split under a separate Benchmark Data License: academic/non-commercial evaluation and local smoke testing are permitted, while model training, distillation, training-data expansion and dataset redistribution require written permission. Official evaluation uses hidden maintainer-run sets. Neither the full task set nor the full Pufibara stack is released; modeling is computational.',
        '2608.23653', 'https://github.com/wangzizhe/modelica-agent-workflow-benchmark', 'https://github.com/wangzizhe/modelica-agent-workflow-benchmark/blob/main/DATA_LICENSE.md', 'Apache-2.0 code; custom Benchmark Data License restricts task data to specified uses and prohibits training/distillation and dataset redistribution without permission', False),
    rec('pace-bench', 'PACE-Bench', 'benchmark', 'Adaptation of code-driven designs to changed simulated physics', 'open-source', 'B',
        '144 source-to-target environment pairs across six physics domains with a limited attempt budget', 'Adapted designs, sandbox feedback, validity checks and adaptation success scores',
        'Tests whether agents can repair a formerly successful design after a change in simulated physics while preserving goal and interface. Public MIT harness includes task environments and executable validation. Distinct from PACE-SIMS, which concerns a physical mass-spectrometry instrument.',
        '2608.14441', 'https://github.com/thunlp/PACE-Bench', 'https://github.com/thunlp/PACE-Bench/blob/main/LICENSE'),
    rec('andy-mathematics', 'Andy (mathematical research)', 'physics', 'Mathematical problem generation and proof workflows', 'open-source', 'A4',
        'Mathematical problems, proposed proofs and optional reference papers', 'Proof dependency graphs, separately reviewed proof steps, new problems and traceable reports',
        'MIT research system with a local workspace, persistent proof state and separate generation and checking models. Failed proof nodes trigger targeted repair. Automatic checking is language-model-based and is not equivalent to a formally verified proof-assistant certificate; the README requires researcher review before formal use.',
        '2608.15052', 'https://github.com/mowaiwaim/Andy', 'https://github.com/mowaiwaim/Andy/blob/main/LICENSE'),
    rec('benchmark-as-teacher', 'Benchmark-as-Teacher (BaT)', 'benchmark', 'Evaluation and recursive post-training harness for medical-imaging research agents', 'open-source', 'B',
        'Stage-level research rubrics, held-out-safe training states and an agent model', 'Targeted training curricula, updated agent checkpoints and repeated stage-level evaluations',
        'NVIDIA-associated MIT framework connecting stage diagnostics, data generation, GRPO training and evaluation gates for medical-imaging research agents. The public repository implements the training loop; it does not establish prospective clinical usefulness or a wet-lab loop. Distinct from the AutoMedBench evaluation resource it uses.',
        '2608.16211', 'https://github.com/AutoMedBench/Benchmark-as-Teacher', 'https://github.com/AutoMedBench/Benchmark-as-Teacher/blob/main/LICENSE'),
    rec('omniscientist-omni-modal', 'OmniScientist (omni-modal, NUS/Oxford)', 'crossdomain', 'Research from raw multimodal evidence to executable analyses and manuscripts', 'open-source', 'A4',
        'A research direction and local raw multimodal scientific data', 'Hypotheses, executed code, analyzed figures, traceable results and manuscript artifacts',
        'MIT system by Bobo Li, Hao Fei and collaborators with perception, ideation, experiment and writing stages. The September desktop release replaces the discontinued standalone terminal edition; a coding-agent skill remains available. Independent identity from Tsinghua FIB Lab’s 2025 OmniScientist: different authors, paper and repository. Demonstrations are computational.',
        '2608.13558', 'https://github.com/Omni-Scientist/OmniScientist', 'https://github.com/Omni-Scientist/OmniScientist/blob/main/LICENSE', aliases=['Omni-Scientist OmniScientist']),
]

# Partial evidence corrections keep their original verified dates.
PATCHES = {
    'asa-tooluniverse': {'notes': 'Scientific-agent infrastructure standardizing tool discovery and invocation across models, datasets, APIs and scientific packages. Supports sequential and parallel tool composition in configured self-directed workflows; this row describes the ecosystem rather than a standalone autonomous scientist.'},
    'asa-chemmcp': {'notes': 'Apache-2.0 MCP-compatible chemistry toolkit extending ChemToolAgent. The current release supports native multi-turn agent/tool reinforcement-learning loops as well as standalone tool integration; scientific autonomy depends on the configured agent and workflow.'},
    'asa-puda': {'notes': 'Hardware orchestration runtime, not a standalone scientist. External agents drive deterministic, provenance-recorded device commands using separate skills; the A3-A4 range describes configured workflows rather than autonomous reasoning intrinsic to PUDA. Researchers may inspect, approve or revise actions mid-campaign. No usable license was confirmed in the public repository.'},
    'asa-k-dense-scientific-agent-skills': {
        'paper_links': [{'label':'arXiv', 'url':'https://arxiv.org/abs/2609.00065'}],
        'notes': 'Scientific Agent Skills is a reusable procedural-skills library for existing coding agents, not a standalone scientist. The repository-level license is MIT, but individual skills may specify different terms, including document skills derived from Anthropic. Users must inspect each skill’s license. Retained under the explicit August selected-infrastructure precedent; no volatile skill count is asserted.'},
    'asa-scta': {'notes': 'Decomposes target discovery into agents aligned with single-cell pipeline decision points, each restricted to predefined tool sets; a Reviewer performs bounded repair on execution errors. Stability was assessed by repeated runs on public GEO datasets. The current README declares MIT but no standalone license text was confirmed, so the record remains source-available.',
                 'access_evidence': {'software_license':'MIT declared in README; no standalone license text confirmed on 2026-09-11', 'commercial_use':False, 'source_url':'https://github.com/silviachen46/SCTA'}},
    'asa-protopilot': {'notes': 'Self-evolving multi-agent workflow from intent through protocols, SOPs and SDK-compliant code to physical execution and feedback-guided revision. The current paper explicitly describes orchestration of physical instruments; the earlier note that it did not state this was too strong. Optional human checkpoints confirm materials, instrument compatibility and local constraints. Wet-lab demonstrations do not establish unattended operation of every step. No official software release was verified.', 'verified':DATE},
}

def main():
    path = ROOT / 'agents_final.json'
    rows = json.loads(path.read_text())
    rows = [r for r in rows if r['id'] != 'asa-periodic-labs']
    deprecated_path = ROOT/'deprecated_ids.json'
    retired = json.loads(deprecated_path.read_text())
    if not any(r['id']=='asa-periodic-labs' for r in retired):
        retired.append({'id':'asa-periodic-labs','removed':DATE,'reason':'Reversible HOLD: current official source describes a development goal but does not demonstrate the physical autonomous loop required for the prior A5 label. No discontinuation is inferred; restore the reserved ID if first-party system evidence supports an autonomy classification.','replacement_id':None})
    deprecated_path.write_text(json.dumps(retired,ensure_ascii=False,indent=2)+'\n')
    by_id = {r['id']:r for r in rows}
    tombstones = {r['id'] for r in json.loads((ROOT/'deprecated_ids.json').read_text())}
    for row in NEW_RECORDS:
        if row['id'] in tombstones:
            raise SystemExit('Refusing to resurrect retired ID: '+row['id'])
        if row['id'] not in by_id:
            rows.append(row); by_id[row['id']] = row
        elif by_id[row['id']] != row:
            raise SystemExit('New-record ID conflict: '+row['id'])
    for key, patch in PATCHES.items():
        row = by_id[key]
        row.update(patch)
        row['date_modified'] = DATE
        row['sources'] = sorted(set(row['sources'] + [l['url'] for l in row['paper_links']]))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
    meta_path = ROOT/'resource_metadata.json'
    meta=json.loads(meta_path.read_text())
    meta.update(resource_version='2.2.0', modified=DATE, baseline_commit=BASELINE,
                baseline_commit_url=meta['repository']+'/commit/'+BASELINE, release_ref=None,
                evidence_statement='Local 2.2.0 preview reviewed 2026-09-11. New records and explicitly re-reviewed claims have dated evidence; untouched verification dates are preserved. The September audit records source/access boundaries, holds, partial releases and coverage limits.')
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(rows)} records; {len(NEW_RECORDS)} additions; {len(PATCHES)} targeted corrections; 1 reversible hold/removal; local preview only')

if __name__ == '__main__':
    main()
