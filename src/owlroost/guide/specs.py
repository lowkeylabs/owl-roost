# src/owlroost/guide/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide subsystem specifications.

Notes
-----
Guide specifications describe workflow
knowledge rather than execution logic.

Providers register SuggestionSpec objects.

The guide engine evaluates those
suggestions against the current planning
context and produces EvaluationResult
objects describing the evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

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


@dataclass(slots=True)
class SuggestionSpec:
    """
    Registered workflow suggestion.
    """

    name: str

    title: str

    description: str

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
class SuggestionResult:
    """
    Result of evaluating one suggestion.
    """

    suggestion: SuggestionSpec

    applicable: bool

    requirement_results: list[RequirementResult] = field(
        default_factory=list,
    )


@dataclass(slots=True)
class EvaluationResult:
    """
    Complete guide evaluation.

    Notes
    -----
    Retains the complete evaluation
    together with convenient subsets
    used by guide renderers and
    explain facets.
    """

    all_suggestions: list[SuggestionResult] = field(
        default_factory=list,
    )

    applicable_suggestions: list[SuggestionResult] = field(
        default_factory=list,
    )

    rejected_suggestions: list[SuggestionResult] = field(
        default_factory=list,
    )

    observed_variables: set[str] = field(
        default_factory=set,
    )

    required_variables: set[str] = field(
        default_factory=set,
    )

    unused_variables: set[str] = field(
        default_factory=set,
    )


@dataclass(slots=True)
class GuideStats:
    suggestion_count: int

    top_suggestion: str | None

    has_suggestions: bool
