# src/owlroost/study/decisions/social_security.py
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

from owlroost.display.specs import DisplayProfile
from owlroost.study.specs import (
    DecisionSpec,
)


def register_decisions(
    reg,
):
    reg.register_decision(
        DecisionSpec(
            name="social_security",
            title="Social Security Timing",
            category="retirement",
            description=("When should Social Security benefits be claimed?"),
            profiles={
                "table": DisplayProfile(
                    label="Decision\nSS Timing",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Decision - Social Security timing",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
            },
        )
    )
