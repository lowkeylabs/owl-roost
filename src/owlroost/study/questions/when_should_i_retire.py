# src/owlroost/study/questions/when_should_i_retire.py
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
            name="when_should_i_retire",
            title="When Should I Retire?",
            category="retirement",
            description=(
                "Explores how retirement outcomes "
                "change as retirement timing varies "
                "across future years."
            ),
            scenario_family_names=[
                "retirement_timing",
                "market_regime",
                "longevity",
            ],
            related_questions=[
                "can_i_retire",
                "should_i_retire",
            ],
        )
    )
