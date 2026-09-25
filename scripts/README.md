# Scripts

## `clean_es.py`

Recipe `clean-es-v0.2.0`. Stages 2–6 of [docs/cleaning.md](../docs/cleaning.md) plus exact document/paragraph dedup (stage 8, no MinHash yet).

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

Reason codes: `ok`, `extract_empty`, `boilerplate`, `too_short`, `too_long`, `wordlen`, `low_alpha`, `high_digit`, `high_url`, `bad_ocr`, `screaming`, `no_spanish_orthography`, `no_stopwords`, `not_spanish`, `lang_ambiguous`, `dup_line`, `dup_ngram`, `dup_doc`, `dup_paragraph`.

`--profile web` (default) or `books`. `--jsonl-out` writes kept documents only.

Changing a threshold or adding a reason code bumps the recipe version.
