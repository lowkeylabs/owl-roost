# src/owlroost/activity/activities/workspace_setup.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace setup activities.

Notes
-----
Registers the planning activities that
establish and inspect a ROOST
workspace.

These activities represent durable
planning milestones rather than
individual shell operations.

Provider discovery automatically
imports this module and invokes:

    register(reg)
"""

from __future__ import annotations

from typing import Any

from owlroost.activity.specs import (
    ActivityCategory,
    ActivityFrequency,
    ActivitySpec,
    Requirement,
)
from owlroost.catalog.ontology import (
    ONTOLOGY_DIMENSIONS,
    CatalogNodeType,
)
from owlroost.core.utils import (
    normalize_module_path,
)

# =========================================================
# Ontology
# =========================================================

ACTIVITY_ONTOLOGY: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="planning",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="context",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Activities
# =========================================================

ACTIVITIES = [
    # -----------------------------------------------------
    # Always available
    # -----------------------------------------------------
    dict(
        name="current.context",
        title="Review Current Context",
        description=(
            "Display the current planning context "
            "and determine the next recommended "
            "planning activities."
        ),
        category=ActivityCategory.WORKSPACE,
        frequency=ActivityFrequency.EVENT,
        display_order=10,
        suggested_commands=[
            "roost workspace",
        ],
    ),
    # -----------------------------------------------------
    # Workspace lifecycle
    # -----------------------------------------------------
    dict(
        name="workspace.initialize",
        title="Initialize Workspace",
        description=("Create a planning workspace in the current directory."),
        category=ActivityCategory.WORKSPACE,
        frequency=ActivityFrequency.ONCE,
        display_order=20,
        suggested_commands=[
            "roost workspace --init",
        ],
        requirements=[
            Requirement(
                "context.workspace_initialized",
                "==",
                False,
            ),
            Requirement(
                "context.workspace_parent_count",
                "==",
                0,
            ),
            Requirement(
                "context.workspace_child_count",
                "==",
                0,
            ),
            Requirement(
                "context.directory_kind",
                "in",
                [
                    "empty",
                    "planning",
                ],
            ),
        ],
    ),
    dict(
        name="workspace.review",
        title="Review Workspace",
        description=("Inspect the workspace structure and planning status."),
        category=ActivityCategory.WORKSPACE,
        frequency=ActivityFrequency.EVENT,
        display_order=30,
        suggested_commands=[
            "roost workspace",
        ],
        prerequisite_activities=[
            "workspace.initialize",
        ],
        requirements=[
            Requirement(
                "context.workspace_initialized",
                "==",
                True,
            ),
        ],
    ),
    # -----------------------------------------------------
    # Household inventory
    # -----------------------------------------------------
    dict(
        name="households.review",
        title="Review Households",
        description=("Review the households available for planning within the current workspace."),
        category=ActivityCategory.HOUSEHOLD,
        frequency=ActivityFrequency.EVENT,
        display_order=40,
        suggested_commands=[
            "roost cases",
        ],
        prerequisite_activities=[
            "workspace.initialize",
        ],
        requirements=[
            Requirement(
                "context.valid_case_count",
                ">",
                0,
            ),
        ],
    ),
]

# =========================================================
# Registration
# =========================================================


def register(
    reg,
):
    """
    Register planning activities.
    """

    for activity in ACTIVITIES:
        ontology = dict(
            ACTIVITY_ONTOLOGY,
        )

        for dimension in ONTOLOGY_DIMENSIONS:
            field = dimension.field_name

            if field in activity:
                ontology[field] = activity[field]

        reg.register(
            ActivitySpec(
                **activity,
                **ontology,
            )
        )
