# Dataset card — `wikipedia-es`

## Identity

- **id:** `wikipedia-es`
- **display name:** Spanish Wikipedia
- **card version:** `0.2.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** Wikimedia contributors
- **canonical URL:** https://es.wikipedia.org/
- **download / snapshot URL:** API extracts via `scripts/fetch_wikipedia_es_slice.py` (smoke); full dump still `https://dumps.wikimedia.org/eswiki/`
- **download or cutoff date:** 2026-09-25 for the smoke slice; dump date pending
- **primary language:** es
- **other languages:** quotations in other languages
- **domain:** other (encyclopedia)

## License and use

- **license or terms:** CC BY-SA 4.0
- **text in `licenses/`:** `licenses/cc-by-sa-4.0.txt`
- **allows model training?** yes
- **allows commercial use?** yes, with attribution
- **attribution required:** yes
- **extra restrictions:** Wikimedia dump terms for a future full dump

## Artifact

- **external uri:** MediaWiki API (`action=query&prop=extracts&explaintext=1`)
- **format:** jsonl smoke slice
- **approximate size:** 5 titles × 2500 characters
- **document / token count (if known):** 5 documents
- **SHA-256 checksum:** `checksums/wikipedia-es-slice-v0.1.0.sha256` (of generated `samples/wikipedia_es/slice.jsonl`)
- **in git?** fetcher + checksum + this card; JSONL is generated

Titles pinned: Idioma español, Miguel de Cervantes, Biblioteca Nacional de España, Real Academia Española, Literatura española.

## Cleaning applied

- filters: `clean-es --profile books` on the generated texts
- deduplication: n/a at five documents
- PII / redaction: stage 7 if the extract contains an email
- quality notes: lead-section encyclopedia register; living-person pages not in this title list except as institutions

## Use in Auralis

- **mixes that include it:** `genesis-mix-v0.2.0`
- **split:** hashed 90/5/5 after clean-es
- **mix weight:** 1.0 for the smoke slice; full dump still weight 0
- **purpose:** smoke / pretrain seed

## Known risks

- Re-fetching live Wikipedia can change the checksum. Bump the slice version when that happens.
- This is not a substitute for an `eswiki` dump.

## Decision

- **status:** accepted
- **reason:** first accepted source with a reproducible slice builder. Full dump still pending.
