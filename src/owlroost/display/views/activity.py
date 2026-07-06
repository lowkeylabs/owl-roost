# src/owlroost/display/views/activity.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning activity display views.

Notes
-----
Registers display views that present
ROOST planning activities from several
perspectives.

The views range from concise
recommendations ("what should I do
next?") through detailed reasoning and
diagnostics used to understand activity
evaluation.
"""

from __future__ import annotations

from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.display.specs import (
    DisplayView,
)

SHARED_VIEW_ONTOLOGY = dict(
    defined_in=normalize_module_path(__file__),
)


def register_display_views(
    reg,
):
    """
    Register planning activity views.
    """

    # =====================================================
    # Recommended Next Activities
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="next",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_next",
                        "depth": 3,
                    },
                ),
            ],
            description=("Recommended planning activities that are ready to perform now."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    # =====================================================
    # overall workflow
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="workflow",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_workflow",
                        "depth": 3,
                    },
                ),
            ],
            description=("Overall workflow"),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    # =====================================================
    # Activity Status
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="status",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_status",
                        "depth": 4,
                    },
                ),
            ],
            description=("Current readiness of all planning activities."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    # =====================================================
    # Activity Details
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="details",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_details",
                        "depth": 6,
                    },
                ),
            ],
            description=(
                "Detailed descriptions, "
                "dependencies, evidence "
                "requirements, and suggested "
                "commands for planning "
                "activities."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    # =====================================================
    # Activity Reasoning
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="reasoning",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_reasoning",
                        "depth": 99,
                    },
                ),
            ],
            description=(
                "Shows how the readiness state "
                "of each activity was determined "
                "from semantic requirements."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    # =====================================================
    # Evaluation Variables
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="variables",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_variables",
                        "depth": 2,
                    },
                ),
            ],
            description=("Semantic variables consulted while evaluating planning activities."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    # =====================================================
    # Diagnostics
    # =====================================================

    reg.register_view(
        DisplayView(
            level="activity",
            name="diagnostics",
            entries=[
                (
                    "tree",
                    {
                        "root": "activity_diagnostics",
                        "depth": 3,
                    },
                ),
            ],
            description=(
                "Internal evaluation statistics and planning activity engine diagnostics."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
