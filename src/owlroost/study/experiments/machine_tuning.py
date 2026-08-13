# src/owlroost/study/experiments/machine_tuning.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Market uncertainty experiment templates.

Notes
-----
Registers reusable experimental
designs for exploring uncertainty
arising from investment return
assumptions.

Each experiment template defines an
unrealized experiment.

When materialized for a household,
a experiment template becomes a Session
containing one or more Runs.

Runs are the primary analytical
objects compared by ROOST.
"""

from __future__ import annotations

from owlroost.core.utils import normalize_module_path
from owlroost.study.specs import (
    ExperimentSpec,
)

SHARED_OVERRIDES = [
    "roost_sweeps.optimization_goal=maxSpnd-0",
    "rates_selection.method=bootstrap_sor",
    "roost_sweeps.named_window=full",
    "roost_settings.trials_per_run=200",
]


def register_experiments(
    reg,
):
    """
    Register market uncertainty
    experiment templates.
    """

    reg.register_experiment(
        ExperimentSpec(
            name="tune_workers_mosek_sweep",
            title="Explore MOSEK workers per run",
            description=(
                """

                """
            ),
            required_levers=[],
            fixed_overrides=[
                *SHARED_OVERRIDES,
                "solver_options.solver=MOSEK",
            ],
            variable_overrides=[
                "roost_settings.workers_per_run=4,5,6,7,8,9,10,11,12",
                #                "roost_settings.workers_per_run=3,4,5,6,7,8,9,10",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="tune_workers_highs_sweep",
            title="Explore HiGHS workers per run",
            description=(
                """

                """
            ),
            required_levers=[],
            fixed_overrides=[
                *SHARED_OVERRIDES,
                "solver_options.solver=HiGHS",
            ],
            variable_overrides=[
                "roost_settings.workers_per_run=20,21,22,23,24,25,26,27,28",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="tune_workers_sweep",
            title="Explore HiGHS workers per run",
            description=(
                """

                """
            ),
            required_levers=[],
            fixed_overrides=[
                *SHARED_OVERRIDES,
            ],
            variable_overrides=[
                "solver_options.solver=MOSEK,HiGHS",
                "roost_settings.workers_per_run=1,2,4,6,8,10,12,14,16,18,20,22,24,26",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )
