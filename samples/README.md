# Samples

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

| File | Expected reason |
| --- | --- |
| `keep_prose.txt` | `ok` |
| `keep_pii.txt` | `ok` after redaction |
| `reject_banners.txt` | `boilerplate` |
| `reject_portuguese.txt` | `not_spanish` |
| `reject_ascii.txt` | `no_spanish_orthography` |
| `reject_short.txt` | `too_short` |
| `reject_repeat.txt` | `dup_line` |
| `z_dup_keep_prose.txt` | `dup_doc` after `keep_prose.txt` |
| `z_shared_paragraph.txt` | `dup_paragraph` after `keep_prose.txt` |

`keep_pii.txt` uses fictional `example.com` / example IBAN / `00000000T`. Do not put real personal data in this folder.
