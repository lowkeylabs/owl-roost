# src/owlroost/study/decisions/roth_conversions.py
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
            name="roth_conversion",
            title="Roth Conversion Strategy",
            category="retirement",
            description=("How should tax-deferred assets be converted into tax-free assets?"),
            profiles={
                "table": DisplayProfile(
                    label="Decision\nRoth",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Decision - Roth conversions",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
            },
        )
    )
