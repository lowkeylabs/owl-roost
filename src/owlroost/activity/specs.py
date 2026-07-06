# src/owlroost/activity/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide semantic specifications.

Notes
-----
Guide specifications describe workflow
knowledge rather than execution logic.

Guide providers register GuideSpec
objects.

The guide engine evaluates those
workflow definitions against the
current planning context and produces
GuideEvaluation objects describing the
evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from owlroost.catalog.ontology import (
    OntologySpec,
)

# =========================================================
# Guide Specifications
# =========================================================


class ActivityFrequency(StrEnum):
    """
    Recommended repetition interval.
    """

    ONCE = "once"

    ANNUAL = "annual"

    QUARTERLY = "quarterly"

    MONTHLY = "monthly"

    EVENT = "event"


class ActivityCategory(StrEnum):
    """
    Broad classification of planning
    activities.

    Categories organize activities for
    presentation and navigation. They
    do not affect evaluation.
    """

    WORKSPACE = "workspace"

    HOUSEHOLD = "household"

    REVIEW = "review"

    DECISION = "decision"

    REPORTING = "reporting"

    GENERAL = "general"


@dataclass(slots=True)
class Requirement:
    """
    One applicability requirement.
    """

    variable: str

    operator: str = "=="

    value: object = True

    _PROPERTY_DESCRIPTIONS = {
        "variable": "Semantic variable evaluated.",
        "operator": "Comparison operator used when evaluating the requirement.",
        "value": "Expected value for the semantic variable.",
    }

    def describe_property(
        self,
        property_name,
    ):
        return self._PROPERTY_DESCRIPTIONS.get(
            property_name,
            "",
        )

    def label_property(
        self,
        property_name,
    ):
        return property_name.replace(
            "_",
            " ",
        ).title()


# =========================================================
# Activity Specifications
# =========================================================


@dataclass(kw_only=True)
class ActivitySpec(
    OntologySpec,
):
    """
    One planning activity.

    Notes
    -----
    Activities describe recommended
    retirement planning practice.

    Activities are declarative.

    They do not perform work.
    """

    # =====================================================
    # Identity
    # =====================================================

    name: str

    title: str

    description: str = ""

    # =====================================================
    # Authoring
    # =====================================================

    defined_in: str | None = None

    # =====================================================
    # Planning
    # =====================================================

    category: ActivityCategory = ActivityCategory.GENERAL

    display_order: int = 100

    frequency: ActivityFrequency = ActivityFrequency.ONCE

    # =====================================================
    # Dependencies
    # =====================================================

    requirements: list[Requirement] = field(
        default_factory=list,
    )

    prerequisite_activities: list[str] = field(
        default_factory=list,
    )

    # =====================================================
    # Evidence
    # =====================================================

    required_scenario_families: list[str] = field(
        default_factory=list,
    )

    # =====================================================
    # Suggested Commands
    # =====================================================

    suggested_commands: list[str] = field(
        default_factory=list,
    )

    _PROPERTY_DESCRIPTIONS = {
        "title": "Human-readable activity title.",
        "description": "Explanation of what this activity accomplishes.",
        "category": "Planning activity category.",
        "display_order": "Evaluation order for planning activities.",
        "frequency": "Recommended repetition interval.",
        "prerequisite_activities": ("Activities that should be completed first."),
        "required_scenario_families": ("Scenario families for which evidence should be collected."),
        "suggested_commands": ("Suggested commands supporting this activity."),
    }

    def describe_property(
        self,
        property_name,
    ):
        if property_name == "description":
            return self.description

        return self._PROPERTY_DESCRIPTIONS.get(
            property_name,
            "",
        )

    def label_property(
        self,
        property_name,
    ):
        return property_name.replace(
            "_",
            " ",
        ).title()

    @property
    def has_requirements(self):
        return bool(self.requirements)

    @property
    def has_required_scenarios(self):
        return bool(self.required_scenario_families)

    @property
    def has_prerequisites(self):
        return bool(self.prerequisite_activities)

    @property
    def has_suggested_commands(self):
        return bool(self.suggested_commands)

    @property
    def is_repeatable(
        self,
    ):
        return self.frequency != ActivityFrequency.ONCE


# =========================================================
# Evaluation Results
# =========================================================


@dataclass(slots=True)
class RequirementResult:
    """
    Result of evaluating one requirement.
    """

    requirement: Requirement

    actual: object

    satisfied: bool

    _PROPERTY_DESCRIPTIONS = {
        "actual": "Observed value of the semantic variable.",
        "satisfied": "Whether the requirement evaluated successfully.",
    }

    def describe_property(
        self,
        property_name,
    ):
        if property_name.startswith(
            "requirement.",
        ):
            return self.requirement.describe_property(
                property_name.removeprefix(
                    "requirement.",
                )
            )

        return self._PROPERTY_DESCRIPTIONS.get(
            property_name,
            "",
        )

    def label_property(
        self,
        property_name,
    ):
        if property_name.startswith(
            "requirement.",
        ):
            return self.requirement.label_property(
                property_name.removeprefix(
                    "requirement.",
                )
            )

        return property_name.replace(
            "_",
            " ",
        ).title()


@dataclass(slots=True)
class ActivityResult:
    """
    Result of evaluating one activity.

    Notes
    -----
    Future versions may enrich this
    object with planning-cycle state,
    freshness, completion dates, and
    evidence coverage.

    For now it simply reports
    applicability.
    """

    activity: ActivitySpec

    applicable: bool

    requirement_results: list[RequirementResult] = field(
        default_factory=list,
    )

    _PROPERTY_DESCRIPTIONS = {
        "applicable": "Whether this activity is currently applicable.",
    }

    def describe_property(
        self,
        property_name,
    ):
        if property_name.startswith(
            "activity.",
        ):
            return self.activity.describe_property(
                property_name.removeprefix(
                    "activity.",
                )
            )

        return self._PROPERTY_DESCRIPTIONS.get(
            property_name,
            "",
        )

    def label_property(
        self,
        property_name,
    ):
        if property_name.startswith(
            "activity.",
        ):
            return self.activity.label_property(
                property_name.removeprefix(
                    "activity.",
                )
            )

        return property_name.replace(
            "_",
            " ",
        ).title()


@dataclass(slots=True)
class ActivityEvaluation:
    """
    Complete activity evaluation.

    Notes
    -----
    Retains the complete planning
    activity evaluation together with
    useful subsets consumed by display,
    explain, and future workflow
    tooling.
    """

    # =====================================================
    # Activity Results
    # =====================================================

    all_activities: list[ActivityResult] = field(
        default_factory=list,
    )

    applicable_activities: list[ActivityResult] = field(
        default_factory=list,
    )

    rejected_activities: list[ActivityResult] = field(
        default_factory=list,
    )

    # =====================================================
    # Coverage
    # =====================================================

    observed_variables: set[str] = field(
        default_factory=set,
    )

    required_variables: set[str] = field(
        default_factory=set,
    )

    unused_variables: set[str] = field(
        default_factory=set,
    )
