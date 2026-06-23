# src/owlroost/study/studies/retirement_readiness.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Retirement readiness study.
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
            name="retirement_readiness",
            title="Retirement Readiness",
            description=(
                "Evaluates whether a household "
                "appears prepared for retirement "
                "and explores major retirement "
                "timing, spending, and risk "
                "questions."
            ),
            question_names=[
                "can_i_retire",
                "should_i_retire",
                "when_should_i_retire",
                "how_much_can_i_spend",
            ],
        )
    )
