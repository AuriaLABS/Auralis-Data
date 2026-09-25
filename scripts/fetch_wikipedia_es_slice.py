#!/usr/bin/env python3
"""Fetch a truncated Spanish Wikipedia slice for Genesis smoke tests.

Does not download a dump. Pins titles, truncates each extract, writes JSONL.
Re-run and bump the mix version if titles or MAX_CHARS change.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

TITLES = [
    "Idioma español",
    "Miguel de Cervantes",
    "Biblioteca Nacional de España",
    "Real Academia Española",
    "Literatura española",
]
MAX_CHARS = 2500
UA = "Auralis-Data/0.1 (slice; https://github.com/AuriaLABS/Auralis-Data)"
OUT = Path(__file__).resolve().parents[1] / "samples" / "wikipedia_es" / "slice.jsonl"
SUM = Path(__file__).resolve().parents[1] / "checksums" / "wikipedia-es-slice-v0.1.0.sha256"


def fetch(title: str) -> dict:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "extracts|info",
            "explaintext": "1",
            "redirects": "1",
            "inprop": "url",
            "titles": title,
            "format": "json",
        }
    )
    req = urllib.request.Request("https://es.wikipedia.org/w/api.php?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    page = next(iter(data["query"]["pages"].values()))
    text = (page.get("extract") or "")[:MAX_CHARS].rsplit(" ", 1)[0].strip()
    return {
        "id": f"wikipedia-es-{page.get('pageid')}",
        "source_id": "wikipedia-es",
        "title": page.get("title"),
        "url": page.get("fullurl"),
        "license": "CC-BY-SA-4.0",
        "text": text,
    }


def main() -> int:
    rows = [fetch(t) for t in TITLES]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    blob = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    OUT.write_text(blob, encoding="utf-8")
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    SUM.write_text(f"{digest}  samples/wikipedia_es/slice.jsonl\n", encoding="utf-8")
    print(f"wrote {OUT} rows={len(rows)} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
