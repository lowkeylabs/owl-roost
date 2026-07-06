# src/owlroost/display/views/activity.py
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

from owlroost.core.utils import normalize_module_path
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
    Register catalog inspection views.
    """

    reg.register_view(
        DisplayView(
            level="activity",
            name="suggestions",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "activity_suggestions", "depth": 5}),
            ],
            description=(
                "Summarizes the current "
                "workspace, its readiness "
                "for retirement planning, "
                "and available analytical "
                "artifacts."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="activity",
            name="details",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "activity_details", "depth": 5}),
            ],
            description=(
                "Summarizes the current "
                "workspace, its readiness "
                "for retirement planning, "
                "and available analytical "
                "artifacts."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="activity",
            name="status",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "activity_status", "depth": 5}),
            ],
            description=(
                "Summarizes the current "
                "workspace, its readiness "
                "for retirement planning, "
                "and available analytical "
                "artifacts."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="activity",
            name="reasoning",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "activity_reasoning", "depth": 99}),
            ],
            description=(
                "Summarizes the current "
                "workspace, its readiness "
                "for retirement planning, "
                "and available analytical "
                "artifacts."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="activity",
            name="variables",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "activity_variables", "depth": 5}),
            ],
            description=(
                "Summarizes the current "
                "workspace, its readiness "
                "for retirement planning, "
                "and available analytical "
                "artifacts."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="activity",
            name="diagnostics",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "activity_diagnostics", "depth": 5}),
            ],
            description=(
                "Summarizes the current "
                "workspace, its readiness "
                "for retirement planning, "
                "and available analytical "
                "artifacts."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
