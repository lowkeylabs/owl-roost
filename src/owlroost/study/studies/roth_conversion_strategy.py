# src/owlroost/study/studies/roth_conversion_strategy.py
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
    StudySpec,
)


def register_studies(
    reg,
):
    reg.register_study(
        StudySpec(
            name="roth_conversion_strategy",
            title="Roth Conversion Strategy",
            description=(
                "Explores how Roth conversion "
                "decisions affect taxes, spending, "
                "portfolio sustainability, and "
                "after-tax wealth."
            ),
            question_names=[
                "should_i_do_roth_conversions",
                "how_much_should_i_convert",
            ],
        )
    )
