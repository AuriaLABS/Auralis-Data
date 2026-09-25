# Audit — genesis-mix-v0.2.0 Wikipedia slice

```bash
python3 scripts/fetch_wikipedia_es_slice.py
python3 scripts/clean_jsonl.py --profile books samples/wikipedia_es/slice.jsonl
```

Snapshot hash: `faf819bb6aaa3cbafd1a4c39b3c1808bf230476b0ddf5fe3780ad19cdacd855c`

| id | reason | split (this snapshot) |
| --- | --- | --- |
| wikipedia-es-1042 | ok | train |
| wikipedia-es-1773 | ok | train |
| wikipedia-es-136789 | ok | train |
| wikipedia-es-2543 | ok | train |
| wikipedia-es-3599 | ok | test |

kept = 5 / 5 under `books`. Live Wikipedia can move a document across splits only if the extract text changes and the hash is bumped.
