# src/owlroost/activity/activities/household_setup.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household setup activities.

Notes
-----
Registers the planning activities
required to establish one or more
canonical retirement plans within an
initialized ROOST workspace.

A retirement plan represents the
household's current financial state
using an OWL household configuration
together with an optional Household
Financial Profile (HFP).

Activities consume semantic variables
materialized by the workspace
subsystem.

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
    # Retirement plan creation
    # -----------------------------------------------------
    dict(
        name="household.create_plan",
        title="Create Retirement Plan",
        description=(
            "Create a canonical retirement "
            "plan representing the current "
            "financial situation of a "
            "household. A completed plan "
            "contains an OWL household "
            "configuration together with "
            "an optional Household "
            "Financial Profile (HFP)."
        ),
        category=ActivityCategory.HOUSEHOLD,
        display_order=100,
        frequency=ActivityFrequency.ONCE,
        prerequisite_activities=[
            "workspace.initialize",
        ],
        suggested_commands=[
            "roost household --new",
            "roost household --import",
            "roost household --library",
        ],
        requirements=[
            Requirement(
                "context.workspace_initialized",
                "==",
                True,
            ),
            Requirement(
                "context.valid_case_count",
                "==",
                0,
            ),
        ],
    ),
    # -----------------------------------------------------
    # Retirement plan review
    # -----------------------------------------------------
    dict(
        name="household.review_plans",
        title="Review Retirement Plans",
        description=(
            "Review the retirement plans "
            "currently available within "
            "the workspace before selecting "
            "one for further planning."
        ),
        category=ActivityCategory.HOUSEHOLD,
        display_order=110,
        frequency=ActivityFrequency.EVENT,
        prerequisite_activities=[
            "household.create_plan",
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
]

# =========================================================
# Registration
# =========================================================


def register(
    reg,
):
    """
    Register household setup activities.
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
