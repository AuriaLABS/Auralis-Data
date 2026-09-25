#!/usr/bin/env python3
"""Run clean-es over JSONL records that have a `text` field."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from clean_es import RECIPE, apply_exact_dedup, clean_document


def load_jsonl(path: Path) -> list[tuple[str, str]]:
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rec = json.loads(line)
        out.append((str(rec.get("id") or f"{path}#{i}"), rec.get("text") or ""))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=f"{RECIPE} jsonl")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--profile", choices=("web", "books"), default="books")
    ap.add_argument("--jsonl-out", type=Path)
    args = ap.parse_args()

    raw_recs = []
    for path in args.paths:
        files = sorted(path.rglob("*.jsonl")) if path.is_dir() else [path]
        for f in files:
            for rid, text in load_jsonl(f):
                rec = clean_document(text, args.profile)
                rec["path"] = rid
                raw_recs.append(rec)

    recs = apply_exact_dedup(raw_recs)
    hist, kept = Counter(), 0
    out_f = args.jsonl_out.open("w", encoding="utf-8") if args.jsonl_out else None
    try:
        for rec in recs:
            hist[rec["reason"]] += 1
            kept += int(rec["keep"])
            print(f"{rec['reason']:24} {rec.get('split', '-'):12} {rec['path']}")
            if out_f and rec["keep"]:
                out_f.write(json.dumps({
                    "id": rec["path"], "text": rec["text"], "recipe": RECIPE,
                    "doc_hash": rec.get("doc_hash"), "split": rec.get("split"),
                    "pii": rec.get("pii") or [],
                }, ensure_ascii=False) + "\n")
    finally:
        if out_f:
            out_f.close()
    total = sum(hist.values())
    print("---")
    print(f"recipe={RECIPE} profile={args.profile} docs={total} kept={kept}")
    for reason, n in hist.most_common():
        print(f"  {reason:24} {n:4}  {100.0 * n / total if total else 0:5.1f}%")
    return 0 if kept else 1


if __name__ == "__main__":
    raise SystemExit(main())
