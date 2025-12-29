.PHONY: help sync pre-commit pytest test

help:
	cat Makefile

sync:
	uv sync --extra dev

pre-commit:
	uv run pre-commit run --all-files

pytest:
	uv run pytest

test: sync pre-commit pytest
