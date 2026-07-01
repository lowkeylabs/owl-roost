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
