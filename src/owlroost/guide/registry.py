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
GuideEvaluation objects.

Architectural Role
-----------------
GuideRegistry also serves as the
semantic object registry for guide
definitions.

Semantic object lookups include:

    guide.workspace.initialize.command

    guide.workspace.initialize.description

    guide.workspace.initialize.priority

without requiring those properties to
appear in the catalog.
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
    # Enumeration
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

    # =====================================================
    # Semantic Object Lookup
    # =====================================================

    def get_object(
        self,
        name,
    ):
        """
        Return one registered GuideSpec.

        This method establishes the
        generic semantic-object lookup
        interface that other registries
        will eventually implement.
        """

        return self._guides.get(
            name,
        )

    #
    # Backwards compatibility.
    #

    def get(
        self,
        name,
    ):
        """
        Return one registered guide.
        """

        return self.get_object(
            name,
        )

    def has_object(
        self,
        name,
    ):
        """
        Return whether a guide exists.
        """

        return name in self._guides

    def resolve_object_property(
        self,
        object_name,
        property_name,
    ):
        """
        Resolve one property of a
        registered GuideSpec.

        Examples
        --------

            workspace.initialize

                description

            welcome

                command
        """

        obj = self.get_object(
            object_name,
        )

        if obj is None:
            return None

        return getattr(
            obj,
            property_name,
            None,
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
