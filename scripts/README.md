# Scripts

## `clean_es.py` + `redact.py`

Recipe `clean-es-v0.3.0`. Stages 2–7 of [docs/cleaning.md](../docs/cleaning.md), exact document/paragraph dedup, and a hash split.

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

PII placeholders (document is kept): `<EMAIL>` `<IP>` `<IBAN>` `<PHONE>` `<ID>`.
DNI/NIE are replaced only when the checksum letter is valid. Phones require `+34` and a 6xx/7xx mobile pattern.

Splits: first 8 hex digits of `doc_hash` → ~90% `train`, 5% `validation`, 5% `test`. The hash is computed **after** redaction so raw PII is not part of the id.

JSONL fields when `--jsonl-out` is set: `id`, `text`, `recipe`, `doc_hash`, `split`, `pii`.

Still out: MinHash, GlotLID, Gopher toxicity classifiers.
