# Dataset card — `fineweb2-spa-latn`

## Identity

- **id:** `fineweb2-spa-latn`
- **display name:** FineWeb-2 Spanish (spa_Latn)
- **card version:** `0.1.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** Hugging Face FineData / FineWeb-2 authors (Penedo et al., 2025)
- **canonical URL:** https://huggingface.co/datasets/HuggingFaceFW/fineweb-2
- **download / snapshot URL:** `data/spa_Latn` subset; pending pin to a dataset revision SHA
- **download or cutoff date:** pending (upstream crawls: Common Crawl mid-2013 – April 2024)
- **primary language:** es
- **other languages:** Portuguese / Catalan / Galician leakage possible
- **domain:** web

## License and use

- **license or terms:** ODC-By 1.0 for the dataset release, **and** Common Crawl Terms of Use for the underlying crawl
- **text in `licenses/`:** `licenses/odc-by-1.0.txt` (pointer)
- **allows model training?** yes, subject to ODC-By attribution and CC ToU
- **allows commercial use?** yes under ODC-By; CC ToU still applies to the crawl origin
- **attribution required:** yes (ODC-By)
- **extra restrictions:** do not pretend Auralis-Data owns the crawl. Cite FineWeb2 (`arxiv:2506.20920`) and ODC-By.

## Artifact

- **external uri:** `hf://datasets/HuggingFaceFW/fineweb-2` subset `spa_Latn`
- **format:** parquet / arrow (upstream)
- **approximate size:** ~261.5B words, ~441.3M documents, ~1.32 TB UTF-8 / ~594 GB on disk (upstream table)
- **document / token count (if known):** see above; Auralis slice size pending
- **SHA-256 checksum:** pending
- **in git?** no

## Cleaning applied

- filters: upstream already ran GlotLID, per-language MinHash, FineWeb quality, PII/ftfy. Auralis still runs Spanish banners, accent-collapse, and cross-source exact dedup vs wiki/books
- deduplication: do not MinHash the whole FineWeb-2 dump again for Genesis; dedup only against other accepted sources
- PII / redaction: upstream + `clean-es` stage 7 on any slice we keep
- quality notes: web register, cookie leftovers, country mix unknown without CEREAL-style tags

## Use in Auralis

- **mixes that include it:** not in `genesis-mix-v0.1.0` (too large). Planned for Foundation (0.2) as the web mass
- **split:** train, with a hashed holdout after our cleaner
- **mix weight:** pending ablation; default web majority, books/wiki as quality upweight
- **purpose:** pretrain

## Known risks

- Spain + large LatAm news sites will dominate; Equatorial Guinea and Andean oral Spanish will not.
- ODC-By attribution must survive model cards.
- Re-hydrating via `minhash_cluster_size` is an upstream feature we do not use yet.

## Decision

- **status:** candidate
- **reason:** license and quality are acceptable; volume is Foundation-scale, not Genesis. Accept a *slice* only after a revision pin and a checksum.
