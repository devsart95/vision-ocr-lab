"""Scoring policy: numeric meaning, exact identifiers, and explicit abstention."""

import json
import re
import unicodedata
from decimal import Decimal, InvalidOperation
from typing import TypeAlias, cast

JSON: TypeAlias = bool | int | float | str | list["JSON"] | dict[str, "JSON"] | None
MISSING = "__MISSING__"
NUMERIC = frozenset(
    {
        "tipo_cambio",
        "cantidad",
        "precio_unitario",
        "iva_porcentaje",
        "importe",
        "total",
        "latitud",
        "longitud",
        "potencia_dbm",
    }
)
TEXT = frozenset({"emisor", "receptor", "condicion", "descripcion"})
IDENTIFIERS = frozenset({"ruc_emisor", "ruc_receptor", "timbrado", "numero"})


def normalize_text(value: JSON) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", str(value)).casefold() if c.isalnum())


def compare_field(path: str, actual: JSON, expected: JSON) -> bool:
    if expected is None:
        return actual is None
    if actual is None or actual == MISSING:
        return False
    suffix = path.split(".")[-1]
    if suffix in NUMERIC:
        try:
            left, right = Decimal(str(actual)), Decimal(str(expected))
            return left.is_finite() and right.is_finite() and left == right
        except InvalidOperation:
            return False
    if suffix in TEXT:
        return normalize_text(actual) == normalize_text(expected)
    return actual == expected


def parse_response(content: str) -> tuple[dict[str, JSON], bool]:
    direct = True
    try:
        value = cast(JSON, json.loads(content))
    except json.JSONDecodeError:
        direct = False
        stripped = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
        try:
            value = cast(JSON, json.loads(stripped))
        except json.JSONDecodeError:
            return {}, False
    return (value, direct) if isinstance(value, dict) else ({}, False)


def flatten(value: JSON, prefix: str = "") -> dict[str, JSON]:
    if isinstance(value, dict):
        output: dict[str, JSON] = {}
        for key, child in value.items():
            output.update(flatten(child, (prefix + "." + key).strip(".")))
        return output
    if isinstance(value, list):
        output = {}
        for index, child in enumerate(value):
            output.update(flatten(child, f"{prefix}.{index}"))
        return output
    return {prefix: value}


def evaluate(expected: dict[str, JSON], content: str) -> dict[str, JSON]:
    parsed, direct = parse_response(content)
    reference, actual = flatten(expected), flatten(parsed)
    errors: list[JSON] = [
        {"field": key, "expected": val, "actual": actual.get(key, MISSING)}
        for key, val in reference.items()
        if not compare_field(key, actual.get(key, MISSING), val)
    ]
    extras: list[JSON] = [key for key in sorted(set(actual) - set(reference))]
    formats: list[JSON] = []
    for key, value in actual.items():
        suffix = key.split(".")[-1]
        if value is None:
            continue
        if suffix in NUMERIC - {"iva_porcentaje"} and (
            not isinstance(value, str) or not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", str(value))
        ):
            formats.append(key)
        if suffix in IDENTIFIERS and not isinstance(value, str):
            formats.append(key)
    hallucinations = sum(
        1
        for err in errors
        if isinstance(err, dict) and err["expected"] is None and err["actual"] != MISSING
    )
    return {
        "correct_fields": len(reference) - len(errors),
        "total_fields": len(reference),
        "exact": not errors and not extras,
        "ready": not errors and not extras and not formats and direct,
        "direct_json": direct,
        "errors": errors,
        "extra_fields": extras,
        "format_errors": formats,
        "hallucinated_missing_fields": hallucinations,
        "parsed": parsed,
    }
