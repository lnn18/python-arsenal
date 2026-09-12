.PHONY: install dev test lint typecheck check

install:
	uv sync --all-extras

dev:
	uv run uvicorn app.main:app --reload --app-dir src

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy src

check: lint typecheck test
