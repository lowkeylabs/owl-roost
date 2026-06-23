# src/owlroost/study/questions/how_much_can_i_spend.py
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
            name="how_much_can_i_spend",
            title="How Much Can I Spend?",
            category="spending",
            description=(
                "Explores sustainable spending "
                "levels under a range of market, "
                "longevity, and retirement timing "
                "assumptions."
            ),
            scenario_family_names=[
                "spending_level",
                "market_regime",
                "longevity",
                "retirement_timing",
            ],
            related_questions=[
                "can_i_retire",
                "should_i_retire",
            ],
        )
    )
