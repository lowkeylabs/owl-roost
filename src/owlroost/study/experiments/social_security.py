# src/owlroost/study/experiments/social_security.py
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

from owlroost.core.utils import normalize_module_path
from owlroost.study.specs import (
    ExperimentSpec,
)


def register_experiments(
    reg,
):
    """
    Register market uncertainty
    experiment templates.
    """

    reg.register_experiment(
        ExperimentSpec(
            name="ss_age_sweep_fixed_rates_coarse",
            title="Fixed Return Models",
            description=(
                "Compare retirement outcomes using deterministic long-term return models."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "solver_options.solver=MOSEK",
                "roost_sweeps.optimization_goal=maxSpnd-0",
            ],
            variable_overrides=[
                "rates_selection.method=conservative,optimistic",
                "roost_sweeps.ss_age_pair=range(64,70,1)-range(64,70,1)",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="ss_age_sweep_bootstrap_all_regimes_coarse",
            title="Fixed Return Models",
            description=(
                "Compare retirement outcomes using deterministic long-term return models."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "solver_options.solver=MOSEK",
                "roost_sweeps.optimization_goal=maxSpnd-0",
                "rates_selection.method=historical_bootstrap",
                "roost_settings.trials_per_run=100",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,modern,lost_decade,stagflation,dotcom,secular_bull",
                "roost_sweeps.ss_age_pair=range(64,70,1)-range(64,70,1)",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="ss_age_pairs_bootstrap_all_regimes",
            title="Fixed Return Models",
            description=(
                "Compare retirement outcomes using deterministic long-term return models."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "solver_options.solver=MOSEK",
                "roost_sweeps.optimization_goal=maxSpnd-0",
                "rates_selection.method=historical_bootstrap",
                "roost_settings.trials_per_run=100",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,modern,lost_decade,stagflation,dotcom,secular_bull",
                "roost_sweeps.ss_age_pair=64-64,65-65,66-66,67-67,68-68,69-69,70-70",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="ss_age_pairs_bootstrap_all_regimes_roth_caps",
            title="Fixed Return Models",
            description=(
                "Compare retirement outcomes using deterministic long-term return models."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "solver_options.solver=MOSEK",
                "roost_sweeps.optimization_goal=maxSpnd-0",
                "rates_selection.method=historical_bootstrap",
                "roost_settings.trials_per_run=100",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,modern,lost_decade,stagflation",
                "roost_sweeps.ss_age_pair=65-65,67-67,68-68,69-69,70-70",
                "solver_options.maxRothConversion=0.0,100.0,200.0,300.0,1000.0",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )
