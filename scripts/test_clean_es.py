#!/usr/bin/env python3
"""Assert clean-es-v0.3.0 reason codes, PII redaction, and splits."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_es import apply_exact_dedup, clean_document
from redact import redact_pii

SAMPLES = ROOT / "samples"
SINGLE = {
    "keep_prose.txt": "ok",
    "keep_pii.txt": "ok",
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

    pii = clean_document((SAMPLES / "keep_pii.txt").read_text(encoding="utf-8"), "web")
    for token in ("<EMAIL>", "<IBAN>", "<PHONE>", "<ID>"):
        ok = token in pii["text"]
        print(f"{'ok' if ok else 'FAIL':4} pii has {token}")
        failed += not ok
    raw_left = any(s in pii["text"] for s in ("example.com", "ES9121", "+34 612", "00000000T"))
    print(f"{'FAIL' if raw_left else 'ok':4} raw PII stripped")
    failed += raw_left
    if set(pii["pii"]) != {"email", "iban", "phone", "id"}:
        print("FAIL pii tags", pii["pii"])
        failed += 1
    else:
        print("ok   pii tags")

    redacted, _ = redact_pii("codigo 12345678A y 00000000T")
    if "12345678A" not in redacted or "<ID>" not in redacted:
        print("FAIL invalid DNI handling", redacted)
        failed += 1
    else:
        print("ok   invalid DNI kept")

    if pii["split"] not in {"train", "validation", "test"}:
        print("FAIL split", pii["split"])
        failed += 1
    else:
        print("ok   split", pii["split"])

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
