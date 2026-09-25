# Dataset card — `pleias-spanish-pd-newspapers`

## Identity

- **id:** `pleias-spanish-pd-newspapers`
- **display name:** PleIAs Spanish Public Domain Newspapers
- **card version:** `0.1.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** PleIAs; sources include BDH / BNE and Internet Archive
- **canonical URL:** https://huggingface.co/datasets/PleIAs/Spanish-PD-Newspapers
- **download / snapshot URL:** pending
- **download or cutoff date:** pending
- **primary language:** es
- **other languages:** pending audit
- **domain:** news

## License and use

- **license or terms:** public domain in all regions (same PleIAs PD claim as the books set)
- **text in `licenses/`:** `licenses/pleias-spanish-pd-books.txt` (same PD note)
- **allows model training?** yes
- **allows commercial use?** yes
- **attribution required:** cite PleIAs for provenance
- **extra restrictions:** OCR and layout noise. Historical news is not current events.

## Artifact

- **external uri:** `hf://datasets/PleIAs/Spanish-PD-Newspapers`
- **format:** parquet
- **approximate size:** 247_491 texts, ~2.70B words (upstream card)
- **document / token count (if known):** 247_491 documents
- **SHA-256 checksum:** pending
- **in git?** no

## Cleaning applied

- filters: `clean-es` web-ish OCR: keep `bad_ocr` loose, still drop repeated mastheads
- deduplication: across issues and vs books
- PII / redaction: historical names stay; modern emails in catalog notes go
- quality notes: 19th/early-20th-century press register

## Use in Auralis

- **mixes that include it:** Foundation candidate, not Genesis
- **split:** train
- **mix weight:** low-to-medium
- **purpose:** pretrain

## Known risks

- OCR, column bleed, serialized novels mixed with news.
- Spain-heavy geographic bias.

## Decision

- **status:** candidate
- **reason:** same legal story as the books set; lower priority than books for a small model (OCR + register).
