# src/owlroost/study/studies/machine_tuning/definition.py
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
            name="machine_tuning",
            title="Machine tuning",
            description=(
                "Explores different threading options to "
                "optimize ROOST multi-tasking for this machine."
            ),
            experiment_names=[
                "tune_workers_sweep",
                "tune_workers_highs_sweep",
                "tune_workers_mosek_sweep",
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
            ],
            resource_dir=RESOURCE_DIR,
            defined_in=normalize_module_path(__file__),
        )
    )
