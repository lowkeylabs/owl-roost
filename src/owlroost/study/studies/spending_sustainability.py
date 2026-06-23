# src/owlroost/study/studies/spending_sustainability.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Spending sustainability study.
"""

from __future__ import annotations

from owlroost.study.specs import (
    StudySpec,
)


def register_studies(
    reg,
):
    reg.register_study(
        StudySpec(
            name="spending_sustainability",
            title="Spending Sustainability",
            description=(
                "Explores sustainable spending "
                "levels, spending flexibility, "
                "and the long-term consequences "
                "of spending decisions under a "
                "range of retirement scenarios."
            ),
            question_names=[
                "how_much_can_i_spend",
                "can_i_retire",
                "should_i_retire",
            ],
        )
    )
