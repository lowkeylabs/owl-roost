# src/owlroost/guide/engine.py
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

from owlroost.display.operations.resolution import (
    resolve_field_value,
)

OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
}


def applicable(
    row,
    suggestion,
):
    """
    Evaluate one suggestion.
    """

    for req in suggestion.requirements:
        actual = resolve_field_value(
            row,
            req.variable,
        )

        fn = OPS[req.operator]

        if not fn(
            actual,
            req.value,
        ):
            return False

    return True


def applicable_suggestions(
    row,
    registry,
):
    """
    Return applicable suggestions.
    """

    return [
        s
        for s in registry.suggestions()
        if applicable(
            row,
            s,
        )
    ]
