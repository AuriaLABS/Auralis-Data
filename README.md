# Auralis-Data

**Data** repository for [Auralis](https://github.com/AuriaLABS/Auralis) (AuriaLABS).

Auralis is the model: tokenizer, transformer, training, and inference in Rust.
Auralis-Data is the corpus factory: provenance, cleaning, mixes, licenses, and versioned manifests.

> The code repo does not hold the real corpus. The corpus does not train the model by itself.
> Every source lands with a license, a checksum, and a card that can be audited.

## Status

Bootstrap phase. Layout, policy, cleaning contract, and a stdlib cleaner for stages 2–5 exist. There are no pretraining shards or frozen mixes yet.

`data/corpus.txt` in the Auralis repo is a **development fixture**: a few Spanish sentences used to close the Genesis loop. It is not the training dataset.

Documentation and metadata are in **English**. The primary pretraining target is Spanish.

## Run the cleaner

```bash
python3 scripts/clean_es.py samples/
python3 scripts/test_clean_es.py
```

Recipe id: `clean-es-v0.1.0`. Contract: [docs/cleaning.md](docs/cleaning.md).

## Layout

```text
Auralis-Data/
  README.md
  LICENSE
  docs/           policy, cleaning contract, card template
  scripts/        clean_es.py (stages 2–5) and fixture tests
  samples/        tiny keep/reject clips for the cleaner
  manifests/      versioned mixes (empty)
  licenses/
  checksums/
  raw/ processed/ mixes/
```

Policy: [docs/policy.md](docs/policy.md).

## Repository license

Scaffolding is [MIT](LICENSE). Datasets keep their original licenses.
