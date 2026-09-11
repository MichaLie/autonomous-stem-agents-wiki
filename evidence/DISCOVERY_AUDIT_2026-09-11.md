# Autonomous Science Agents discovery audit — 2026-09-11

> Historical review-stage snapshot. Publication was subsequently authorized; see [release packaging](RELEASE_2026-09-11.md).

## Local preview and result

This is an unpublished **2.2.0 preview**, derived from commit `601e7e49fa4c6d28c1124c92015f15812c76272c`. `release_ref` remains null. No push, release, tag or remote write was performed.

- Baseline: 438 records.
- Additions: 21.
- Targeted corrections to existing records: 6.
- Reversible hold/removal: 1, Periodic Labs.
- Current catalog: **458 records** — 77 cross-domain, 99 biology, 85 chemistry, 91 physics and 106 benchmarks.

New records have `date_added` and `verified` equal to the actual review date. Existing verification dates were preserved except ProtoPilot, whose current paper claims were re-appraised and rewritten. The other five corrections carry `date_modified` without implying a complete new verification. HTTP reachability alone never changes a record's evidence date.

## Discovery and evidence boundary

The main discovery window is 2026-08-13 through 2026-09-11, with targeted older gaps and the August watchlist revisited. Three explicit topical lanes covered cross-domain systems/benchmarks, biology/medicine, and chemistry/materials/physics/engineering. This catalog lane was assembled by one maintainer; root review supplied an additional, separate appraisal of selected disputed and changed records. It is not described as three independently staffed literature reviews.

The arXiv API query retrieved **671** metadata matches in two pages. It combined `agent` with scientific/research/domain terms and submission dates. **66** papers were deliberately shortlisted for primary-source inspection. An official Terminal-Bench-Science release and the August-12 MACROS overlap lead brought the candidate set to **68**: 21 additions, 43 held leads, three scope rejections and one match to an existing record (the K-Dense paper). A separate Pufibara component decision accompanies the accepted Modelica benchmark paper. The unselected metadata inventory is not a list of individually verified exclusions.

The exact API queries, pagination URLs and inventory are in [`refresh-2026-09-11/discovery-index.json`](refresh-2026-09-11/discovery-index.json); web queries and coverage limits are in [`search-log.json`](refresh-2026-09-11/search-log.json). Primary pages, repositories, license texts and relevant paper sections were inspected. [`decisions.json`](refresh-2026-09-11/decisions.json) links each verdict and changed claim to the compact [`source_registry.json`](refresh-2026-09-11/source_registry.json), which records URLs, retrieval dates, HTTP/access status, hashes, locators and brief excerpts. Full fetched pages and feed snapshots remain in the ignored `.maintenance-output/refresh-2026-09-11/` cache, not in public evidence.

Paper metadata was checked for identity, version and withdrawal notices. No withdrawal notice appeared on admitted papers' inspected arXiv pages. This does not imply peer review or independent replication. Access levels distinguish metadata/abstracts, fetched HTML full text, repository documentation, and inaccessible pages. ARCHE's scientific description relies on the primary abstract plus its released repository documentation; its HTML full text was unavailable. No search snippet was promoted to full-text evidence.

This is a broad discovery refresh with targeted verification, **not a complete re-verification of all 438 baseline records or an exhaustive systematic review**. bioRxiv/medRxiv and company announcements were searched, but were not exhaustively enumerated. Several apparent new systems remain held because a licensed, author-endorsed reusable artifact was not verified. That means unresolved access, not proof that no artifact exists anywhere.

## Accepted additions

| Area | Added records |
|---|---|
| Cross-domain | Dr. Claw; ArcticSwarm; AutoResearch (EvoMap); The Station (Dualverse); ScienceFlow; OmniScientist (omni-modal, NUS/Oxford) |
| Biology | Brain Researcher; Orchestra (regulatory discovery) |
| Chemistry | ARCHE; La Agente Óptima |
| Physics/mathematics | Andy (mathematical research) |
| Benchmarks/harnesses | Terminal-Bench-Science; ASI-Bench; BixBench3; EarthVerse; FrontierChallenge; TruthInsightBench; Science Sandboxes (MPRAbox / CodonBox); Modelica Agent Workflow Benchmark; PACE-Bench; Benchmark-as-Teacher (BaT) |

### Release and identity findings that changed admission

- **ScienceFlow:** the paper did not directly expose its own repository in the inspected HTML. A targeted first-party search and the Huawei Noah's Ark monorepo verified the actual ScienceFlow subdirectory, MIT license, framework, task packages and README. It is open-source rather than paper-only. Its “physical jobs” are compute jobs, not a laboratory loop.
- **OmniScientist:** the NUS/Oxford system has different authors, paper and repository from the existing Tsinghua FIB Lab OmniScientist. The two identities are retained separately with a disambiguated new display name. Its September desktop release discontinued the standalone terminal edition; the catalog does not advertise that obsolete delivery mode.
- **BixBench3:** distinct study-scale tasks rather than the original BixBench's question/capsule benchmark. The runner and grader are public, while task manifests and scientific data use separate Hugging Face/GCS distribution. Author-created code and materials are **CC BY-SA 4.0**, not an assumed MIT or Apache software release. The documented harness requires a configured GCP project.
- **ASI-Bench:** the current license file is **Apache-2.0**, despite a stale MIT footer on the official site. Public artifact production and official submission-based scoring are distinguished.
- **EarthVerse:** original code is Apache-2.0, original annotations are **CC BY-NC 4.0**, and upstream evidence has separate terms. It is therefore represented as source-available with the noncommercial dataset boundary explicit.
- **ARCHE:** public code carries a custom **Academic and Non-Commercial Research License**, so it is source-available. Root review additionally identified that current `investigation_v2` differs from the paper’s Planner/Execution/Reflection implementation: ARCHE-Chem weights, reward model, corpus and training pipeline are absent. The row now explicitly limits release and reproduction claims.
- **FrontierChallenge:** the paper describes 300 workflows but releases/evaluates 97; the row names the released subset.
- **Modelica Agent Workflow Benchmark:** the public release consists of protocol, schemas, scoring notes and a small demo split. Root review found the separate `DATA_LICENSE.md`: while code is Apache-2.0, task data permit specified uses including academic/noncommercial evaluation and prohibit training, distillation, training-dataset expansion and large-scale/dataset redistribution without written permission. Access is corrected to **source-available** with explicit evidence. Official evaluation uses hidden maintainer-run sets. The associated **Pufibara agent remains held as a separate row**: its README explicitly says the broader system is private despite releasing selected Apache-licensed tools.
- **La Agente Óptima:** real physical campaigns are documented alongside digital tasks, including operator approvals, human deck certification and recovery decisions. The public artifact repository contains experimental evidence and plotting code, not a verified complete deployable system; the row remains paper-only. A4-A5 does not mean unattended execution of every laboratory step.
- **Brain Researcher:** the current public release excludes private benchmark corpora, knowledge-graph contents and site-specific launchers. Its broader paper archive wording is not evidence that these are available to a public user.
- **BaT:** root review corrected the proposed agent classification. The inspected release is an evaluation/post-training harness with stage diagnostics, data generation, GRPO and checkpoint evaluation, so it is **category benchmark, autonomy B**.
- **Andy:** separate model-based proof checking does not establish formal proof-assistant certification. The row preserves this limitation.

No advertised scientific benchmark score was reproduced during this catalog review. “Open-source” identifies a verified software license and described release, not a successful local installation of every external project.

## Existing corrections and disagreements

**ToolUniverse, ChemMCP, PUDA and K-Dense scientific-agent-skills** were initially proposed for exclusion by the catalog lane because they are infrastructure or skills. Root independently inspected their current first-party READMEs and the August audit. It retained August's explicit selected-infrastructure precedent: the maintenance boundary says this is not a *general list* of components, and does not unambiguously revoke those deliberate inclusions. This disagreement and adjudication are recorded in [`component-scope-review.json`](refresh-2026-09-11/component-scope-review.json). No inclusion policy was changed.

Their notes now make the boundary explicit. ToolUniverse supports sequential/parallel tool composition in configured workflows. ChemMCP advertises native multi-turn agent/tool RL loops. PUDA's displayed autonomy range refers to configured external-agent workflows, not autonomous reasoning intrinsic to the hardware runtime. K-Dense receives its September paper, omits an inconsistent volatile skill count, and clarifies that repository-level MIT does not override individual skill licenses, including Anthropic document skills. New skill-pack candidates remain held until their scope is resolved; this adjudication is not blanket admission of every component.

**SCTA:** its current README declares MIT, but no standalone license text was confirmed. Source-available is retained and its evidence describes the declaration rather than simply claiming no license statement exists.

**ProtoPilot:** the current paper explicitly states that the system orchestrates physical instrument execution. The previous assertion that it did not state this was too strong. Notes now distinguish that positive evidence from optional human checkpoints and the lack of demonstrated unattended operation of every step. The paper remains v2 from July; this is a correction of the earlier reading, not an asserted September paper revision.

The other seven source-available access checks retain their labels. In particular, LQCDMaster's linked LICENSE still returned 404 and NNStar's license remains an unresolved placeholder despite including template MIT text. Vibe Calibration's paper still supports physical calibration after human skill distillation. PACE-SIMS metadata was reachable but HTML was not; no new autonomy inference was made. Claude Science and Lila's official pages were checked selectively, without changing their verification dates.

## Reversible hold: Periodic Labs

The sole cited current official page says it is building an AI scientist and autonomous laboratories. It does not demonstrate the observed physical closed loop required for the existing A5 label. Root independently confirmed this evidence problem. Assigning an invented lower autonomy level would not repair it.

`asa-periodic-labs` is therefore removed from the displayed table and reserved in `deprecated_ids.json`, with the complete prior row preserved in [`periodic-prior-row.json`](refresh-2026-09-11/periodic-prior-row.json). **No shutdown or discontinuation is inferred.** Restore the same ID when first-party technical or demonstration evidence supports a concrete system and an autonomy classification.

## Held and rejected candidates

All 43 new held leads are individually listed in `decisions.json`, including ADMET-EvO (author-linked repository returned 404), SciLENS, AgentFold, AutoKD, AutoSR, SAEScientist-Bench and Eureka (public repositories without confirmed usable licenses), and several paper-only leads requiring better artifact evidence. MACROS, MAESTRO, zenDot, ALKEMIE Agent and some physical-instrument systems had inaccessible HTML and remain held for fuller appraisal. These are unresolved leads, not claims of nonexistence or failed science.

Three candidates were rejected on scope: **BuildOcc** simulates occupants rather than scientists; the **atomic-layer-deposition evaluation overview** does not establish a separate reusable agent/harness; **Intern-S2-Preview** is a base-model family rather than a separately established scientific system in this review.

The four August holds were revisited: IOBRpy remains a pipeline toolkit with external-agent integrations, TCellAlign remains unresolved on scope/release, LabRobFail remains a partial unlicensed simulator release, and Sakana Marlin remains business/strategy research. FARS's official site still failed at the network level, so its existing tombstone remains. Plato-Bio, Agentic Re-Casting and the Argonne atomistic framework remain follow-up leads; the RSC source returned 403. No new Edison Finch product claim was substantiated. The August OpenDDE/IgGM2 leads belong to the foundation-model catalog and were not independently re-adjudicated here.

## Local checks and remaining release gate

- Dated migration is idempotent: canonical JSON, metadata and tombstones were byte-identical on a second run.
- `maintenance/run_maintenance.py --mode quick`: **PASS**, including deterministic build, preview validation, full JSON Schema/format and identity/date invariants, canonical immutability, and diff checks.
- Full URL audit: **819 unique URLs across 1,644 current occurrences; 789 reachable, 30 restricted; zero missing, network-error or server-error outcomes.** Restricted publisher hosts are listed in [`link-audit-summary.json`](refresh-2026-09-11/link-audit-summary.json); restrictions are not described as broken links.
- The live audit began before the Periodic hold. Its three retired-row occurrences were removed from the public current-catalog TSV; the original audit is preserved locally. Every final canonical URL is covered. A final root-review citation change to Modelica’s separate data license was audited individually and the exact canonical occurrence inventory regenerated; the distinct-URL count remained 819.
- `validate_catalog.py --release`: **expected failure solely for null release_ref**. Governance was not weakened to make an unpublished preview pass as a release.
- Version-badge tooltip now says “Catalog version and metadata modification date,” avoiding a false claim that this local preview is published.
- Root owns the final rendered desktop/mobile preview and shuffled cross-catalog review. Those checks must be reported separately from this catalog lane's completed data/build/link checks.
- After ASA canonical changes stabilized, this editor independently checked six specified Foundation records against primary sources. Two wording refinements were applied by the Foundation editor; no admission-blocking issue remained in that bounded sample. Scope, sources, findings and access limitations are recorded in [`foundation-cross-review.md`](refresh-2026-09-11/foundation-cross-review.md). This is a separate cross-catalog check, not an assertion of exhaustive Foundation review.

Publication remains the final, separately agreed step.
