# src/owlroost/guide/specs.py
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

from owlroost.catalog.ontology import (
    OntologySpec,
)

# =========================================================
# Guide Specifications
# =========================================================


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


@dataclass(kw_only=True)
class GuideSpec(
    OntologySpec,
):
    #
    # Identity
    #

    name: str

    title: str

    description: str = ""

    #
    # Authoring
    #

    defined_in: str | None = None

    #
    # Workflow
    #

    command: str | None = None

    category: str = "general"

    priority: int = 100

    requirements: list[Requirement] = field(
        default_factory=list,
    )

    _PROPERTY_DESCRIPTIONS = {
        "title": "Human-readable guide title.",
        "description": "Explanation of what this workflow step accomplishes.",
        "command": "Command to execute this workflow step.",
        "priority": "Evaluation order for workflow guidance.",
        "category": "Workflow category.",
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
            return self.requirement.describe_property(property_name.removeprefix("requirement."))

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
            return self.requirement.label_property(property_name.removeprefix("requirement."))

        return property_name.replace(
            "_",
            " ",
        ).title()


@dataclass(slots=True)
class GuideResult:
    """
    Result of evaluating one guide.
    """

    guide: GuideSpec

    applicable: bool

    requirement_results: list[RequirementResult] = field(
        default_factory=list,
    )

    _PROPERTY_DESCRIPTIONS = {
        "applicable": "Whether this guide is currently applicable.",
    }

    def describe_property(
        self,
        property_name,
    ):
        if property_name.startswith(
            "guide.",
        ):
            return self.guide.describe_property(property_name.removeprefix("guide."))

        return self._PROPERTY_DESCRIPTIONS.get(
            property_name,
            "",
        )

    def label_property(
        self,
        property_name,
    ):
        if property_name.startswith(
            "guide.",
        ):
            return self.guide.label_property(property_name.removeprefix("guide."))

        return property_name.replace(
            "_",
            " ",
        ).title()


@dataclass(slots=True)
class GuideEvaluation:
    """
    Complete guide evaluation.

    Notes
    -----
    Retains the complete workflow
    evaluation together with useful
    subsets consumed by display,
    explain, and future workflow
    tooling.
    """

    # =====================================================
    # Guide Results
    # =====================================================

    all_guides: list[GuideResult] = field(
        default_factory=list,
    )

    applicable_guides: list[GuideResult] = field(
        default_factory=list,
    )

    rejected_guides: list[GuideResult] = field(
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
