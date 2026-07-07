# src/owlroost/workspace/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace semantic specifications.

Notes
-----
WorkspaceSpec defines canonical
workspace inventory ontology.

Workspace observations describe:

    - workspace identity
    - workspace structure
    - workspace inventory
    - workspace realization state

These values materialize into:

    row["_workspace"]

and participate in catalog synthesis
alongside schema and metrics.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from owlroost.catalog.ontology import (
    OntologySpec,
)


class OverridePolicy(StrEnum):
    """
    Policy governing whether and how a
    semantic observation may be replaced
    by persisted workspace configuration.
    """

    NEVER = "never"

    REPLACE = "replace"

    RECOMPUTE = "recompute"


@dataclass(kw_only=True)
class WorkspaceSpec(
    OntologySpec,
):
    """
    Canonical workspace observation.
    """

    # =====================================================
    # Identity
    # =====================================================

    name: str

    description: str = ""

    # =====================================================
    # Authoring
    # =====================================================

    defined_in: str | None = None

    # =====================================================
    # Typing
    # =====================================================

    dtype: type | None = object

    # =====================================================
    # Materialization
    # =====================================================

    compute_fn: Callable[[dict[str, Any]], Any] | None = None

    # =====================================================
    # Configuration
    # =====================================================
    #
    # Workspace configuration may replace
    # this computed semantic observation.
    #
    override_policy: OverridePolicy = OverridePolicy.NEVER

    # =====================================================
    # Notes
    # =====================================================

    notes: str = ""
