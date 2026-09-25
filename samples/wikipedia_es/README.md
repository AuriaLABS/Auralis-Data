# Wikipedia ES smoke slice

Five truncated article extracts (`MAX_CHARS=2500`) used as the first *accepted-source* text in Genesis.
Not a dump. Not a training corpus.

```bash
python3 scripts/fetch_wikipedia_es_slice.py
python3 scripts/clean_es.py --profile books samples/wikipedia_es/
```

`clean_es.py` skips `README.md` and currently ignores `.jsonl`; the extracts also live as the `text` field inside `slice.jsonl`.

License: CC BY-SA 4.0 (Wikimedia contributors). Checksum: [`../../checksums/wikipedia-es-slice-v0.1.0.sha256`](../../checksums/wikipedia-es-slice-v0.1.0.sha256).
