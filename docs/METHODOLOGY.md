# Methodology

## Question and unit of measurement

Can a multimodal endpoint extract administrative and field-service data while preserving numbers, identifiers, signs and unknown values? The experimental unit is one image/request, not an individual character or field. This is an exploratory convenience sample, not a population sample.

The primary experiment has ten synthetic images and four OpenRouter endpoints. Each endpoint receives each image once. The final matrix contains forty responses. Four superseded case-02 requests remain separately auditable and billable.

## Request protocol

- Endpoint: OpenRouter Chat Completions, `POST /api/v1/chat/completions`.
- Endpoint IDs and catalog snapshot: [run metadata](../data/synthetic/run.json).
- Exact user prompt: [prompt.txt](../data/synthetic/prompt.txt). Spanish, unchanged from the experiment.
- A user message contains that prompt and one original PNG as a base64 data URL.
- No expected answers, case titles, prior model answers, or previous chat turns are sent.
- `max_tokens=4096`; reasoning request `effort=low, exclude=true`.
- Temperature and generation seed use provider defaults. A fixed seed only shuffled job order.
- Four requests were allowed concurrently. Providers were selected by OpenRouter rather than pinned.
- No cropping, deskewing, enhancement, external OCR, or post-model correction was applied to a scored input.
- Prompt-only JSON instruction, without an enforced JSON Schema response format.

Reasoning settings are requests to the routing layer, not evidence that all providers execute identical internal reasoning. Cost and latency measure the endpoint as served. This is not a controlled comparison of model weights alone. [OpenRouter image input documentation](https://openrouter.ai/blog/tutorials/send-image-to-llm/).

## Ground truth and generation

Python/Pillow rendered the synthetic fields from known values. Decimal arithmetic produced displayed totals and the PYG reference. The [manifest](../data/synthetic/cases.json) binds each PNG to a SHA-256 hash and expected JSON object. Most truth values existed before the first calls.

Case 02 is the disclosed exception to an immutable original stimulus: its first image was judged ambiguous after observing differing interpretations. A PYG equivalent was added, then all four endpoints were rerun with the same prompt/settings. Neither endpoint-specific prompts nor selective best responses were used. The revised case is exploratory development data, not an untouched holdout.

The archived PNGs define the evaluated stimulus. The [historical generation source](../data/synthetic/generator-source.py.txt) is retained as provenance, not offered as a byte-identical cross-platform renderer: its original fonts were system fonts and its noise renderer was not fully seeded. No proprietary font files are redistributed. Offline result/figure reproduction uses the archived PNGs and responses and does not rerender the dataset.

## Scoring

The evaluator recursively flattens expected and returned JSON objects and compares their leaf fields. Extra returned leaf fields fail whole-image exact match. Missing fields fail; missing is not equivalent to `null`.

| Value | Comparison |
|---|---|
| Amounts, rates, quantities, coordinates, dBm | Decimal numeric equivalence; finite values only |
| Tax IDs, timbrado, invoice numbers, dates, currency code | Exact value |
| Company names, descriptions and payment condition | Case/punctuation/diacritic-insensitive text normalization |
| Expected unknown or hidden field | Must be explicit `null` |

`6.454` and `6454` are different numbers under the requested normalized schema. A thousands-separator error therefore counts as a data error even when the visible glyphs were recognized. Positive signs and trailing zeros do not change numeric meaning. Identifiers are not repaired by removing spaces.

Whole-image exact match requires every expected leaf to match, no extra leaf, and matching container types, object keys and array lengths (including empty containers). “Ready” additionally requires direct JSON and the implemented numeric/identifier string checks. These checks are deliberately narrower than a complete JSON Schema validator; the published suite has no readiness-only failures. The evaluator does not validate accounting compliance, taxpayer identity, physical meter calibration, or business correctness of the source document.

There are 154 scored leaves per endpoint, including routing fields, expected nulls and repeated values. Field accuracy is descriptive and can look high despite a consequential amount error. It is not character error rate, word error rate, or an independent-sample accuracy estimate.

## Timing and cost

Duration uses a client monotonic clock around the HTTP request. It includes image upload, routing, provider generation and network time. Reported means/medians describe the recorded concurrent workload. Ten observations are insufficient to estimate tail latency reliably.

Cost is copied from each response's `usage.cost`; aggregation uses Decimal. Recorded token counts and cache counters are retained. No token-price multiplication substitutes for actual returned cost. The per-thousand projection is:

```text
projected_cost = sum(recorded_call_cost) / scored_call_count * 1000
```

It applies only to this image/prompt/output mix. It excludes customer review, infrastructure and credit-purchase fees. Original excluded-case costs are counted in the actual experiment budget but not the final matrix's per-model averages.

## Reproduction and publication checks

The offline commands validate hashes, a complete unique matrix, Pydantic artifact schemas, stop reasons, the total recorded budget and public-content rules. Unit cases distinguish a correct decimal from a separator error, dropped signs, altered IDs, unknown values and fenced JSON.

The publication export omits full provider envelopes, encrypted reasoning, response IDs and private pilots' images/extractions. No paid requests were made while assembling this repository. Replays are opt-in and write new files outside the historical dataset.

## Post-publication scoring audit

A follow-up audit found that leaf flattening alone could accept a list replaced by an indexed object, or extra empty objects/array elements. The evaluator now rejects these structural differences before granting exact/ready status. Regression cases failed before the correction and pass afterward. None of the archived primary responses contains these mismatches; the published scores, costs and ranking are unchanged. This remains a limited extraction evaluator rather than a complete JSON Schema validator.
