# src/owlroost/study/questions/how_much_should_i_convert.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from owlroost.study.specs import (
    QuestionSpec,
)


def register_questions(
    reg,
):
    reg.register_question(
        QuestionSpec(
            name="how_much_should_i_convert",
            title="How Much Should I Convert?",
            category="tax",
            description=(
                "Explores the consequences of "
                "different Roth conversion amounts "
                "on taxes, spending, and long-term "
                "retirement outcomes."
            ),
            scenario_family_names=[
                "roth_conversion",
                "market_regime",
            ],
            required_levers=[
                "has_pretax_savings",
            ],
            related_questions=[
                "should_i_do_roth_conversions",
            ],
        )
    )
