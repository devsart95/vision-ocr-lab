"""Offline scoring and aggregation. Monetary calculations use Decimal."""

import json
import statistics
from decimal import Decimal
from pathlib import Path
from typing import cast

from ocr_lab.domain import JSON, evaluate
from ocr_lab.records import Case, Response, read_cases, read_responses

NAMES = {
    "anthropic/claude-haiku-5.5": "Haiku 5.5",
    "google/gemini-3.8-flash": "Gemini 3.8 Flash",
    "openai/gpt-6-luna": "GPT-6 Luna",
    "openai/gpt-6-sol": "GPT-6 Sol",
}


def score_records(cases: list[Case], responses: list[Response]) -> list[dict[str, JSON]]:
    indexed = {case.id: case for case in cases}
    return [
        dict(
            evaluate(cast(dict[str, JSON], indexed[row.case_id].expected), row.content),
            case_id=row.case_id,
            model=row.model,
            seconds=row.seconds,
            cost_usd=str(row.cost_usd),
            prompt_tokens=row.prompt_tokens,
            completion_tokens=row.completion_tokens,
            provider=row.provider,
            finish_reason=row.finish_reason,
        )
        for row in responses
    ]


def summarize(rows: list[dict[str, JSON]]) -> dict[str, JSON]:
    result: dict[str, JSON] = {}
    for model in NAMES:
        subset = [row for row in rows if row["model"] == model]
        if not subset:
            continue
        cost = sum((Decimal(str(row["cost_usd"])) for row in subset), Decimal(0))
        times = [float(str(row["seconds"])) for row in subset]
        result[model] = {
            "name": NAMES[model],
            "calls": len(subset),
            "exact_images": sum(bool(row["exact"]) for row in subset),
            "ready_images": sum(bool(row["ready"]) for row in subset),
            "correct_fields": sum(int(str(row["correct_fields"])) for row in subset),
            "total_fields": sum(int(str(row["total_fields"])) for row in subset),
            "mean_seconds": round(statistics.mean(times), 3),
            "median_seconds": round(statistics.median(times), 3),
            "cost_usd": str(cost),
            "projected_1000_usd": str(cost * 1000 / len(subset)),
        }
    return result


def analyze(root: Path) -> dict[str, JSON]:
    responses = read_responses(root / "data/synthetic/responses")
    rows = score_records(read_cases(root), responses)
    audit_dir = root / "data/synthetic/audit/case-02-original"
    excluded = read_responses(audit_dir)
    cost = sum((r.cost_usd for r in responses + excluded), Decimal(0))
    report: dict[str, JSON] = {
        "models": summarize(rows),
        "results": cast(list[JSON], rows),
        "scored_calls": len(responses),
        "excluded_calls": len(excluded),
        "all_actual_cost_usd": str(cost),
    }
    target = root / "results"
    target.mkdir(exist_ok=True)
    (target / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report
