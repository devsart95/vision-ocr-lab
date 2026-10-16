# Research background and what this lab measures

This is vision-based structured extraction. It combines text recognition, layout interpretation and schema mapping. The references below explain those tasks; their reported benchmark results are not imported into this lab's rankings.

## Recognition, layout and information extraction are different layers

A useful conceptual pipeline is:

```text
image quality -> text recognition -> layout/field association -> typed normalization -> validation
```

[SROIE](https://arxiv.org/abs/2103.10213) distinguishes receipt text localization, recognition and key-information extraction. That separation explains why a readable digit sequence can still be assigned to the wrong field. This lab checks the final structured fields; it does not isolate recognition from the other stages.

[DocVQA](https://arxiv.org/abs/2007.00398) studies answering questions from document images. It motivates evaluating document understanding beyond plain text transcription. Its dataset and evaluation setting differ from our synthetic invoices, so its scores cannot be compared with the numbers here.

[LayoutLMv3](https://arxiv.org/abs/2204.08387) combines text/image pretraining with alignment information. Layout can distinguish a unit price from a tax amount even when both look similar. Our line-item fixtures exercise association, but contain much simpler layouts than broad document benchmarks.

## OCR-based and OCR-free approaches

[TrOCR](https://arxiv.org/abs/2109.10282) uses image and text transformers for recognition, with experiments on printed, handwritten and scene text. Real handwriting is a separate evaluation domain: a Comic Sans fixture does not recreate individual pen strokes, writer variation or ambiguous corrections.

[Donut](https://arxiv.org/abs/2111.15664) studies OCR-free document understanding and synthetic document generation. Synthetic data enables known answers and controlled rendering, but does not eliminate the domain gap between a rendering and a real photograph.

The tested hosted endpoints are treated as black boxes. We do not assert that they implement any of these particular research architectures. TrOCR, LayoutLMv3, Donut and Tesseract were **not run as baselines** in this experiment.

## Image formation and degradation

[Tesseract's primary quality guide](https://github.com/tesseract-ocr/tessdoc/blob/main/ImproveQuality.md) documents practical effects of rotation, noise, borders and preprocessing. These motivate our rotated/blurred fixtures. Their effect on Tesseract does not establish an identical effect size for a multimodal language model.

A controlled degradation study would vary one factor over several known levels while keeping text and layout fixed. This lab changes several factors together in some cases. It can expose a failure, but cannot estimate a causal blur or rotation tolerance curve.

## Metrics and monetary risk

Character error rate is based on edit operations relative to a reference transcript. Word error rate changes the token unit. End-to-end field exactness instead asks whether each required extracted value is correct. They answer different questions. This lab does not publish CER/WER because it does not contain a complete adjudicated page transcript for that purpose.

A monetary schema makes numeric interpretation essential. `79.003` and `79003` have similar strings but different values. We compare finite Decimal values rather than edit similarity for numeric fields. A valid JSON object only proves syntax; it does not prove that an amount or tax ID is correct.

[ExtractBench](https://arxiv.org/abs/2602.12247) evaluates complex PDF-to-JSON extraction and underscores the importance of schema-level reliability. Its much broader setting is useful context, not confirmation of our endpoint ordering.

## What to measure next

Collect consented, independently transcribed photographs across suppliers, layouts, writers and capture conditions. Hold out templates and writers; repeat requests; pin provider routes and settings where possible. Report critical-field failures, abstention quality and correction time alongside cost. Compare a conventional OCR pipeline and document-specific parsers under the same task contract before making a deployment decision.
