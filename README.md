<p align="center"><img src="figures/cover.png" alt="Vision OCR Lab: a small experiment, not a general OCR leaderboard" width="100%"></p>

<p align="center">
  <a href="#results">Results</a> · <a href="docs/METHODOLOGY.md">Methodology</a> · <a href="docs/DATASET.md">Dataset</a> · <a href="docs/RESEARCH.md">Research</a> · <a href="#reproduce-offline">Reproduce</a> · <a href="https://justino.dev">justino.dev</a>
</p>

# Vision OCR Lab

**Which vision model can extract useful structured data without changing the numbers?** This small lab tests invoices and optical power-meter readings, with exact answers, recorded API costs, and visible failures.

The main experiment contains **10 synthetic images, four model endpoints, and 40 scored calls**. Every image is published separately, with its ground truth and provider response. Four earlier calls on a revised stimulus remain in the audit trail, including their cost.

> **Small-lab disclaimer:** these are exploratory observations from a hand-built, correlated dataset. One call per image and model. No statistical winner, no production accuracy estimate, no real-handwriting benchmark. A font that resembles handwriting is still a font.

## Results

**Gemini 3.8 Flash is the strongest candidate to test next for invoices in this setup.** It matched GPT-6 Sol on completely correct images, made fewer field errors, and cost less. GPT-6 Luna was the cheapest endpoint. That is a workload-specific observation, not a claim that one model is universally better at OCR.

| Endpoint | Exact images | Correct fields | Mean / median latency | Recorded cost | Projected USD / 1,000 requests |
|---|---:|---:|---:|---:|---:|
| **Gemini 3.8 Flash** | **9/10** | **153/154** | 5.93 / 4.30 s | $0.01928925 | **$1.93** |
| GPT-6 Sol | **9/10** | 151/154 | **3.86 / 3.66 s** | $0.084165 | $8.42 |
| GPT-6 Luna | 7/10 | 149/154 | 5.21 / 4.45 s | **$0.00473825** | **$0.47** |
| Claude Haiku 5.5 | 7/10 | 149/154 | 5.82 / 3.80 s | $0.00575710 | $0.58 |

Costs come from OpenRouter's returned `usage.cost`, including the behavior of its chosen providers and caching. The projection uses the average request cost of this exact image mix; it excludes human review and credit-purchase fees. It is **not a fixed price per invoice**. Latency includes client/network/provider time under four concurrent requests.

The 154 fields include document routing, repeated identifiers, and expected `null` values. They are not independent samples. Whole-image exact match is the stricter headline: one wrong field makes the image fail. [Machine-readable results](results/summary.json).

<img src="figures/cost-quality.png" alt="Observed cost versus whole-image exact match, with a logarithmic cost axis" width="100%">

### What actually failed

- **Gemini:** in the sideways invoice, returned exchange rate `6.454` instead of normalized `6454`.
- **GPT-6 Sol:** read `79,003 USD` as `79003`, despite a visible PYG cross-check. The mistake propagated into unit price, line amount, and total.
- **GPT-6 Luna:** made that same monetary interpretation error and mishandled exchange-rate separators in other cases.
- **Haiku:** mishandled some separators, inserted a space inside a tax ID, and returned `450.000` where the normalized value was `450000`.

All endpoints returned direct JSON in the scored suite. All passed the four meter cases, including signed coordinates, hidden power, and absent coordinates. All left the masked invoice total as `null` and ignored the instruction embedded in that document. These isolated successes do not establish general prompt-injection resistance.

**Practical implication:** separate visual transcription from monetary normalization and arithmetic validation. A tiny character error can change an amount drastically while the JSON remains valid. Never silently “repair” an unreadable source using a calculated answer.

## The test set

<img src="figures/dataset-gallery.png" alt="Contact sheet of the ten individually published synthetic test images" width="100%">

| Case | Input | Stress tested |
|---|---|---|
| [01](data/synthetic/images/01.png) | Invoice | Mixed VAT rates, multiple lines, fractional quantity |
| [02](data/synthetic/images/02.png) | USD invoice | Decimal comma, thousands separators, PYG cross-check |
| [03](data/synthetic/images/03.png) | USD invoice | US number formatting and multiple lines |
| [04](data/synthetic/images/04.png) | Invoice | Handwriting-style font, sideways orientation |
| [05](data/synthetic/images/05.png) | Invoice | Skew, reduced contrast, blur and noise |
| [06](data/synthetic/images/06.png) | Invoice | Hidden total, document-borne instruction |
| [07](data/synthetic/images/07.png) | Meter | Negative dBm and negative coordinates |
| [08](data/synthetic/images/08.png) | Meter | Positive signs, sideways orientation |
| [09](data/synthetic/images/09.png) | Meter | Blur, skew, decimal power and mixed coordinate signs |
| [10](data/synthetic/images/10.png) | Meter | Masked power and missing coordinates: abstention |

Historical stimuli and the exact API prompt are in Spanish; they remain unchanged for auditability. The documentation and analysis are in English. The layouts are simplified and share names, identifiers and structure. The synthetic meter display is a transcription fixture, not a physically calibrated instrument simulation; distracting uW values are not guaranteed consistent with dBm.

<img src="figures/case-heatmap.png" alt="Per-case field-correctness heatmap with exact counts" width="100%">

## Technical curves and maps

The [cost/quality scatter](figures/cost-quality.svg), [case heatmap](figures/case-heatmap.svg), [exact-match bars](figures/exact-match.svg), and [latency ECDF](figures/latency-ecdf.svg) are generated from the recorded responses. SVG and PNG versions are provided.

<img src="figures/latency-ecdf.png" alt="Empirical latency distributions, ten observed requests per endpoint" width="100%">

There are no fitted degradation curves, ROC/PR curves, or significance claims: this experiment did not sweep controlled severity levels, collect calibrated confidences, or repeat calls. The ECDF is descriptive, not a service-level promise.

## Reproduce offline

Requires Python and [uv](https://docs.astral.sh/uv/). The lockfile pins dependencies.

```bash
uv sync --locked
uv run python -m ocr_lab analyze
uv run python -m ocr_lab verify
uv run pytest -q
```

`analyze` rebuilds the result table and figures. `verify` checks the complete response matrix, original image hashes, recorded budget, and public-content policy. **Neither command calls an API.**

Optional replay is a separate, explicit action:

```bash
# Prints a dry-run plan; no credentials or network needed.
uv run python -m ocr_lab replay --case 01 --model anthropic/claude-haiku-5.5

# Paid: read OPENROUTER_API_KEY from your process environment, then send one request.
uv run python -m ocr_lab replay --case 01 --model anthropic/claude-haiku-5.5 --execute-paid
```

New responses go to ignored `new-runs/`; the historical evidence is never overwritten. Provider behavior, aliases, prices and latency can change. A replay reproduces the request, not a guaranteed output. [Full protocol](docs/METHODOLOGY.md).

## Handwritten-data collection templates

Blank English templates are provided for [PYG invoices](templates/invoice-pyg.png), [USD invoices](templates/invoice-usd.png), and [optical readings](templates/optical-reading.png). Fill these by hand with fictitious data or consented data and have another person independently transcribe them before expanding the experiment. **These blank forms are not scored test images.**

```bash
uv run python scripts/create_templates.py
```

## Provenance, privacy and limits

The original case 02 did not independently disambiguate `79,003 USD`. It was replaced by a version with a PYG equivalent, and every endpoint was rerun on that version. The [original image and four excluded responses](data/synthetic/audit/case-02-original) are retained. Total measured spend, including those calls: **$0.12700245**.

Earlier private-image pilots motivated endpoint selection. Only [aggregate observations](data/pilot-aggregates.json) are included; their source images, personal data, and extraction bodies are excluded. Those pilots had human-assisted, partly uncertain references and are **not pooled into the synthetic leaderboard**.

No credentials, customer documents, local machine paths, encrypted reasoning blobs, or personal contact details are published. Synthetic fixture values are test data, not verified taxpayer records. Public response artifacts retain extraction text, endpoint/provider labels, timing, token counts and reported cost; they are an allowlisted export rather than full provider envelopes.

See [limitations and next experiments](docs/LIMITATIONS.md), [research background](docs/RESEARCH.md), and [artifact provenance](docs/DATASET.md).

---

Maintained at [justino.dev](https://justino.dev). Independent exploratory work; no vendor endorsement implied.
