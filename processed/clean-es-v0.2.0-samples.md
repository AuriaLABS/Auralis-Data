# Audit — clean-es-v0.2.0 on `samples/`

```text
python3 scripts/clean_es.py --profile web samples/
python3 scripts/test_clean_es.py
```

Single-document reasons plus batch exact-dedup (directory order):

| reason | files |
| --- | --- |
| ok | `keep_prose.txt` |
| boilerplate | `reject_banners.txt` |
| not_spanish | `reject_portuguese.txt` |
| no_spanish_orthography | `reject_ascii.txt` |
| too_short | `reject_short.txt` |
| dup_line | `reject_repeat.txt` |
| dup_doc | `z_dup_keep_prose.txt` |
| dup_paragraph | `z_shared_paragraph.txt` |

kept = 1 / 8. MinHash and PII are still out of this recipe.
