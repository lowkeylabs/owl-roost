# src/owlroost/study/studies/legacy_planning.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Legacy planning study.
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
            name="legacy_planning",
            title="Legacy Planning",
            description=(
                "Explores how spending, gifting, "
                "tax strategies, and retirement "
                "decisions influence future estate "
                "values and legacy objectives."
            ),
            question_names=[
                "how_much_can_i_spend",
                "should_i_do_roth_conversions",
            ],
        )
    )
