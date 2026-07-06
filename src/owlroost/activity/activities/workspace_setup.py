# src/owlroost/activity/activities/workspace_setup.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace lifecycle activities.

Notes
-----
Registers the planning activities that
establish a ROOST workspace and prepare
it for retirement planning.

These activities represent durable
planning milestones rather than
individual shell operations.

Provider discovery automatically
imports this module and invokes

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
    # Context
    # -----------------------------------------------------
    dict(
        name="workspace.context",
        title="Review Current Context",
        description=(
            "Determine the current planning "
            "context and identify the next "
            "recommended planning milestones."
        ),
        category=ActivityCategory.WORKSPACE,
        frequency=ActivityFrequency.EVENT,
        display_order=10,
        suggested_commands=[
            "roost workspace",
        ],
    ),
    # -----------------------------------------------------
    # Workspace
    # -----------------------------------------------------
    dict(
        name="workspace.initialize",
        title="Initialize Workspace",
        description=("Create a new ROOST workspace to hold retirement planning artifacts."),
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
        description=(
            "Inspect the workspace structure and determine its readiness for retirement planning."
        ),
        category=ActivityCategory.WORKSPACE,
        frequency=ActivityFrequency.EVENT,
        display_order=30,
        prerequisite_activities=[
            "workspace.initialize",
        ],
        suggested_commands=[
            "roost workspace",
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
    # Households
    # -----------------------------------------------------
    dict(
        name="households.inventory",
        title="Review Households",
        description=("Review the retirement households available within the current workspace."),
        category=ActivityCategory.HOUSEHOLD,
        frequency=ActivityFrequency.EVENT,
        display_order=40,
        prerequisite_activities=[
            "workspace.review",
        ],
        suggested_commands=[
            "roost cases",
        ],
        requirements=[
            Requirement(
                "context.valid_case_count",
                ">",
                0,
            ),
        ],
    ),
    dict(
        name="households.create",
        title="Create Retirement Household",
        description=(
            "Create a retirement household by "
            "assembling a household TOML file "
            "and Household Financial Profile "
            "(HFP)."
        ),
        category=ActivityCategory.HOUSEHOLD,
        frequency=ActivityFrequency.ONCE,
        display_order=50,
        prerequisite_activities=[
            "workspace.initialize",
        ],
        suggested_commands=[
            "roost household",
        ],
        requirements=[
            Requirement(
                "context.valid_case_count",
                "==",
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
    Register workspace lifecycle
    activities.
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
