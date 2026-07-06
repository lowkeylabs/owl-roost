# src/owlroost/activity/registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide registry.

Notes
-----
Owns registration and evaluation of
planning activities.

Activity providers register
ActivitySpec objects.

The registry evaluates those
activities against a planning context
and returns ActivityEvaluation
objects.

Architectural Role
-----------------
GuideRegistry serves as the semantic
object registry for planning activity
definitions.

Semantic object lookups include:

    workspace.initialize.description

    annual_review.frequency

    annual_review.display_order

without requiring those properties to
appear in the catalog.
"""

from __future__ import annotations

from .engine import (
    evaluate,
)
from .specs import (
    ActivitySpec,
)


class ActivityRegistry:
    """
    Registered planning activities.
    """

    def __init__(
        self,
    ):
        self._activities: dict[
            str,
            ActivitySpec,
        ] = {}

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        activity: ActivitySpec,
    ):
        """
        Register one planning activity.
        """

        self._activities[activity.name] = activity

    # =====================================================
    # Enumeration
    # =====================================================

    def all(
        self,
    ):
        """
        Return all registered
        activities in presentation
        order.
        """

        return sorted(
            self._activities.values(),
            key=lambda activity: (
                activity.display_order,
                activity.title.lower(),
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
        Return one registered
        ActivitySpec.

        This method establishes the
        generic semantic-object lookup
        interface that other registries
        will eventually implement.
        """

        return self._activities.get(
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
        Return one registered
        activity.
        """

        return self.get_object(
            name,
        )

    def has_object(
        self,
        name,
    ):
        """
        Return whether an activity
        exists.
        """

        return name in self._activities

    def resolve_object_property(
        self,
        object_name,
        property_name,
    ):
        """
        Resolve one property of a
        registered ActivitySpec.

        Examples
        --------

            workspace.initialize

                description

            annual_review

                frequency
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
        Evaluate all registered
        activities for one planning
        context.
        """

        return evaluate(
            row=row,
            registry=self,
        )
