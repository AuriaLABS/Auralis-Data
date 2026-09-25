#!/usr/bin/env python3
"""clean-es-v0.1.0 — stages 2–5 of docs/cleaning.md (stdlib only).

Normalize, heuristic language gate, fast-reject, Spanish boilerplate.
Optional fastText/GlotLID can wrap this later; the reason codes stay stable.

Usage:
  python3 scripts/clean_es.py samples/
  python3 scripts/clean_es.py --profile books path/to/file.txt
  python3 scripts/clean_es.py --jsonl-out /tmp/kept.jsonl samples/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RECIPE = "clean-es-v0.1.0"

ES_STOP = frozenset(
    "de la que el en y a los se del las un por con no una su para es al lo como más pero sus le ha me si ya o este entre cuando muy sin sobre también hasta hay desde está mi porque esta son nos así".split()
)
PT_MARKERS = frozenset(
    "não você vocês também são está estão para pelo pela pelos pelas numa neste nesta isso issozinho aí ainda hoje onde".split()
)
CA_MARKERS = frozenset(
    "amb dels perquè els les una uns unes aquest aquesta aquests aquestes també després als".split()
)
GL_MARKERS = frozenset(
    "unha polos polas dunha neste nesta galego tamén despois".split()
)

BANNER_RES = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"aceptar cookies",
        r"acepto las cookies",
        r"pol[ií]tica de cookies",
        r"configurar cookies",
        r"dos clic[ks]s?",
        r"m[aá]s privacidad",
        r"gestionar consentimiento",
        r"necesario para el funcionamiento",
        r"suscr[ií]bete",
        r"newsletter",
        r"iniciar sesi[oó]n",
        r"crear cuenta",
        r"a[nñ]adir al carrito",
        r"finalizar compra",
        r"gastos de env[ií]o",
        r"cesta de la compra",
        r"proceder al pago",
        r"dejar un comentario",
        r"escribe un comentario",
        r"valoraci[oó]n",
        r"saltar al contenido",
        r"aviso legal",
    )
]
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
WORD_RE = re.compile(r"\S+")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = CTRL_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def strip_banners(text: str) -> tuple[str, int]:
    kept = []
    dropped = 0
    for line in text.split("\n"):
        if any(rx.search(line) for rx in BANNER_RES):
            dropped += 1
            continue
        kept.append(line)
    return "\n".join(kept).strip(), dropped


def heuristic_lang(text: str) -> tuple[str, dict]:
    tokens = [w.strip("..,;:¡!¿?\"'«»()[]").lower() for w in words(text)]
    if not tokens:
        return "und", {"es": 0.0, "pt": 0.0, "ca": 0.0, "gl": 0.0}
    n = len(tokens)
    scores = {
        "es": sum(t in ES_STOP for t in tokens) / n,
        "pt": sum(t in PT_MARKERS for t in tokens) / n,
        "ca": sum(t in CA_MARKERS for t in tokens) / n,
        "gl": sum(t in GL_MARKERS for t in tokens) / n,
    }
    pt_hits = sum(t in PT_MARKERS for t in tokens)
    if pt_hits >= 3 and any(t in {"não", "você", "vocês", "pelo", "pela"} for t in tokens):
        scores["pt"] = max(scores["pt"], scores["es"] + 0.05)
    label = max(scores, key=scores.get)
    if scores[label] < 0.02:
        label = "und"
    return label, scores


def fast_reject(text: str, profile: str) -> str | None:
    w = words(text)
    n = len(w)
    lo, hi = (20, 500_000) if profile == "books" else (50, 100_000)
    if n < lo:
        return "too_short"
    if n > hi:
        return "too_long"

    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return "low_alpha"
    mean_len = sum(len(t.strip("..,;:¡!¿?")) for t in w) / n
    wlo, whi = (2, 18) if profile == "books" else (3, 12)
    if not (wlo <= mean_len <= whi):
        return "wordlen"

    alpha = sum(ch.isalpha() for ch in text) / max(len(text), 1)
    if alpha < (0.55 if profile == "books" else 0.70):
        return "low_alpha"
    digit = sum(ch.isdigit() for ch in text) / max(len(text), 1)
    if digit > (0.30 if profile == "books" else 0.20):
        return "high_digit"

    url_n = len(URL_RE.findall(text))
    if n and url_n / n > (0.02 if profile == "books" else 0.05):
        return "high_url"
    if text.count("\ufffd") > (5 if profile == "books" else 0):
        return "bad_ocr"

    upper = sum(ch.isupper() for ch in letters) / len(letters)
    if upper > (0.50 if profile == "books" else 0.40):
        return "screaming"

    if profile == "web" and len(text) >= 400:
        if not re.search(r"[áéíóúñÁÉÍÓÚÑ]", text) and not text.isupper():
            return "no_spanish_orthography"

    low = [t.strip("..,;:¡!¿?\"").lower() for t in w]
    if sum(t in ES_STOP for t in low) < 3:
        return "no_stopwords"
    return None


def clean_document(text: str, profile: str = "web") -> dict:
    raw = text
    text = normalize(text)
    if not text:
        return {"keep": False, "reason": "extract_empty", "text": "", "recipe": RECIPE}

    text, n_banner = strip_banners(text)
    if not text:
        return {"keep": False, "reason": "boilerplate", "text": "", "banners": n_banner, "recipe": RECIPE}

    reason = fast_reject(text, profile)
    if reason:
        return {"keep": False, "reason": reason, "text": text, "banners": n_banner, "recipe": RECIPE}

    label, scores = heuristic_lang(text)
    if label == "pt":
        return {"keep": False, "reason": "not_spanish", "lang": label, "scores": scores, "text": text, "recipe": RECIPE}
    if label in {"ca", "gl"} and scores[label] >= scores.get("es", 0) + 0.02:
        return {"keep": False, "reason": "lang_ambiguous", "lang": label, "scores": scores, "text": text, "recipe": RECIPE}

    return {
        "keep": True,
        "reason": "ok",
        "lang": label,
        "scores": scores,
        "banners": n_banner,
        "n_words": len(words(text)),
        "text": text,
        "recipe": RECIPE,
        "input_chars": len(raw),
    }


def iter_inputs(paths: list[Path]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for p in paths:
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.suffix.lower() in {".txt", ".md"} and f.is_file():
                    if f.name.lower() == "readme.md":
                        continue
                    out.append((str(f), f.read_text(encoding="utf-8", errors="replace")))
        elif p.is_file():
            out.append((str(p), p.read_text(encoding="utf-8", errors="replace")))
        else:
            print(f"skip missing {p}", file=sys.stderr)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=RECIPE)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--profile", choices=("web", "books"), default="web")
    ap.add_argument("--jsonl-out", type=Path)
    args = ap.parse_args()

    hist: Counter[str] = Counter()
    kept = 0
    out_f = args.jsonl_out.open("w", encoding="utf-8") if args.jsonl_out else None
    try:
        for name, raw in iter_inputs(args.paths):
            rec = clean_document(raw, args.profile)
            rec["path"] = name
            hist[rec["reason"]] += 1
            if rec["keep"]:
                kept += 1
            print(f"{rec['reason']:24} {name}")
            if out_f and rec["keep"]:
                out_f.write(json.dumps({"id": name, "text": rec["text"], "recipe": RECIPE}, ensure_ascii=False) + "\n")
    finally:
        if out_f:
            out_f.close()

    total = sum(hist.values())
    print("---")
    print(f"recipe={RECIPE} profile={args.profile} docs={total} kept={kept}")
    for reason, n in hist.most_common():
        pct = 100.0 * n / total if total else 0
        print(f"  {reason:24} {n:4}  {pct:5.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
