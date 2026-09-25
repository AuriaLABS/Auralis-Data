# Samples

Tiny clips for tests and CI. Anything large enough to need LFS or object storage does not belong here.

Allowed: short `.txt` or tiny `.json` / `.jsonl` that illustrate format. Not allowed: crawl extracts that still contain PII.

## clean-es-v0.1.0 fixtures

Run from the repo root:

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

| File | Expected reason |
| --- | --- |
| `keep_prose.txt` | `ok` |
| `reject_banners.txt` | `boilerplate` |
| `reject_portuguese.txt` | `not_spanish` |
| `reject_ascii.txt` | `no_spanish_orthography` |
| `reject_short.txt` | `too_short` |
