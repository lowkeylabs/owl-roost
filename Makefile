.PHONY: help

help:
	cat Makefile


.PHONY: dev
dev:
	uv sync --extra dev

.PHONY: pre-commit
pre-commit:
	uv sync --extra dev
	uv run pre-commit run --all-files
	uv run pytest
