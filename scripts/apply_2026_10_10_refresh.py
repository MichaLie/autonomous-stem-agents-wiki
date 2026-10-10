#!/usr/bin/env python3
"""Apply the evidence-reviewed October 2026 preview data; never publish.

Idempotent, preserves stable IDs, and leaves untouched verification dates intact.
Complete records and every decision (with source locators and adversarial-review
verdicts) are in evidence/refresh-2026-10-10/decisions.json.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / 'evidence/refresh-2026-10-10/decisions.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    payload = read(PAYLOAD)
    date = payload['review_date']
    rows = read(ROOT / 'agents_final.json')
    tombstones = [t for t in read(ROOT / 'deprecated_ids.json') if t['id'] not in set(payload['restored_ids'])]
    retired = {t['id'] for t in tombstones}
    updates = {r['id']: r for r in payload['records']}
    if len(updates) != len(payload['records']):
        raise SystemExit('Duplicate IDs in the reviewed payload')
    if retired & set(updates):
        raise SystemExit('Refusing to resurrect retired IDs: ' + ', '.join(sorted(retired & set(updates))))
    existing = {r['id'] for r in rows}
    rows = [updates.get(r['id'], r) for r in rows] + [r for r in payload['records'] if r['id'] not in existing]
    write(ROOT / 'agents_final.json', rows)
    write(ROOT / 'deprecated_ids.json', tombstones)

    # Counts come from the payload, not the current file, so a re-run writes identical metadata.
    restored = set(payload['restored_ids'])
    new = sum(1 for r in payload['records'] if r['date_added'] == date or r['id'] in restored)
    corrected = len(payload['records']) - new
    verified_now = sum(1 for r in rows if r['verified'] == date)
    meta = read(ROOT / 'resource_metadata.json')
    meta.update(resource_version='2.3.0', modified=date, evidence_review_date=date,
                baseline_commit=payload['baseline_commit'],
                baseline_commit_url=meta['repository'] + '/commit/' + payload['baseline_commit'], release_ref=None,
                evidence_statement=(
                    f'Local 2.3.0 preview reviewed {date}. {len(rows)} records; {verified_now} carry this review date. '
                    f'{new} records were added or restored after an independent adversarial check. {corrected} existing records '
                    'received targeted corrections, mostly access relabels after a licence check, and keep their earlier '
                    'verification dates. The October audit records sources, review verdicts, holds and coverage limits.'))
    write(ROOT / 'resource_metadata.json', meta)
    cats = Counter(r['category'] for r in rows)
    print(f"Applied {date}: {len(rows)} records ({new} added/restored, {corrected} corrected, "
          f"{len(payload['restored_ids'])} tombstones lifted); categories {dict(cats)}; local preview only")


if __name__ == '__main__':
    main()
