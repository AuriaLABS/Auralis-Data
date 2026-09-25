# Samples

Tiny clips for tests and CI.

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
| `reject_repeat.txt` | `dup_line` |
| `z_dup_keep_prose.txt` | `dup_doc` after `keep_prose.txt` |
| `z_shared_paragraph.txt` | `dup_paragraph` after `keep_prose.txt` |

The `z_` prefix keeps those files after `keep_prose.txt` when the cleaner walks the directory in name order.
