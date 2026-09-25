# Auralis-Data

**Data** repository for [Auralis](https://github.com/AuriaLABS/Auralis) (AuriaLABS).

Auralis is the model. Auralis-Data is the corpus factory: provenance, cleaning, mixes, licenses, manifests.

Documentation is in **English**. Conversation about the project may be in Spanish. The pretraining target is Spanish.

## Status

- Cleaner: `clean-es-v0.3.0` (`scripts/clean_es.py`, `scripts/redact.py`).
- First mix: [`manifests/genesis-mix-v0.1.0.yaml`](manifests/genesis-mix-v0.1.0.yaml) (smoke samples only).
- Source cards: [`docs/sources/`](docs/sources/). No external shard has a checksum yet.

## Run

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

## Sources (decisions)

| Source | Status |
| --- | --- |
| PleIAs Spanish-PD-Books | accepted |
| Spanish Wikipedia | accepted |
| FineWeb-2 `spa_Latn` | candidate (Foundation) |
| PleIAs Spanish-PD-Newspapers | candidate |
| CEREAL | quarantine (labels vs OSCAR text) |
| esCorpius | rejected (CC BY-NC-ND) |

Policy: [docs/policy.md](docs/policy.md). Cleaning: [docs/cleaning.md](docs/cleaning.md).

Scaffolding is [MIT](LICENSE). Datasets keep their original licenses.
