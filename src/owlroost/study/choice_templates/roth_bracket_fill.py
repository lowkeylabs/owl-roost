# src/owlroost/study/choice_templates/roth_bracket_fill.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Roth conversion bracket-fill methodology.
"""

from __future__ import annotations

from owlroost.display.specs import (
    DisplayProfile,
)
from owlroost.study.specs import (
    ChoiceTemplateSpec,
)


def register_choice_templates(
    reg,
):
    reg.register_choice_template(
        ChoiceTemplateSpec(
            name="roth_bracket_fill",
            decision_name="roth_conversion",
            title="Roth Bracket Fill",
            description=(
                "Evaluate Roth conversion "
                "strategies that fill a target "
                "tax bracket while minimizing "
                "unnecessary tax exposure."
            ),
            required_levers=[
                "has_pretax_savings",
            ],
            overrides=[
                ("roost_sweeps.roth_conversion_amount=range(0,200000,10000)"),
            ],
            tags=[
                "retirement",
                "roth",
                "tax",
                "conversion",
            ],
            profiles={
                "table": DisplayProfile(
                    label="Template\nBracket Fill",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label=("Choice Template - Roth Bracket Fill"),
                    width="auto",
                ),
            },
        )
    )
