# src/owlroost/guide/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from dataclasses import dataclass, field


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
    Registered guide suggestion.
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
