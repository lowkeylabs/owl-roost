# src/owlroost/activity/activities/household_setup.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household lifecycle activities.

Notes
-----
Registers the planning activities
required to establish and manage
retirement households within an
initialized ROOST workspace.

A household is the canonical
representation of a retiree or
retiring household. It consists of an
OWL household configuration together
with an optional Household Financial
Profile (HFP).

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
    # Household creation
    # -----------------------------------------------------
    dict(
        name="household.create",
        title="Create Retirement Household",
        description=(
            "Create a retirement household "
            "consisting of an OWL household "
            "configuration together with an "
            "optional Household Financial "
            "Profile (HFP)."
        ),
        category=ActivityCategory.HOUSEHOLD,
        frequency=ActivityFrequency.ONCE,
        display_order=100,
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
    # Household inventory
    # -----------------------------------------------------
    dict(
        name="household.inventory",
        title="Review Retirement Households",
        description=("Review the retirement households available within the current workspace."),
        category=ActivityCategory.HOUSEHOLD,
        frequency=ActivityFrequency.EVENT,
        display_order=110,
        prerequisite_activities=[
            "workspace.initialize",
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
    # -----------------------------------------------------
    # Household selection
    # -----------------------------------------------------
    dict(
        name="household.select",
        title="Select Active Household",
        description=(
            "Select the retirement household "
            "that will serve as the basis for "
            "the current planning cycle."
        ),
        category=ActivityCategory.HOUSEHOLD,
        frequency=ActivityFrequency.EVENT,
        display_order=120,
        prerequisite_activities=[
            "household.inventory",
        ],
        suggested_commands=[
            "roost household",
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
    Register household lifecycle
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
