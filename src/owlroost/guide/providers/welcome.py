# src/owlroost/guide/providers/welcome.py
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
    SuggestionSpec,
)


def register(
    reg,
):
    reg.register(
        SuggestionSpec(
            name="welcome",
            title="Getting Started",
            description=("Display the current planning context."),
            command="roost .",
            priority=10,
        )
    )
