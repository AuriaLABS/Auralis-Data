# Scripts

## `clean_es.py`

Implements stages 2–5 of [docs/cleaning.md](../docs/cleaning.md) as recipe `clean-es-v0.1.0`.
Standard library only. Language ID is a heuristic gate (Spanish stopwords vs Portuguese/Catalan/Galician markers), not GlotLID.

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

`--profile web` (default) uses the strict floors. `--profile books` loosens length and OCR.
`--jsonl-out` writes kept documents only.

Reason codes must stay stable across versions. Changing a threshold bumps the recipe version.
