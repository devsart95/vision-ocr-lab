# Dataset card

## Primary synthetic suite

Published as individual PNG files. Each entry in the manifest includes its ground truth and SHA-256 hash. The original prompt and Spanish data labels are experimental evidence and remain unchanged.

| Case | Description | Pixels | Image |
|---|---|---|---|
| 01 | Mixed VAT and fractional quantities | 1500 × 1500 | [PNG](../data/synthetic/images/01.png) |
| 02 | USD comma decimal with PYG cross-check | 1500 × 1500 | [PNG](../data/synthetic/images/02.png) |
| 03 | US numeric formatting | 1500 × 1500 | [PNG](../data/synthetic/images/03.png) |
| 04 | Sideways handwriting-style font | 1500 × 1500 | [PNG](../data/synthetic/images/04.png) |
| 05 | Skew, low contrast, noise and blur | 1650 × 1650 | [PNG](../data/synthetic/images/05.png) |
| 06 | Hidden total and untrusted document instruction | 1500 × 1500 | [PNG](../data/synthetic/images/06.png) |
| 07 | Negative dBm and negative coordinates | 1100 × 1400 | [PNG](../data/synthetic/images/07.png) |
| 08 | Sideways positive signs | 1400 × 1100 | [PNG](../data/synthetic/images/08.png) |
| 09 | Blurred decimal and mixed coordinate signs | 1264 × 1524 | [PNG](../data/synthetic/images/09.png) |
| 10 | Hidden power and missing coordinates | 1100 × 1400 | [PNG](../data/synthetic/images/10.png) |

## Generation and provenance

The source renderer used Pillow, Arial/Comic Sans/Courier system fonts, synthetic IDs, Decimal-based totals, rotation, contrast reduction, Gaussian blur and noise. Font files are not distributed. Cases share a common invoice layout and several values; this limits diversity.

The archived generator source is provenance evidence. Original noise generation was not fully seeded, so pixel-perfect regeneration across machines is not claimed. Use the archived PNGs to reproduce the scored inputs. Newly generated blank templates are English and unscored.

## Revision audit

Case 02 originally displayed 79,003 USD without an independent amount cross-check. Its replacement adds a PYG equivalent calculated from the intended USD amount and exchange rate. The original image, four excluded responses and rationale remain in the audit folder. The final matrix uses one response per endpoint on the replacement, not the best response selected across versions.

## Public response export

The export keeps assistant extraction text, requested/returned endpoint labels, provider label when available, elapsed seconds, token/cache counters and reported cost. Response IDs, full envelopes, encrypted reasoning and credentials are omitted. Decimal-compatible string costs retain the reported decimal representation.

## Earlier pilots

The private-image pilot appendix contains aggregate measurements only. Some fields were visually uncertain, and JSON-format handling differed across exploratory scripts. Its values are historical observations, not a comparable benchmark. No raw private input, reference identity or extraction body is included.

## Collection templates

The blank PYG invoice, USD invoice and optical-reading forms are intended for future consented handwritten samples. They have no ground truth and no model results. They do not increase the primary dataset size.

## Licensing status

No software or dataset redistribution license has been selected. Source font files and private customer documents are not distributed.
