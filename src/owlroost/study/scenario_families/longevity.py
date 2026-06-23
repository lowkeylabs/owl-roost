# src/owlroost/study/scenario_families/longevity.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Longevity scenario family.
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
            name="longevity",
            title="Longevity",
            category="risk",
            description=(
                "Explores how retirement outcomes "
                "change under different longevity "
                "and life-expectancy assumptions."
            ),
            related_scenario_families=[
                "market_regime",
                "retirement_timing",
                "spending_level",
                "social_security_claiming",
            ],
        )
    )
