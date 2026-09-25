#!/usr/bin/env python3
"""Assert clean-es-v0.2.0 reason codes on samples/."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_es import apply_exact_dedup, clean_document

SAMPLES = ROOT / "samples"
SINGLE = {
    "keep_prose.txt": "ok",
    "reject_banners.txt": "boilerplate",
    "reject_portuguese.txt": "not_spanish",
    "reject_ascii.txt": "no_spanish_orthography",
    "reject_short.txt": "too_short",
    "reject_repeat.txt": "dup_line",
}


def main() -> int:
    failed = 0
    for name, want in SINGLE.items():
        got = clean_document((SAMPLES / name).read_text(encoding="utf-8"), "web")["reason"]
        mark = "ok" if got == want else "FAIL"
        print(f"{mark:4} {name:28} want={want:24} got={got}")
        failed += got != want

    batch_names = ["keep_prose.txt", "z_dup_keep_prose.txt", "z_shared_paragraph.txt"]
    recs = []
    for name in batch_names:
        rec = clean_document((SAMPLES / name).read_text(encoding="utf-8"), "web")
        rec["path"] = name
        recs.append(rec)
    out = {r["path"]: r["reason"] for r in apply_exact_dedup(recs)}
    batch_want = {
        "keep_prose.txt": "ok",
        "z_dup_keep_prose.txt": "dup_doc",
        "z_shared_paragraph.txt": "dup_paragraph",
    }
    print("--- batch ---")
    for name, want in batch_want.items():
        got = out[name]
        mark = "ok" if got == want else "FAIL"
        print(f"{mark:4} {name:28} want={want:24} got={got}")
        failed += got != want
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
