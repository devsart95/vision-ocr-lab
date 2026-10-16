# Operational context

Public exploratory vision extraction lab assembled from the recorded experiment on 2026-10-16.

## Scope

- Primary: archived synthetic images, known-answer manifest, original prompt, allowlisted provider responses, offline scoring and descriptive plots.
- Audit: original ambiguous USD case and its excluded calls; every endpoint was rerun after adding a PYG cross-check.
- Earlier private-image pilots: aggregate observations only, excluded from primary results.
- Blank English handwriting collection templates: unscored.

## Decisions

Magnitude: herramienta, confirmed by the owner. Publish publicly under Sarto. Public contact is justino.dev. No new paid model calls are required to assemble or verify this repository. No CI/CD pipeline was requested. No blanket redistribution license was selected.

## Scientific limits

Single observation per image/model, correlated layouts, default provider routing and sampling, synthetic fonts rather than handwriting, development-time case revision. Do not claim statistical superiority, production reliability, CER/WER, or a general OCR leaderboard.

## Reproduction

README and docs/REPRODUCIBILITY.md contain commands. Offline artifacts and plots are rebuilt from the package CLI. Historical PNG bytes are authoritative; the generation source used system fonts and partially unseeded noise.

## Publication status

Initial repository created publicly. Implementation is tracked in issue 1 and its publication PR. Verify the remote and branch before updating this status.
