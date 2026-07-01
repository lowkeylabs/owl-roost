# src/owlroost/guide/providers/cases.py
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

from owlroost.guide.specs import (
    Requirement,
    SuggestionSpec,
)


def register(
    reg,
):
    reg.register(
        SuggestionSpec(
            name="cases.review",
            title="Review Cases",
            description=("Review available planning cases."),
            command="roost cases",
            priority=30,
            requirements=[
                Requirement(
                    "context.valid_case_count",
                    ">",
                    0,
                ),
            ],
        )
    )
