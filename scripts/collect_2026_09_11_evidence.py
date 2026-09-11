#!/usr/bin/env python3
"""Read-only primary-source collection for the dated local refresh.

Cached text is evidence for human/agent review, not automatic admission.
Two concurrent requests maximum; no credentials, scraping bypass or mutations.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import time
import urllib.request
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1] / '.maintenance-output/refresh-2026-09-11'
ROOT.mkdir(exist_ok=True)

def fetch(url):
    key = hashlib.sha256(url.encode()).hexdigest()[:20]
    path = ROOT / 'sources' / (key + '.json')
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        return json.loads(path.read_text())
    out = {'url': url, 'retrieved': '2026-09-11'}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ScientificCatalogEvidenceReview/1.0'})
        with urllib.request.urlopen(req, timeout=30) as f:
            payload = f.read(4000000)
            out.update(status=f.status, final_url=f.url, content_type=f.headers.get('Content-Type'))
        html = payload.decode('utf8', errors='replace')
        if 'html' in out['content_type']:
            soup = BeautifulSoup(html, 'html.parser')
            for t in soup(['script', 'style', 'nav']):
                t.decompose()
            out['links'] = sorted(set(a.get('href') for a in soup.select('a[href]')))
            out['text'] = soup.get_text(' ', strip=True)
        else:
            out['text'] = html
        out['payload_sha256'] = hashlib.sha256(payload).hexdigest()
        out['access_level'] = 'fulltext-html' if '/html/' in url else 'primary-page-or-repository-text'
        if '/abs/' in url:
            out['access_level'] = 'paper-metadata-and-abstract'
    except Exception as e:
        out.update(status=getattr(e, 'code', None), error=type(e).__name__, access_level='inaccessible')
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    time.sleep(.35)
    return out

if __name__ == '__main__':
    import sys
    urls = json.loads(Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        for out in pool.map(fetch, urls):
            print(out['url'], out.get('status'), len(out.get('text', '')), flush=True)
