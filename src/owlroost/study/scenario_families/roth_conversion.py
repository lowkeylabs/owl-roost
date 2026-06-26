# src/owlroost/study/scenario_families/roth_conversion.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Roth conversion scenario family.
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
            name="roth_conversion",
            title="Roth Conversion",
            category="tax",
            description=(
                "Explores the consequences of "
                "different Roth conversion amounts "
                "and conversion strategies."
            ),
            related_scenario_families=[
                "market_regime",
            ],
        )
    )
