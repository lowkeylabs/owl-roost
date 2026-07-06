# src/owlroost/activity/activities/annual_review.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Annual retirement review activities.

Notes
-----
Registers the repeatable planning
activities supporting an annual
retirement review.

The goal of the annual review is to
produce current evidence supporting
spending, withdrawal, tax, and other
retirement decisions for the coming
year.

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
    # Review household
    # -----------------------------------------------------
    dict(
        name="review.household",
        title="Review Current Household",
        description=(
            "Verify that the retirement plan accurately represents the current financial situation."
        ),
        category=ActivityCategory.REVIEW,
        display_order=200,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "household.review_plans",
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
    # Characterization
    # -----------------------------------------------------
    dict(
        name="review.characterize",
        title="Characterize Household",
        description=(
            "Characterize the household to "
            "identify available planning "
            "levers and applicable scenario "
            "families."
        ),
        category=ActivityCategory.REVIEW,
        display_order=210,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.household",
        ],
        suggested_commands=[
            "roost workspace",
        ],
    ),
    # -----------------------------------------------------
    # Applicable scenarios
    # -----------------------------------------------------
    dict(
        name="review.scenarios",
        title="Determine Applicable Scenario Families",
        description=("Identify the retirement planning questions requiring updated evidence."),
        category=ActivityCategory.REVIEW,
        display_order=220,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.characterize",
        ],
    ),
    # -----------------------------------------------------
    # Evidence generation
    # -----------------------------------------------------
    dict(
        name="review.build_evidence",
        title="Build Planning Evidence",
        description=("Generate current evidence for all applicable scenario families."),
        category=ActivityCategory.REVIEW,
        display_order=230,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.scenarios",
        ],
        suggested_commands=[
            "roost build",
            "roost run",
        ],
    ),
    # -----------------------------------------------------
    # Evidence review
    # -----------------------------------------------------
    dict(
        name="review.review_evidence",
        title="Review Planning Evidence",
        description=("Review the evidence generated for the current planning cycle."),
        category=ActivityCategory.REVIEW,
        display_order=240,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.build_evidence",
        ],
        suggested_commands=[
            "roost results",
            "roost reports",
        ],
    ),
    # -----------------------------------------------------
    # Longitudinal comparison
    # -----------------------------------------------------
    dict(
        name="review.compare",
        title="Compare With Previous Reviews",
        description=(
            "Compare current evidence with "
            "previous planning cycles to "
            "understand how the retirement "
            "plan has evolved."
        ),
        category=ActivityCategory.REVIEW,
        display_order=250,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.review_evidence",
        ],
        suggested_commands=[
            "roost compare",
        ],
    ),
    # -----------------------------------------------------
    # Planning decisions
    # -----------------------------------------------------
    dict(
        name="review.policy",
        title="Establish Annual Spending Policy",
        description=(
            "Use the accumulated evidence "
            "to establish spending, Roth "
            "conversion, withdrawal, and "
            "other retirement decisions "
            "for the coming year."
        ),
        category=ActivityCategory.DECISION,
        display_order=260,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.compare",
        ],
    ),
    # -----------------------------------------------------
    # Package review
    # -----------------------------------------------------
    dict(
        name="review.publish",
        title="Package Annual Review",
        description=(
            "Package the retirement review "
            "and supporting evidence for "
            "future planning cycles or "
            "consultation."
        ),
        category=ActivityCategory.REPORTING,
        display_order=270,
        frequency=ActivityFrequency.ANNUAL,
        prerequisite_activities=[
            "review.policy",
        ],
        suggested_commands=[
            "roost package",
            "roost reports",
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
    Register annual review activities.
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
