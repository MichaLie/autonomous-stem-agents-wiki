---
name: update-stem-agents-wiki
description: Safely update, verify, classify, build, and locally validate the Autonomous Science Agents index under the repository maintenance and FAIR release gates.
---

# Update the Autonomous Science Agents index

1. Read `MAINTENANCE.md` completely. It is canonical and this skill cannot override it.
2. Read `schema.json`, load `agents_final.json`, normalize every name/alias, and inspect the latest `evidence/` note.
3. For a full refresh, use independent cross-domain/benchmark, biology/medicine, and chemistry/materials/physics/engineering discovery lanes, followed by shuffled adversarial review.
4. Verify that every paper/DOI is real, matched, and not withdrawn; every repository/platform is official; and access/licence and physical-versus-simulated closure are supported. B is only for a benchmark/harness. Public unlicensed code is not open-source.
5. Preserve stable IDs and evidence dates. Prefer HOLD/removal over obscure, duplicate, unlicensed, unreleased, or out-of-scope records. Use a dated migration and evidence note for a large refresh.
6. Run:

```bash
python3 build.py
python3 validate_catalog.py
python3 scripts/audit_links.py --workers 24 --timeout 20
git diff --check
```

7. Inspect the rendered site and machine-readable distributions. `python3 validate_catalog.py --release` is the final eligibility gate.

Never push, deploy Pages, create a release/DOI, or publish a FAIR badge unless the human owner explicitly authorizes it after reviewing the complete preview and a passing release gate.
