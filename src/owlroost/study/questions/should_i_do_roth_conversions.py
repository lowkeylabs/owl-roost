# src/owlroost/study/questions/should_i_do_roth_conversions.py
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
            name="should_i_do_roth_conversions",
            title="Should I Do Roth Conversions?",
            category="tax",
            description=(
                "Evaluates whether Roth conversions "
                "may improve future retirement outcomes "
                "through reduced taxes, improved "
                "portfolio flexibility, or increased "
                "after-tax wealth."
            ),
            scenario_family_names=[
                "roth_conversion",
                "market_regime",
            ],
            required_levers=[
                "has_pretax_savings",
            ],
            related_questions=[
                "how_much_should_i_convert",
            ],
        )
    )
