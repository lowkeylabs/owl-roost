# src/owlroost/study/questions/when_should_i_claim_social_security.py
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
            name="when_should_i_claim_social_security",
            title="When Should I Claim Social Security?",
            category="social_security",
            description=(
                "Explores how retirement outcomes change as Social Security claiming ages vary."
            ),
            scenario_family_names=[
                "social_security_claiming",
                "market_regime",
                "longevity",
            ],
            required_levers=[
                "has_ss_pia",
            ],
            related_questions=[
                "should_i_claim_social_security",
            ],
        )
    )
