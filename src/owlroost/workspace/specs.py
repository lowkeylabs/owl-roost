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
from datetime import datetime
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


# =====================================================
# Planning Context
# =====================================================


@dataclass(slots=True, frozen=True)
class PlanningSection:
    """
    One semantic section within a
    planning context.
    """

    name: str

    title: str

    description: str

    observations: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class HouseholdPlanningContext:
    """
    HouseholdPlanningContext is the
    highest-level semantic synthesis
    produced by the Workspace subsystem.

    It communicates the current planning
    situation for one household.

    It is intended to be consumed by:

        * Activity evaluation

        * Reports

        * Published evidence packages

        * LLM interfaces

    It is intentionally independent of
    presentation.
    """

    #
    # Identity
    #

    name: str

    title: str

    #
    # Narrative
    #

    description: str

    #
    # Planning characterization
    #

    sections: tuple[PlanningSection, ...] = ()


@dataclass(slots=True, frozen=True)
class WorkspacePlanningContext:
    """
    Semantic characterization of the
    current planning investigation.

    A Workspace Planning Context
    summarizes one or more household
    planning contexts together with
    workspace-level planning state.

    This object becomes the primary
    semantic entry point for:

        * roost .
        * reports
        * evidence packages
        * LLM interfaces
    """

    workspace_name: str

    overview: str

    generated_at: datetime

    households: tuple[HouseholdPlanningContext, ...] = ()

    sections: tuple[PlanningSection, ...] = ()
