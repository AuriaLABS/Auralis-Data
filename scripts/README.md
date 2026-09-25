# Scripts

- `clean_es.py` + `redact.py` — `clean-es-v0.3.0` on `.txt` / `.md`
- `clean_jsonl.py` — same recipe on JSONL records with a `text` field
- `fetch_wikipedia_es_slice.py` — optional 5-title Wikipedia snapshot
- `test_clean_es.py` — fixture reason codes

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
python3 scripts/clean_jsonl.py --profile books samples/wikipedia_es/
```

Still out: MinHash, GlotLID, PleIAs parquet streaming (smallest file ~139 MB).
