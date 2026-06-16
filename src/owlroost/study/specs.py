# src/owlroost/study/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study subsystem specifications.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from owlroost.display.specs import (
    DisplayProfile,
)


@dataclass(slots=True)
class DecisionSpec:
    """
    Defines a decision space.

    A decision represents a question
    that may be investigated.

    Decisions are intentionally
    independent of case applicability.

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
    Defines case applicability.

    Levers evaluate case structure
    and determine whether a choice
    template may be applied.
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
