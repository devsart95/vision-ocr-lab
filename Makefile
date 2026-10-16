.PHONY: check report audit
check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pyright
	uv run vulture src --min-confidence 80
	uv run pytest -q
	uv run lint-imports
	uv run python -m ocr_lab verify
report:
	uv run python -m ocr_lab analyze
audit:
	uv run pip-audit
