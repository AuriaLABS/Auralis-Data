# Dataset card — `pleias-spanish-pd-books`

## Identity

- **id:** `pleias-spanish-pd-books`
- **display name:** PleIAs Spanish Public Domain Books
- **card version:** `0.1.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** PleIAs (curation); texts from Biblioteca Digital Hispánica / BNE and Internet Archive
- **canonical URL:** https://huggingface.co/datasets/PleIAs/Spanish-PD-Books
- **download / snapshot URL:** pending (no shard pulled yet)
- **download or cutoff date:** pending
- **primary language:** es
- **other languages:** occasional Latin, Catalan, or other languages inside historical volumes — pending audit
- **domain:** books

## License and use

- **license or terms:** public domain in all regions, per the dataset card (EU 70-year post-mortem rule; 2019 Copyright Directive art. 14 cited by PleIAs)
- **text in `licenses/`:** `licenses/pleias-spanish-pd-books.txt`
- **allows model training?** yes
- **allows commercial use?** yes
- **attribution required:** not as a copyright condition; cite PleIAs for provenance
- **extra restrictions:** none stated on the card. OCR quality varies. Do not treat the HF wrapper as creating a new copyright.

## Artifact

- **external uri:** `hf://datasets/PleIAs/Spanish-PD-Books`
- **format:** parquet (full text of ~2_000 books per file, per the card)
- **approximate size:** 302_640 texts, ~13.9B words (card as of March 2024)
- **document / token count (if known):** 302_640 documents; token count pending our tokenizer
- **SHA-256 checksum:** pending
- **in git?** no

## Cleaning applied

- filters: `clean-es` profile `books` when a slice is pulled (skip cookie banners)
- deduplication: exact document/paragraph vs Wikipedia and vs newspapers
- PII / redaction: run anyway; historical books still leak later annotations
- quality notes: expect OCR, hyphenation, long-s leftovers, catalog front matter

## Use in Auralis

- **mixes that include it:** `genesis-mix-v0.1.0` (planned slice, not pulled), `foundation` later
- **split:** train (default); hold out a title list before packing
- **mix weight:** high for quality, low for recency
- **purpose:** pretrain

## Known risks

- Peninsular and historical Spanish dominate; Latin America is under-represented.
- OCR noise can teach broken morphology if the books profile is too loose.
- Temporal skew: authors dead >70 years.
- Some volumes are catalogs or bilingual editions.

## Decision

- **status:** accepted
- **reason:** clearest high-quality Spanish source with an explicit public-domain claim. No shard in object storage yet; the card accepts the *source*, not a checksummed slice.
