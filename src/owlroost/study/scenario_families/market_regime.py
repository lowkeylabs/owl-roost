# src/owlroost/study/scenario_families/market_regime.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Market regime scenario family.
"""

from __future__ import annotations

from owlroost.study.specs import (
    ScenarioFamilySpec,
)


def register_scenario_families(
    reg,
):
    reg.register_scenario_family(
        ScenarioFamilySpec(
            name="market_regime",
            title="Market Regime",
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
        )
    )
