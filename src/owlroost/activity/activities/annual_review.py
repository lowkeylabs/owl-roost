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
activities comprising the ROOST annual
planning cycle.

The goal of the annual review is to
produce current evidence supporting
retirement decisions for the coming
year and package that evidence for
future planning cycles.

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
    # Begin planning cycle
    # -----------------------------------------------------
    dict(
        name="annual.begin",
        title="Begin Annual Review",
        description=("Begin a new annual retirement planning cycle."),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=200,
        suggested_commands=[
            "roost workspace",
        ],
        requirements=[
            Requirement(
                "context.workspace.valid_case_count",
                ">",
                0,
            ),
        ],
    ),
    # -----------------------------------------------------
    # Household review
    # -----------------------------------------------------
    dict(
        name="annual.household",
        title="Review Current Household",
        description=(
            "Verify that the retirement "
            "household accurately reflects "
            "the current financial and "
            "personal situation."
        ),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=210,
        prerequisite_activities=[
            "annual.begin",
        ],
        suggested_commands=[
            "roost cases",
        ],
    ),
    # -----------------------------------------------------
    # Characterization
    # -----------------------------------------------------
    dict(
        name="annual.characterize",
        title="Characterize Household",
        description=(
            "Characterize the household to "
            "identify planning levers, "
            "constraints, and applicable "
            "retirement scenario families."
        ),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=220,
        prerequisite_activities=[
            "annual.household",
        ],
        suggested_commands=[
            "roost workspace",
        ],
    ),
    # -----------------------------------------------------
    # Scenario identification
    # -----------------------------------------------------
    dict(
        name="annual.scenarios",
        title="Identify Applicable Scenario Families",
        description=(
            "Determine which retirement "
            "decisions require updated "
            "evidence during the current "
            "planning cycle."
        ),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=230,
        prerequisite_activities=[
            "annual.characterize",
        ],
    ),
    # -----------------------------------------------------
    # Experiment planning
    # -----------------------------------------------------
    dict(
        name="annual.experiments",
        title="Design Planning Experiments",
        description=(
            "Design the experiments needed "
            "to collect evidence for each "
            "applicable retirement scenario "
            "family."
        ),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=240,
        prerequisite_activities=[
            "annual.scenarios",
        ],
    ),
    # -----------------------------------------------------
    # Evidence generation
    # -----------------------------------------------------
    dict(
        name="annual.evidence",
        title="Generate Decision Evidence",
        description=("Generate retirement planning evidence for every applicable scenario family."),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=250,
        prerequisite_activities=[
            "annual.experiments",
        ],
        suggested_commands=[
            "roost build",
            "roost run",
        ],
    ),
    # -----------------------------------------------------
    # Longitudinal comparison
    # -----------------------------------------------------
    dict(
        name="annual.compare",
        title="Compare With Previous Reviews",
        description=(
            "Compare the current planning "
            "cycle with previous reviews to "
            "understand how the retirement "
            "plan has evolved over time."
        ),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=260,
        prerequisite_activities=[
            "annual.evidence",
        ],
        suggested_commands=[
            "roost compare",
        ],
    ),
    # -----------------------------------------------------
    # Evidence interpretation
    # -----------------------------------------------------
    dict(
        name="annual.analysis",
        title="Analyze Planning Evidence",
        description=(
            "Interpret the evidence and "
            "identify the retirement "
            "decisions supported by the "
            "current planning cycle."
        ),
        category=ActivityCategory.REVIEW,
        frequency=ActivityFrequency.ANNUAL,
        display_order=270,
        prerequisite_activities=[
            "annual.compare",
        ],
        suggested_commands=[
            "roost results",
            "roost reports",
        ],
    ),
    # -----------------------------------------------------
    # Decisions
    # -----------------------------------------------------
    dict(
        name="annual.decisions",
        title="Make Retirement Decisions",
        description=(
            "Use the accumulated evidence "
            "to establish spending, Roth "
            "conversions, withdrawal "
            "strategies, tax strategies, "
            "and other retirement decisions "
            "for the coming year."
        ),
        category=ActivityCategory.DECISION,
        frequency=ActivityFrequency.ANNUAL,
        display_order=280,
        prerequisite_activities=[
            "annual.analysis",
        ],
    ),
    # -----------------------------------------------------
    # Publish
    # -----------------------------------------------------
    dict(
        name="annual.publish",
        title="Publish Annual Review",
        description=(
            "Package the annual retirement "
            "review together with its "
            "supporting evidence for future "
            "planning cycles and external "
            "decision makers."
        ),
        category=ActivityCategory.REPORTING,
        frequency=ActivityFrequency.ANNUAL,
        display_order=290,
        prerequisite_activities=[
            "annual.decisions",
        ],
        suggested_commands=[
            "roost reports",
            "roost package",
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
