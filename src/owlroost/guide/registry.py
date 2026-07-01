# src/owlroost/guide/registry.py
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

from owlroost.guide.engine import (
    applicable_suggestions,
)
from owlroost.guide.render import (
    render_context,
)


class GuideRegistry:
    """
    Registered guide suggestions.
    """

    def __init__(self):
        self._suggestions = {}

    def register(
        self,
        suggestion,
    ):
        self._suggestions[suggestion.name] = suggestion

    def suggestions(
        self,
    ):
        return list(
            sorted(
                self._suggestions.values(),
                key=lambda s: (
                    s.priority,
                    s.title.lower(),
                ),
            )
        )

    def get(
        self,
        name,
    ):
        return self._suggestions.get(
            name,
        )

    def applicable(
        self,
        row,
    ):
        return applicable_suggestions(
            row,
            self,
        )

    def render(
        self,
        *,
        mode,
        row,
    ):
        if mode == "context":
            return render_context(
                self.applicable(row),
            )

        raise ValueError(f"Unknown guide mode: {mode}")
