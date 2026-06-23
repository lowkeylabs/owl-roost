# src/owlroost/study/scenario_families/retirement_timing.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Retirement timing scenario family.
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
            name="retirement_timing",
            title="Retirement Timing",
            category="retirement",
            description=(
                "Explores how retirement outcomes "
                "change when retirement occurs at "
                "different future dates."
            ),
            related_scenario_families=[
                "spending_level",
                "market_regime",
                "longevity",
            ],
        )
    )
