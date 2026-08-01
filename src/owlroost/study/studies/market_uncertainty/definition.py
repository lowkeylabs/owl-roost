# src/owlroost/study/studies/market_uncertainty/definition.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from pathlib import Path

from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.study.specs import (
    StudySpec,
)

RESOURCE_DIR = Path(__file__).parent


def register_studies(
    reg,
):
    reg.register_study(
        StudySpec(
            name="market_uncertainty",
            title="Market Uncertainty",
            description=(
                "Explores how retirement outcomes "
                "change under different market "
                "return assumptions, historical "
                "periods, and stochastic return "
                "sequences."
            ),
            experiment_names=[
                "bootstrap_quick",
                "fixed_return_models",
                "historical_models",
            ],
            # Constructed using load_run_rows()
            run_row_views=[
                {
                    "level": "run",
                    "view": "table_of_runs",
                    "mode": "table",
                    "save_file": "25_1_table_of_runs",
                },
                {
                    "level": "run",
                    "view": "table_of_rate_models",
                    "mode": "table",
                    "save_file": "35_1_table_of_rate_models",
                },
                {
                    "level": "run",
                    "view": "social_security1",
                    "mode": "table",
                    "save_file": "55_10_median_values",
                },
                {
                    "level": "run",
                    "view": "social_security2",
                    "mode": "table",
                    "save_file": "55_20_p10_values",
                },
                {
                    "level": "run",
                    "view": "social_security3",
                    "mode": "table",
                    "save_file": "55_30_p90_values",
                },
            ],
            resource_dir=RESOURCE_DIR,
            defined_in=normalize_module_path(__file__),
        )
    )
