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

    A decision represents a question that
    may be asked for a particular case.

    Applicability is determined by the
    required lever set.
    """

    name: str

    title: str

    category: str

    description: str

    required_levers: list[str] = field(
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
    Defines case applicability
    for one or more decisions.
    """

    name: str

    title: str

    description: str

    decision_names: list[str]

    applicable_fn: Callable

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )
