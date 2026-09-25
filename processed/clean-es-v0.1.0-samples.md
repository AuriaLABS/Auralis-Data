# Audit — clean-es-v0.1.0 on `samples/`

Not a corpus audit. This pins the fixture histogram so a recipe change is visible.

```text
python3 scripts/clean_es.py --profile web samples/
```

| reason | n | % |
| --- | --- | --- |
| ok | 1 | 20 |
| boilerplate | 1 | 20 |
| not_spanish | 1 | 20 |
| no_spanish_orthography | 1 | 20 |
| too_short | 1 | 20 |

kept = 1 / 5. Profile = web.
