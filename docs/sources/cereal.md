# Dataset card — `cereal`

## Identity

- **id:** `cereal`
- **display name:** CEREAL (Corpus del Español REAL)
- **card version:** `0.1.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** Cristina España-Bonet, Alberto Barrón-Cedeño; text from OSCAR / Common Crawl
- **canonical URL:** https://cereal-es.github.io/CEREAL/
- **download / snapshot URL:** https://zenodo.org/records/14771240 (CEREAL v2 note on the project page)
- **download or cutoff date:** pending
- **primary language:** es
- **other languages:** none intended
- **domain:** web

## License and use

- **license or terms:** annotations CC0 (authors' statement). **They do not hold copyright of the document text**, which comes from OSCAR and therefore Common Crawl.
- **text in `licenses/`:** not copied while quarantined
- **allows model training?** conditional (CC ToU / OSCAR terms on the text, not the CC0 of the labels)
- **allows commercial use?** conditional
- **attribution required:** yes if used (paper + OSCAR/CC)
- **extra restrictions:** country labels are the valuable part. Do not treat CEREAL as a clean-room corpus.

## Artifact

- **external uri:** Zenodo CEREAL I/II records
- **format:** bz2 per country code
- **approximate size:** ~13.5M gold documents (CEREAL) + ~28M silver (CEREALex), 24 countries
- **document / token count (if known):** pending slice
- **SHA-256 checksum:** pending
- **in git?** no

## Cleaning applied

- filters: n/a until un-quarantined
- deduplication: would overlap FineWeb-2 / OSCAR heavily
- PII / redaction: n/a
- quality notes: gold country-from-URL vs silver classifier (`docTransformer`)

## Use in Auralis

- **mixes that include it:** none
- **split:** n/a
- **mix weight:** 0
- **purpose:** variety tagging later, not raw pretrain mass

## Known risks

- Double-counting with FineWeb-2 if both are ingested as text.
- Silver labels are a classifier, not geography.

## Decision

- **status:** quarantine
- **reason:** useful dialect metadata, unclear right to treat the *text* as CC0. Revisit as a label layer on top of a source we already accept, not as a second web dump.
