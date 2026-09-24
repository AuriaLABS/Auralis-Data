# Data policy

Rules for accepting, describing, and versioning sources in Auralis-Data.
This is not legal advice. If a source is unclear, it does not go in.

## Principles

1. **Provenance before volume.** One sentence with origin and license beats an anonymous dump.
2. **Spanish first.** The pretraining corpus prioritizes Spanish. English and code are added with an explicit mix weight.
3. **License per source.** Mixing does not unify licenses. Each card states what may be trained, published, or cited.
4. **Git is not bulk storage.** Metadata and samples live here. Shards live elsewhere, referenced by checksum.
5. **Nothing is accepted on intuition.** Same rule as Auralis: a source lands when the card is complete and a manifest names it.

## Fast-reject criteria

Reject (or quarantine) a source if any of the following is true:

- no identifiable license or terms of use;
- the license forbids model training or commercial use and no documented exception exists;
- the material is clearly PII (emails, phone numbers, ID documents, medical records);
- sexual content involving minors, or exploitation;
- the text is mostly web boilerplate, captchas, carts, cookie banners, or unreadable OCR;
- origin cannot be reconstructed (URL, snapshot, hash, date).

## PII and safety

- Do not commit secrets, cookies, credentials, or real mail dumps.
- If an evaluation sample needs a personal detail, redact it or synthesize it.
- Cleaning logs that quote raw documents are not uploaded.

## Splits

Every versioned mix declares `train`, `validation`, and `test` (even if test is small at first). The Auralis fixture does not count as an evaluation split.

A document must not appear in two splits of the same mix. If leakage is found, ship a new manifest version; do not silently patch the previous one.

## Versioning

- A manifest has a stable name and a version (`genesis-mix-v0.1.0`).
- Changing weights, sources, or filters **bumps the version**.
- The published artifact checksum is stored under `checksums/`.
- Auralis should point at that triple (name, version, hash), not at “latest file on disk.”

## Relationship to the model

The [Auralis](https://github.com/AuriaLABS/Auralis) repo consumes data; it does not define it. When the 0.2 pipeline exists, this repository is the source of truth for *what* was trained, not for *how* tensors multiply.
