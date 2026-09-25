#!/usr/bin/env python3
"""clean-es-v0.2.0 — stages 2–6 and exact dedup (8) of docs/cleaning.md.

Standard library only. Reason codes stay stable when GlotLID or MinHash wrap this.

Usage:
  python3 scripts/clean_es.py samples/
  python3 scripts/test_clean_es.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RECIPE = "clean-es-v0.2.0"

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
PUNCT_RE = re.compile(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]+", re.UNICODE)

GOPHER_TOP = ((2, 0.20), (3, 0.18), (4, 0.16))
GOPHER_DUP = ((5, 0.15), (6, 0.14), (7, 0.13), (8, 0.12), (9, 0.11), (10, 0.10))


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = CTRL_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def tokens_norm(text: str) -> list[str]:
    return [t for t in PUNCT_RE.sub(" ", text.lower()).split() if t]


def strip_banners(text: str) -> tuple[str, int]:
    kept, dropped = [], 0
    for line in text.split("\n"):
        if any(rx.search(line) for rx in BANNER_RES):
            dropped += 1
            continue
        kept.append(line)
    return "\n".join(kept).strip(), dropped


def heuristic_lang(text: str) -> tuple[str, dict]:
    tokens = [w.strip(".,;:¡!¿?\"'«»()[]").lower() for w in words(text)]
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
    mean_len = sum(len(t.strip(".,;:¡!¿?")) for t in w) / n
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
    low = [t.strip(".,;:¡!¿?\"").lower() for t in w]
    if sum(t in ES_STOP for t in low) < 3:
        return "no_stopwords"
    return None


def _ngrams(toks: list[str], n: int) -> list[tuple[str, ...]]:
    if len(toks) < n:
        return []
    return [tuple(toks[i : i + n]) for i in range(len(toks) - n + 1)]


def _gram_char_weight(gram: tuple[str, ...]) -> int:
    return sum(len(w) for w in gram) + max(len(gram) - 1, 0)


def repetition_reject(text: str) -> str | None:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if len(lines) >= 4:
        counts = Counter(lines)
        dup_lines = sum(c for ln, c in counts.items() if c > 1)
        if dup_lines / len(lines) > 0.30:
            return "dup_line"
        total_c = sum(len(ln) for ln in lines)
        dup_c = sum(len(ln) * c for ln, c in counts.items() if c > 1)
        if total_c and dup_c / total_c > 0.20:
            return "dup_line"

    toks = tokens_norm(text)
    total_c = sum(len(t) for t in toks) + max(len(toks) - 1, 0)
    if total_c == 0:
        return None
    for n, thr in GOPHER_TOP:
        grams = _ngrams(toks, n)
        if not grams:
            continue
        gram, cnt = Counter(grams).most_common(1)[0]
        if cnt * _gram_char_weight(gram) / total_c > thr:
            return "dup_ngram"
    for n, thr in GOPHER_DUP:
        grams = _ngrams(toks, n)
        if not grams:
            continue
        counts = Counter(grams)
        covered = 0
        for g, cnt in counts.items():
            if cnt > 1:
                covered += (cnt - 1) * _gram_char_weight(g)
        if covered / total_c > thr:
            return "dup_ngram"
    return None


def doc_hash(text: str) -> str:
    squeezed = re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()
    return hashlib.sha256(squeezed.encode("utf-8")).hexdigest()


def paragraphs(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return parts if parts else [text.strip()]


def para_hash(text: str) -> str:
    norm = PUNCT_RE.sub(" ", text.lower())
    norm = re.sub(r"\s+", " ", norm).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


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

    reason = repetition_reject(text)
    if reason:
        return {"keep": False, "reason": reason, "lang": label, "text": text, "recipe": RECIPE}

    return {
        "keep": True,
        "reason": "ok",
        "lang": label,
        "scores": scores,
        "banners": n_banner,
        "n_words": len(words(text)),
        "text": text,
        "doc_hash": doc_hash(text),
        "para_hashes": [para_hash(p) for p in paragraphs(text) if len(p) >= 40],
        "recipe": RECIPE,
        "input_chars": len(raw),
    }


def apply_exact_dedup(records: list[dict]) -> list[dict]:
    seen_docs: set[str] = set()
    seen_paras: set[str] = set()
    out = []
    for rec in records:
        if not rec.get("keep"):
            out.append(rec)
            continue
        dh = rec["doc_hash"]
        if dh in seen_docs:
            rec = dict(rec)
            rec["keep"] = False
            rec["reason"] = "dup_doc"
            out.append(rec)
            continue
        phs = rec.get("para_hashes") or []
        if any(p in seen_paras for p in phs):
            rec = dict(rec)
            rec["keep"] = False
            rec["reason"] = "dup_paragraph"
            out.append(rec)
            continue
        seen_docs.add(dh)
        seen_paras.update(phs)
        out.append(rec)
    return out


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

    raw_recs = []
    for name, raw in iter_inputs(args.paths):
        rec = clean_document(raw, args.profile)
        rec["path"] = name
        raw_recs.append(rec)
    recs = apply_exact_dedup(raw_recs)

    hist: Counter[str] = Counter()
    kept = 0
    out_f = args.jsonl_out.open("w", encoding="utf-8") if args.jsonl_out else None
    try:
        for rec in recs:
            hist[rec["reason"]] += 1
            if rec["keep"]:
                kept += 1
            print(f"{rec['reason']:24} {rec['path']}")
            if out_f and rec["keep"]:
                out_f.write(
                    json.dumps(
                        {"id": rec["path"], "text": rec["text"], "recipe": RECIPE, "doc_hash": rec.get("doc_hash")},
                        ensure_ascii=False,
                    )
                    + "\n"
                )
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
