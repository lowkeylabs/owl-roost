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
