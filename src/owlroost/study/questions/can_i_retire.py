# src/owlroost/study/questions/can_i_retire.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Can I retire?
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
            name="can_i_retire",
            title="Can I Retire?",
            category="retirement",
            description=(
                "Evaluates whether available "
                "household assets appear capable "
                "of supporting retirement spending "
                "under a range of market and "
                "longevity assumptions."
            ),
            scenario_family_names=[
                "retirement_timing",
                "spending_level",
                "market_regime",
                "longevity",
            ],
            related_questions=[
                "should_i_retire",
                "when_should_i_retire",
                "how_much_can_i_spend",
            ],
        )
    )
