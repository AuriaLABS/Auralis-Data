# Auralis-Data

**Data** repository for [Auralis](https://github.com/AuriaLABS/Auralis) (AuriaLABS).

Auralis is the model: tokenizer, transformer, training, and inference in Rust.
Auralis-Data is the corpus factory: provenance, cleaning, mixes, licenses, and versioned manifests.

> The code repo does not hold the real corpus. The corpus does not train the model by itself.
> Every source lands with a license, a checksum, and a card that can be audited.

## Status

Bootstrap phase. The repository layout exists; there are no pretraining shards or frozen mixes yet.

`data/corpus.txt` in the Auralis repo is a **development fixture**: a few Spanish sentences used to close the Genesis loop (train, save a checkpoint, generate text). It is not the training dataset.

Documentation and metadata are in **English**. The primary pretraining target is Spanish, with English and code added when a mix justifies the weight.

## What belongs here

- Dataset cards (origin, language, license, cutoff date, known biases).
- Mix manifests: which sources, which weight, which split.
- Cleaning recipes and reject criteria.
- Checksums (`SHA-256`) of versioned artifacts.
- Per-source license texts.
- Small samples and evaluation sets that fit in git.
- Scripts or notes that document how an artifact was built.

## What does not belong in git

- Crawl dumps, massive `.parquet` / `.arrow` / `.jsonl`, tarballs, tokenized shards (`.bin`, `.idx`).
- Model checkpoints (`auralis.bin` and equivalents).
- Secrets, cookies, credentials, or unredacted PII.

Those artifacts live elsewhere (object storage or a training disk). This repo keeps the pointer: URI, size, checksum, and card.

That is not repo aesthetics. GitHub is not a data lake; multi-gigabyte pushes break clones, CI, and history. Auralis 0.2 calls for larger datasets and a data pipeline; that pipeline must be reproducible without cloning terabytes.

## Layout

```text
Auralis-Data/
  README.md                 this file
  LICENSE                   license for repo scaffolding (not for each corpus)
  docs/
    policy.md               acceptance rules, PII, attribution
    cleaning.md             Spanish-first cleaning pipeline
    card.template.md        dataset-card template
  manifests/                versioned mixes and inventories (JSON/YAML)
  licenses/                 per-source license texts or excerpts
  checksums/                SHA-256 of published artifacts
  samples/                  tiny clips for tests and CI
  raw/                      provenance notes; not the dump
  processed/                notes on the cleaned corpus; not the shards
  mixes/                    train/val/test mix recipes
```

`raw/`, `processed/`, and `mixes/` hold **descriptions and pointers**, not binaries. If a file is more than a few megabytes, it does not belong in git.

## Relationship to Auralis

| Piece | Where | Role |
| --- | --- | --- |
| Engine, tokenizer, train/eval/chat | [AuriaLABS/Auralis](https://github.com/AuriaLABS/Auralis) | code |
| Fixture `data/corpus.txt` | Auralis repo | smoke / Genesis |
| Corpora, mixes, cards | this repo | data |
| Checkpoints | outside both repos | training artifacts |

When the first usable mix exists, Auralis should reference it by **name + version + checksum**, not by “a file someone left on disk.”

This tracks the Auralis roadmap:

- **0.1 Genesis** — loop on a tiny corpus (already covered by the fixture).
- **0.2 Foundation** — larger datasets, train/val/test splits, perplexity.
- **0.7 Multimodal** — versioned multimodal datasets, later.

## Adding a source

1. Copy `docs/card.template.md` to `docs/sources/<id>.md`.
2. Record a stable URL or identifier, download date, license, and restrictions.
3. If the artifact is large, publish the checksum under `checksums/` and the URI in the manifest. Do not upload the blob.
4. If it belongs in a mix, edit `manifests/` and `mixes/` in the same change.
5. Any source without a clear license, or with obvious PII, stays out until that is resolved.

Policy: [docs/policy.md](docs/policy.md).  
Cleaning recipe: [docs/cleaning.md](docs/cleaning.md).

## Repository license

Scaffolding (documentation, templates, empty manifests, future scripts) is [MIT](LICENSE), same as Auralis.

**That does not cover the datasets.** Each source keeps its original license. Training on or redistributing a corpus requires reading `licenses/` and the matching card. Mixing sources does not create a new license or erase the old ones.
