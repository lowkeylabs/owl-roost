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

    experiment_names: list[str] = field(
        default_factory=list,
    )

    defined_in: str | None = (None,)

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class ExperimentSpec:
    """
    Defines an unrealized experimental
    design.

    A Choice Template specifies a
    reusable methodology for exploring
    a scenario family.

    A Choice Template consists of:

        • Fixed model overrides

        • Variable model overrides

        • Applicability requirements

    When materialized for a household,
    a Choice Template becomes a Session.

    The Session expands the variable
    overrides into one or more Runs.

    Runs are the primary units of
    comparison.

    Sessions exist to concisely define
    large collections of related Runs.

    Examples include:

        Bootstrap Sequence of Returns

        Historical Average Returns

        Fixed Return Models

        Historical Replay

        Social Security Age Sweep

        Retirement Date Sweep
    """

    #
    # Identity
    #

    name: str

    title: str

    description: str

    #
    # Applicability
    #

    required_levers: list[str] = field(
        default_factory=lambda: [
            "workspace.levers.is_initialized",
        ],
    )

    optional_levers: list[str] = field(
        default_factory=list,
    )

    #
    # Experimental Design
    #

    fixed_overrides: list[str] = field(
        default_factory=list,
    )

    variable_overrides: list[str] = field(
        default_factory=list,
    )

    defined_in: str | None = (None,)

    #
    # Display
    #

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )
