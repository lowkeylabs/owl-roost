# src/owlroost/study/scenario_families/market_uncertainty.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Market regime scenario family.
"""

from __future__ import annotations

from owlroost.display.specs import DisplayProfile
from owlroost.study.specs import (
    ScenarioFamilySpec,
)


def register_scenario_families(
    reg,
):
    reg.register_scenario_family(
        ScenarioFamilySpec(
            name="market_uncertainty",
            title="Market Uncertainty",
            category="risk",
            description=(
                "Explores how retirement outcomes "
                "change under different return "
                "assumptions, historical periods, "
                "and stochastic return sequences."
            ),
            related_scenario_families=[
                "retirement_timing",
                "spending_level",
                "social_security_claiming",
                "roth_conversion",
                "longevity",
            ],
            experiment_names=[
                "historical_regimes",
                "bootstrap_regimes",
                "garch_dcc_regimes",
                "fixed_return_regimes",
            ],
            profiles={
                "table": DisplayProfile(
                    label="Market\nUncertainty",
                ),
                "pivot": DisplayProfile(
                    label="Market Uncertainty",
                ),
            },
        )
    )
