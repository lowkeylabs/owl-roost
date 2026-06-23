# src/owlroost/study/scenario_families/spending_level.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Spending level scenario family.
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
            name="spending_level",
            title="Spending Level",
            category="spending",
            description=(
                "Explores sustainable spending "
                "levels and the consequences of "
                "higher or lower retirement spending."
            ),
            related_scenario_families=[
                "market_regime",
                "longevity",
                "retirement_timing",
            ],
        )
    )
