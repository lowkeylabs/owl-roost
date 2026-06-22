# src/owlroost/study/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study subsystem specifications.

Notes
-----
Owns the analytical definition layer
of the study subsystem.

Conceptually:

    Study
        ↓
    Question
        ↓
    Decision
        ↓
    Choice Template
        ↓
    Lever

Studies organize related questions.

Questions are the primary user-facing
analytical entities.

Decisions define dimensions of
investigation.

Choice templates define methodologies.

Levers determine applicability.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from owlroost.display.specs import (
    DisplayProfile,
)


@dataclass(slots=True)
class StudySpec:
    """
    Defines a collection of
    related retirement questions.

    Studies organize analytical
    exploration around a coherent
    topic area.

    Studies are intentionally
    independent of case applicability.

    Questions determine applicability
    through their associated decisions,
    choice templates, and levers.

    Questions may participate in
    multiple studies.
    """

    name: str

    title: str

    description: str

    question_names: list[str] = field(
        default_factory=list,
    )

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class QuestionSpec:
    """
    Defines a retirement question.

    Questions represent the primary
    user-facing entry point into the
    study subsystem.

    Examples include:

        Can I retire?

        When can I retire?

        How much can I spend?

        When should I claim
        Social Security?

        Should I perform
        Roth conversions?

    Questions may participate in
    multiple studies.

    Questions may reference one
    or more decisions.

    Questions are intentionally
    independent of case applicability.

    Applicability is determined by
    the decisions, choice templates,
    and levers associated with the
    question.
    """

    name: str

    title: str

    category: str

    description: str

    decision_names: list[str] = field(
        default_factory=list,
    )

    required_levers: list[str] = field(
        default_factory=list,
    )

    related_questions: list[str] = field(
        default_factory=list,
    )

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class DecisionSpec:
    """
    Defines an analytical dimension.

    A decision represents a dimension
    of variation or investigation that
    may contribute to answering one or
    more questions.

    Examples include:

        Social Security timing

        Roth conversion strategy

        Historical regime selection

        Trial count

        Worker scaling

    Questions reference decisions.

    Decisions do not reference
    questions directly.

    Applicability is determined by
    the available choice templates
    and their required levers.
    """

    name: str

    title: str

    category: str

    description: str

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class ChoiceTemplateSpec:
    """
    Defines a methodology for
    investigating a decision.

    A choice template specifies:

    * Which decision it supports
    * Which levers are required
    * Which override patterns are
      typically used

    Choice templates may later
    materialize experiments,
    sessions, reports, or study
    artifacts.
    """

    name: str

    decision_name: str

    title: str

    description: str

    required_levers: list[str] = field(
        default_factory=list,
    )

    overrides: list[str] = field(
        default_factory=list,
    )

    tags: list[str] = field(
        default_factory=list,
    )

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class LeverSpec:
    """
    Defines case-dependent capability
    requirements.

    Levers evaluate case structure and
    determine whether a particular
    investigation may be performed.

    Examples include:

        has_social_security

        has_pretax_savings

        has_retirement_timing

    Levers are intentionally unaware of
    studies, questions, decisions, and
    choice templates.

    Future versions may extend levers
    with explanatory and remediation
    guidance describing:

        Why a question cannot
        be answered.

        What information is
        missing.

        How the user can proceed.
    """

    name: str

    title: str

    description: str

    applicable_fn: Callable

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )
