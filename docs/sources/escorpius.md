# Dataset card — `escorpius`

## Identity

- **id:** `escorpius`
- **display name:** esCorpius
- **card version:** `0.1.0`
- **card date:** 2026-09-25
- **owner:** AuriaLABS / Auralis-Data

## Origin

- **publisher or author:** Gutiérrez-Fandiño et al. / LHF Labs
- **canonical URL:** https://huggingface.co/datasets/LHF/escorpius
- **download / snapshot URL:** n/a
- **download or cutoff date:** n/a
- **primary language:** es
- **other languages:** none intended
- **domain:** web

## License and use

- **license or terms:** CC BY-NC-ND 4.0 (dataset card and LINDAT record)
- **text in `licenses/`:** not copied; rejected sources do not get a local license file
- **allows model training?** conditional / no for a model Auralis may release commercially
- **allows commercial use?** no
- **attribution required:** yes, if it were used
- **extra restrictions:** ND forbids derivatives of the corpus itself; NC forbids commercial use. Pretraining a released model on it is the use we will not take on.

## Artifact

- **external uri:** `hf://datasets/LHF/escorpius`
- **format:** pending
- **approximate size:** ~322.5 GB ES / ~50.8B words (authors' comparison table)
- **document / token count (if known):** pending
- **SHA-256 checksum:** n/a
- **in git?** no

## Cleaning applied

- filters: n/a
- deduplication: n/a
- PII / redaction: n/a
- quality notes: cleaning quality is high (dLHF); the block is the license, not the text quality

## Use in Auralis

- **mixes that include it:** none
- **split:** n/a
- **mix weight:** 0
- **purpose:** n/a

## Known risks

- Using it “just to train locally” still poisons a later public checkpoint.

## Decision

- **status:** rejected
- **reason:** CC BY-NC-ND 4.0. FineWeb-2 and PleIAs cover the same web/book roles with licenses that allow training.
