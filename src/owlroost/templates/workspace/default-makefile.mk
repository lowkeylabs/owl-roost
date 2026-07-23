# Shared ROOST Makefile
# Default location for this file: ./owlroost/templates/workspace/default-makefile.mk
# Location is assigned in ./owlroost/core/settings.py

.PHONY: help validate cases results docs all clean realclean

help:
	@echo ""
	@echo "ROOST Workspace Targets"
	@echo ""
	@echo "  make validate"
	@echo "  make cases"
	@echo "  make results"
	@echo "  make docs"
	@echo "  make all"
	@echo ""
	@echo "  make clean - delete results_dir"
	@echo "  make realclean"
	@echo ""

validate:
	@echo "Validating workspace..."
	@roost workspace . --validate

cases:
	@if [ -f 01_build_cases.qmd ]; then
	quarto render 01_build_cases.qmd;
	else
	echo "No 01_build_cases.qmd found.";
	fi

results2:
	@if [ -f 02_build_results.qmd ]; then
	quarto render 02_build_results.qmd;
	else
	echo "No 02_build_results.qmd found.";
	fi

build:
	roost build --all

run:
	roost run

results: run
	roost workspace --sync-results-catalog --force

docs:
	@quarto render

all: validate cases results docs

clean:
	@echo "Removing generated results..."
	@rm -rf results
	@rm -fr docs

realclean: clean
	@echo "Removing generated cases..."
	@rm -rf cases
