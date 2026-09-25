#!/usr/bin/env python3
"""Assert clean-es-v0.1.0 reason codes on samples/."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_es import clean_document

SAMPLES = ROOT / "samples"
EXPECT = {
    "keep_prose.txt": "ok",
    "reject_banners.txt": "boilerplate",
    "reject_portuguese.txt": "not_spanish",
    "reject_ascii.txt": "no_spanish_orthography",
    "reject_short.txt": "too_short",
}


def main() -> int:
    failed = 0
    for name, want in EXPECT.items():
        got = clean_document((SAMPLES / name).read_text(encoding="utf-8"), "web")["reason"]
        mark = "ok" if got == want else "FAIL"
        print(f"{mark:4} {name:28} want={want:24} got={got}")
        failed += got != want
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
