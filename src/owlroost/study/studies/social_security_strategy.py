# src/owlroost/study/studies/social_security_strategy.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Social Security strategy study.
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
            name="social_security_strategy",
            title="Social Security Strategy",
            description=(
                "Explores Social Security claiming "
                "alternatives and evaluates how "
                "claiming decisions affect spending, "
                "portfolio sustainability, lifetime "
                "income, and retirement outcomes."
            ),
            question_names=[
                "can_i_claim_ss_this_year",
                "when_should_i_claim_ss",
            ],
        )
    )
