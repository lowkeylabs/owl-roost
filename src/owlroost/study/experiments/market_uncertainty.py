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
                "bootstrap sampling "
                "across a historical market"
                "regimes."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "rates_selection.method=historical_bootstrap",
                "roost_settings.trials_per_run=100",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,modern,lost_decade,stagflation,dotcom,secular_bull",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="garch_dcc_regimes",
            title="DCC-GARCH model with historical data",
            description=(
                "DCC-GARCH(1,1) model (Engle 2002) fitted "
                "by two-step MLE on historical data. Captures"
                "time-varying volatility (GARCH) and time-varying"
                "cross-asset correlations (DCC). Produces realistic"
                "volatility clustering and correlation spikes"
                "during market stres."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "rates_selection.method=garch_dcc",
                "roost_settings.trials_per_run=100",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,modern,lost_decade,stagflation,dotcom,secular_bull",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )

    reg.register_experiment(
        ExperimentSpec(
            name="fixed_return_regimes",
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

    reg.register_experiment(
        ExperimentSpec(
            name="historical_regimes",
            title="Historical Average Returns",
            description=(
                "Evaluate retirement outcomes usingreturns drawn from a historical market regime."
            ),
            required_levers=[
                "workspace.levers.is_initialized",
            ],
            fixed_overrides=[
                "rates_selection.method=historical",
            ],
            variable_overrides=[
                "roost_sweeps.named_window=full,modern,lost_decade,stagflation,dotcom,secular_bull",
            ],
            defined_in=normalize_module_path(__file__),
        )
    )
