# src/owlroost/study/scenario_families/social_security_claiming.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Social Security claiming scenario family.
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
            name="social_security_claiming",
            title="Social Security Claiming",
            category="social_security",
            description=(
                "Explores how retirement outcomes change as Social Security claiming ages vary."
            ),
            related_scenario_families=[
                "market_regime",
                "longevity",
            ],
        )
    )
