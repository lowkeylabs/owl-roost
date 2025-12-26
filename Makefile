.PHONY: help

help:
	cat Makefile


.PHONY: dev
dev:
	uv sync --extra dev
