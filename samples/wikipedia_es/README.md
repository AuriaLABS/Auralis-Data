# Wikipedia ES smoke slice

Two layers:

1. **Pinned in git** (CI, no network): `wikipedia-es-1042.jsonl`, `wikipedia-es-1773.jsonl`, `wikipedia-es-136789.jsonl`. Short CC BY-SA extracts.
2. **Generated snapshot** (optional): `python3 scripts/fetch_wikipedia_es_slice.py` writes a 5-title, 2500-char `slice.jsonl` whose hash is `checksums/wikipedia-es-slice-v0.1.0.sha256`. Live Wikipedia can drift.

```bash
python3 scripts/clean_jsonl.py --profile books samples/wikipedia_es/
```

License: CC BY-SA 4.0 (Wikimedia contributors).
