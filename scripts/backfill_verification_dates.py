#!/usr/bin/env python3
"""Backfill explicit verification dates from documented catalog audits.

The 2026-06-16 release is supported by the retained existing-entry audit and
adversarial new-candidate verification workflow. The 2026-06-20 release added
23 verified records under the repository update protocol. Records reviewed
again later keep their newer explicit date.
"""
from __future__ import annotations

import json
from pathlib import Path


path = Path("agents_final.json")
records = json.loads(path.read_text(encoding="utf-8"))
allowed = {"2026-06-16", "2026-06-20"}
changed = 0
for record in records:
    if record.get("verified"):
        continue
    if record.get("date_added") not in allowed:
        raise SystemExit(f"no documented audit date for {record['id']}")
    record["verified"] = record["date_added"]
    changed += 1

path.write_text(json.dumps(records, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"backfilled {changed} historical verification dates")
