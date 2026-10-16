# Limits and interpretation

## What these results support

On this fixed synthetic set, Gemini had the fewest field errors. Gemini and GPT-6 Sol each returned nine completely correct images. Luna had the lowest measured average request cost. These observations help choose the next pilot; they do not identify a statistically proven winner.

## What they do not support

- A model's general OCR, accounting, handwriting, security, or geolocation capability.
- A production error rate, reliability guarantee or tail-latency commitment.
- A claim about model weights alone: OpenRouter routing, provider behavior and caches are part of the measurement.
- A causal tolerance threshold for blur, rotation or contrast. Some cases combine degradations and there is no severity sweep.
- OCR character/word error rates, a calibrated confidence curve or meaningful ROC/PR curves.
- Physical calibration of the synthetic power-meter illustration. It is a visual transcription fixture.

## Design limitations

The inputs were hand-designed rather than randomly sampled. They share layouts, company names, IDs and dates. There is only one response per image/endpoint combination. Multiple fields repeat the same number, and expected null/routing values are included in field counts. A single interpretation mistake can therefore create several field errors; several easy nulls can inflate aggregate field accuracy.

Model selection was informed by earlier private-image pilots rather than preregistered. The experiment author generated and evaluated the stimuli. Independent annotation and blind adjudication were not performed. Case 02 was revised after observing model behavior, so it is development data. Responses were not cherry-picked across retries: every endpoint was rerun on the revised image and all earlier calls remain in the audit trail.

Default temperatures and seed behavior differ between providers. Reasoning requests do not standardize internal computation. Request durations were measured under limited concurrency, and endpoint aliases may change. Historical cost may include cache effects and does not include human correction or credit-purchase fees.

## Handwriting

The synthetic cases use fonts, including a handwriting-style font. They do not contain real handwriting. The earlier handwritten-photo pilot had uncertain reference values; only aggregate measurements are public, and they are not pooled into the headline table. A clean synthetic result cannot establish reliability on handwritten customer invoices.

The blank templates in `templates/` are collection aids, not additional evaluated cases. New data should be consented, annotated independently, and assigned a held-out split before tuning prompts or selecting models against it.

## Publication and privacy

Only synthetic primary images are public. Private source photographs, extracted personal fields, credentials, provider response IDs and encrypted reasoning are omitted. The aggregate pilot appendix cannot independently reproduce its private-image results; it exists to make the selection history visible. Synthetic identifier strings are not asserted to be valid, registered, or legally compliant.

The local secret-signature check is not proof that arbitrary future uploads are safe. Review every image and its metadata before adding it. Use a dedicated expiring API credential through the environment; offline commands require none. No blanket software/data license has been selected.

## Next useful experiments

1. Collect real handwriting across writers, vendors, layouts and lighting conditions with consent.
2. Independently transcribe critical fields and adjudicate disagreements against the original document.
3. Hold out layouts and writers; freeze the test set and prompt before evaluating candidates.
4. Repeat requests and record pinned provider routes, parameters, cache states and end-to-end cost.
5. Compare conventional OCR plus normalization and specialized document parsers under the same output contract.
6. Measure critical-field errors, abstention, human correction time and business-rule violations.

A larger benchmark is justified when a deployment decision needs these answers. It is not implied by a small lab's attractive chart.
