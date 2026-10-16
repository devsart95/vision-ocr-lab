import pytest

from ocr_lab.domain import JSON, MISSING, compare_field, parse_response


@pytest.mark.parametrize(
    ("path", "actual", "expected", "matches"),
    [
        ("factura.total", "79.003", "79.003", True),
        ("factura.total", "79003", "79.003", False),
        ("factura.tipo_cambio", "6.454", "6454", False),
        ("medicion.latitud", "+26.048390", "26.04839", True),
        ("medicion.potencia_dbm", "0.50", "-0.50", False),
        ("factura.ruc_receptor", "8007654 3-2", "80076543-2", False),
        ("factura.condicion", "CREDITO", "Crédito", True),
        ("factura.total", None, None, True),
        ("factura.total", "0", None, False),
        ("factura.total", MISSING, None, False),
        ("factura.total", "NaN", "79.003", False),
    ],
)
def test_field_comparison(path: str, actual: JSON, expected: JSON, matches: bool) -> None:
    assert compare_field(path, actual, expected) is matches


def test_markdown_is_readable_but_not_direct_json() -> None:
    data, direct = parse_response('```json\n{"total":null}\n```')
    assert data == {"total": None}
    assert direct is False


def test_array_is_not_an_extraction_object() -> None:
    data, direct = parse_response("[1, 2]")
    assert data == {}
    assert direct is False
