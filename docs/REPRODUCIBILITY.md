# Reproducibility levels

| Level | Available here | Guarantee |
|---|---|---|
| Rescore recorded responses | Yes, offline | Same stored artifacts and scoring policy |
| Regenerate summary and figures | Yes, offline | Same measurements; image/SVG bytes may vary across rendering environments |
| Reconstruct original PNG pixels from generation source | Not guaranteed | Fonts and historical unseeded noise affect pixels; archived PNGs plus hashes are authoritative |
| Repeat the API request | Yes, explicit paid single-call command | Same prompt and input; outputs, endpoint routing and prices may differ |
| Independently reproduce private pilots | No | Private inputs and extractions are intentionally withheld |

## Commands

```bash
uv sync --locked
make check
make report
```

The project lockfile pins the installed Python dependencies. Matplotlib generates PNG and SVG figures with an offline backend. Blank English data-collection templates can be regenerated with `uv run python scripts/create_templates.py`; they are not historical benchmark stimuli.

Run `uv run python -m ocr_lab replay --case 01 --model google/gemini-3.8-flash` to inspect a no-network dry run. Add `--execute-paid` only when you intend to spend your own API credit and have set `OPENROUTER_API_KEY` in the process environment. The runner sends one request, uses an explicit timeout, performs no automatic retry, and saves a new ignored artifact. No API key file is required.

The recorded endpoints and settings are in the dataset run manifest. The published response export is an allowlist: assistant extraction, model/provider labels, duration, usage and reported cost. It is intentionally not the complete provider response.

## Scoring compatibility

The package reproduces the historical primary counts while adding boundary validation and rejection of non-finite numeric values. It separately identifies readable fenced JSON and direct JSON. All historical scored responses used direct JSON, so that distinction does not alter the published primary rankings.

The numeric policy uses Decimal, never tolerance-based matching for amounts or coordinates. The current schema checks are limited to the documented numeric/identifier representation checks, not full structural JSON Schema enforcement. Future changes to scoring require a versioned experiment result rather than silently replacing these measurements.
