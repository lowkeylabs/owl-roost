# src/owlroost/study/questions/should_i_retire.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Should I retire?
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
            name="should_i_retire",
            title="Should I Retire?",
            category="retirement",
            description=(
                "Evaluates the tradeoffs between "
                "retiring now and delaying retirement "
                "under a range of market, spending, "
                "and longevity assumptions."
            ),
            scenario_family_names=[
                "retirement_timing",
                "market_regime",
                "spending_level",
                "longevity",
            ],
            related_questions=[
                "can_i_retire",
                "when_should_i_retire",
                "how_much_can_i_spend",
            ],
        )
    )
