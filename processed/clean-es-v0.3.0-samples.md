# Audit — clean-es-v0.3.0 on `samples/`

```bash
python3 scripts/clean_es.py --profile web samples/
python3 scripts/test_clean_es.py
```

Kept after redaction: `keep_prose.txt`, `keep_pii.txt`.
`keep_pii.txt` must contain `<EMAIL> <IBAN> <PHONE> <ID>` and none of the raw values.

Split of a document is a function of `doc_hash[:8]` after redaction (90/5/5). It is stable for a given recipe and text; it is not meaningful on eight files.

Still missing from a published mix: MinHash, a real language ID, and a checksummed shard off-git.
