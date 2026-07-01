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

Guide providers register GuideSpec
objects.

The registry evaluates those guides
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
    Registered workflow guides.
    """

    def __init__(
        self,
    ):
        self._guides = {}

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        guide,
    ):
        """
        Register one workflow guide.
        """

        self._guides[guide.name] = guide

    # =====================================================
    # Lookup
    # =====================================================

    def all(
        self,
    ):
        """
        Return all registered guides in
        presentation order.
        """

        return sorted(
            self._guides.values(),
            key=lambda guide: (
                guide.priority,
                guide.title.lower(),
            ),
        )

    def get(
        self,
        name,
    ):
        """
        Return one registered guide.
        """

        return self._guides.get(
            name,
        )

    # =====================================================
    # Evaluation
    # =====================================================

    def evaluate(
        self,
        *,
        row,
    ):
        """
        Evaluate all registered guides
        for one planning row.
        """

        return evaluate(
            row=row,
            registry=self,
        )
