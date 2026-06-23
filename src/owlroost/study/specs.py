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
    Scenario Family
        ↓
    Choice Template
        ↓
    Lever

Studies organize related questions.

Questions represent information needs.

Scenario families define evidence spaces.

Choice templates define methodologies.

Levers determine applicability.

The study subsystem defines work
that should be performed.

The realization subsystem executes
that work and generates evidence.

The interpretation layer consumes
evidence and produces guidance.
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

    Questions may participate in
    multiple studies.

    Studies are organizational
    entities and do not own
    execution artifacts.
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

        Should I retire?

        When should I retire?

        When should I claim
        Social Security?

        How much can I spend?

    Questions identify information
    needs.

    Questions consume evidence but
    do not directly generate it.

    Evidence generation is delegated
    to one or more scenario families.
    """

    name: str

    title: str

    category: str

    description: str

    scenario_family_names: list[str] = field(
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
class ScenarioFamilySpec:
    """
    Defines a reusable evidence-
    generation space.

    Scenario families organize
    related what-if investigations.

    Examples include:

        retirement_timing

        social_security_claiming

        roth_conversion

        spending_level

        market_regime

    A scenario family answers:

        What evidence should
        be generated?

    Scenario families may support
    multiple questions.

    Questions may depend upon
    multiple scenario families.
    """

    name: str

    title: str

    category: str

    description: str

    required_levers: list[str] = field(
        default_factory=list,
    )

    related_scenario_families: list[str] = field(
        default_factory=list,
    )

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
    generating evidence within a
    scenario family.

    Choice templates answer:

        How should this scenario
        family be explored?

    Examples include:

        yearly_sweep

        monthly_sweep

        historical_windows

        bootstrap_regimes

        owl_optimizer

    Choice templates are reusable
    analytical recipes.

    They are not execution
    artifacts.
    """

    name: str

    scenario_family_name: str

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

    Levers determine whether a
    question, scenario family, or
    choice template may be applied.

    Examples include:

        has_social_security

        has_pretax_savings

        has_retirement_timing

    Future versions may extend
    levers with remediation and
    guidance describing:

        Why a question cannot
        be answered.

        What information is
        missing.

        What assumptions are
        required.

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
