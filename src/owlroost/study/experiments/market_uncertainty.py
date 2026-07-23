# src/owlroost/study/experiments/market_uncertainty.py
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


def register_experiments(
    reg,
):
    """
    Register market uncertainty
    experiment templates.
    """

    reg.register_experiment(
        ExperimentSpec(
            name="bootstrap_regimes",
            title="Bootstrap Sequence of Returns",
            description=(
                "Evaluate retirement outcomes using "
                "bootstrap sequence-of-returns sampling "
                "across multiple historical market "
                "regimes."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "rates_selection.method=bootstrap_sor",
                "roost_settings.trials_per_run=100",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,dotcom,stagflation",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="historical_average_regimes",
            title="Historical Average Returns",
            description=(
                "Evaluate retirement outcomes using "
                "historical average returns computed "
                "over several historical market regimes."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "rates_selection.method=historical_average",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,dotcom,stagflation",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="fixed_return_models",
            title="Fixed Return Models",
            description=(
                "Compare retirement outcomes using deterministic long-term return models."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[],
            variable_overrides=[
                "rates_selection.method=conservative,optimistic,trailing_30",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )
