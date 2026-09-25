# Dataset card — `wikipedia-es`

## Identity

- **id:** `wikipedia-es`
- **display name:** Spanish Wikipedia
- **card version:** `0.1.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** Wikimedia contributors
- **canonical URL:** https://es.wikipedia.org/
- **download / snapshot URL:** https://dumps.wikimedia.org/eswiki/ (dump date pending pin)
- **download or cutoff date:** pending
- **primary language:** es
- **other languages:** quotations and code samples in other languages
- **domain:** other (encyclopedia)

## License and use

- **license or terms:** CC BY-SA 4.0 (and GFDL for older text). Share-alike applies to *adapted* Wikipedia text, not automatically to model weights; still attribute in the model card.
- **text in `licenses/`:** `licenses/cc-by-sa-4.0.txt` (pointer)
- **allows model training?** yes
- **allows commercial use?** yes, with attribution and SA on adapted text dumps
- **attribution required:** yes
- **extra restrictions:** do not re-publish the dump as if it were public domain. Follow Wikimedia dump terms.

## Artifact

- **external uri:** `https://dumps.wikimedia.org/eswiki/`
- **format:** xml.bz2 dump → extracted text
- **approximate size:** pending dump date
- **document / token count (if known):** pending
- **SHA-256 checksum:** pending
- **in git?** no (a tiny extract may live under `samples/` later)

## Cleaning applied

- filters: wikiextractor; skip HTML banners; `clean-es` books-loose length floor
- deduplication: exact paragraph vs PleIAs and FineWeb (Wikipedia is widely copied)
- PII / redaction: living-person articles can contain phones or emails; run stage 7
- quality notes: high signal, encyclopedia register, Spain-centric project culture with large LatAm editor base

## Use in Auralis

- **mixes that include it:** planned for Foundation; optional tiny extract for a later Genesis bump
- **split:** train; reserve a list of titles for eval leakage checks
- **mix weight:** medium (quality upweight, not mass)
- **purpose:** pretrain

## Known risks

- Lead-section style and citation tails.
- Dump date must be pinned or eval leakage is un-auditable.

## Decision

- **status:** accepted
- **reason:** standard, attributable encyclopedia source. No dump file is stored yet.
