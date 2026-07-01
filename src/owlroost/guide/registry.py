# src/owlroost/guide/registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide registry.

Notes
-----
Owns registration and evaluation of
workflow guidance.

Guide providers register SuggestionSpec
objects.

The registry evaluates those suggestions
against a planning context and returns
a semantic EvaluationResult.

Rendering is owned by the display
subsystem.
"""

from __future__ import annotations

from owlroost.guide.engine import (
    evaluate,
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
        return sorted(
            self._suggestions.values(),
            key=lambda s: (
                s.priority,
                s.title.lower(),
            ),
        )

    def get(
        self,
        name,
    ):
        return self._suggestions.get(
            name,
        )

    def evaluate(
        self,
        *,
        row,
    ):
        """
        Evaluate all registered guide
        suggestions for one planning row.
        """

        return evaluate(
            row=row,
            registry=self,
        )
