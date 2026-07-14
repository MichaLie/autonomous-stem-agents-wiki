# Maintenance protocol

This is the canonical, agent-neutral operating guide for the Autonomous Science Agents index. `CLAUDE.md`, `AGENTS.md`, and `.claude/skills/` are adapters to this file; if they disagree, this file wins.

## Purpose and boundary

The resource catalogs systems that perform multi-step scientific work—literature, hypotheses, experiments or simulations, code/tool execution, analysis, reporting—or benchmarks/harnesses that evaluate such systems. It is not a general list of LLMs, optimization libraries, scientific software components, or one-off case-study audits.

Categories are `crossdomain`, `biology`, `chemistry`, `physics`, and `benchmark`. Access is one of `open-source`, `source-available`, `open-data`, `platform`, `lab-gated`, `paper-only`, or `list`. B is reserved for benchmarks/harnesses.

Autonomy describes observed closure: A1 assistant; A2 tool agent; A3 workflow agent; A4 in-silico autonomous scientist; A5 real physical/laboratory loop. Simulation/HPC closure is not A5. Human safety gates do not automatically preclude A5 when the system demonstrably controls a physical loop, but they must be disclosed.

## Sources of truth

- `agents_final.json`: canonical records; the only catalog data edited by hand or a reviewed migration.
- `schema.json`: JSON Schema 2020-12 contract.
- `resource_metadata.json`: resource identity, dates, version, provenance, creator/publisher/licence decisions.
- `build.py`: deterministic build and synchronization entry point.
- `validate_catalog.py`: preview/release validation.
- `evidence/`: dated discovery and URL evidence.
- Generated HTML/Markdown/JSON/JSON-LD under `docs/` and the repository root: never hand-edit.

Counts are derived from `agents_final.json`; never hard-code them in agent instructions.

## Identity, evidence, and dates

- Preserve existing stable `asa-*` IDs through renames; store former names in `aliases`.
- New records receive `date_added` and an evidence-backed `verified` date.
- A rebuild is not verification. Update `verified` only after checking the record's claims and current sources.
- Confirm that papers/DOIs resolve, match the system, and are not withdrawn.
- Repository/platform links must be official or explicitly author-endorsed. Never use a third-party reconstruction as evidence for the original system.
- `open-source` requires a confirmed software licence. Public but unlicensed code is not open-source.

## Update workflow

1. Read this file, `schema.json`, and the latest evidence note.
2. Build normalized current name/alias sets, including same-name/different-system collision checks.
3. Choose a bounded correction/addition or a full refresh.
4. A full refresh uses independent lanes for cross-domain/benchmarks, biology/medicine, and chemistry/materials/physics/engineering, followed by shuffled adversarial review.
5. Verify primary sources, artifact ownership, access/licence, and physical versus computational closure.
6. Prefer HOLD or removal over padding the index with obscure, unlicensed, unreleased, duplicate, or out-of-scope entries.
7. Apply a large refresh through a dated idempotent migration and document additions, corrections, removals, holds, and disagreements in `evidence/`.
8. Build, validate, audit all URLs, inspect the rendered preview, and only then consider release.

## Local verification

```bash
python3 build.py
python3 validate_catalog.py
python3 scripts/audit_links.py --workers 24 --timeout 20
git diff --check
```

The public, agent-neutral harness in [`maintenance/`](maintenance/README.md) runs these gates, full JSON Schema 2020-12 format validation, normalized identity/date checks, report generation, and isolated synthetic fault injection. The checked-in GitHub workflow runs quality gates on changes and a live-link audit on a schedule; it has read-only repository permissions and contains no deployment job.

`build.py` proves byte-stable generation. Preview mode may report unresolved governance warnings. Release mode is stricter:

Rendered-table regression check: above 900 px, scroll the catalog and verify that the table-header top is exactly aligned with the bottom of the sticky controls. At 900 px and below, controls and table headers must both be static, the table wrapper may scroll horizontally, and the document itself must not overflow. Test at least one wide desktop, 1024 px, 900 px, and 390 px viewport after changing filters, table CSS, fonts, or header content.

The public design is generated from `build_html.py`. Source Sans 3 is self-hosted in `assets/fonts/` under the SIL Open Font License and copied into `docs/assets/fonts/` by `build.py`; do not add a runtime font service or edit generated HTML. Preserve the shared crisp layout and this index's violet identity accent while keeping autonomy/access semantics, focus states, sticky-table behavior, and mobile geometry accessible.

```bash
python3 validate_catalog.py --release
```

Do not weaken release validation to hide missing record evidence, catalogue licence, formal publisher identity, versioning, or distribution synchronization.

## FAIR and fork checklist

Forkers must replace landing-page/repository URLs and real creator, publisher, licence, version, and provenance in `resource_metadata.json`; rebuild; and validate JSON, schema, embedded JSON-LD, standalone JSON-LD, checksums, sitemap, and synchronized distributions. Do not copy institutional identity or imply endorsement without authority.

Machine-readable metadata and stable IDs improve FAIRness but do not prove that an external system is runnable, safe, licensed, or scientifically valid. Record-level evidence and honest access/autonomy labels remain mandatory.

For this release line, catalog data/metadata/original documentation are CC BY 4.0 and maintenance/build code is MIT. External resources, logos, and trademarks retain their own terms. Michaela Liegertová is the individual publisher; IMG CAS is affiliation only, and ELIXIR-CZ is dedication/community context only.

Provenance separates `baseline_commit`/`baseline_commit_url` (the revision from which the refresh was derived) from `release_ref` (the immutable release URL). Keep `release_ref: null` during ordinary preview work. During an explicitly authorized final packaging step, set it to the planned release URL matching `repository/releases/tag/v<resource_version>`; after publication and before announcement, verify that the exact URL resolves. Do not try to embed the hash of the commit that contains itself.

## Publication boundary

Local editing, testing, and commits are preparation. Push, merge, Pages deployment, DOI minting, release creation, and public FAIR badges require explicit human approval after release validation and preview review. No agent adapter or skill authorizes publication by itself.
