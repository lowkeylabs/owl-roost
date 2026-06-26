# src/owlroost/display/views/workspace.py
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
            level="workspace",
            name="workspace",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "workspace_tree", "depth": 2, "label": "."}),
                # =====================================
                # Scenario Families
                # =====================================
                (
                    "tree",
                    {
                        "root": "study_tree.scenario_families",
                        "label": "Available Scenario Families",
                        "depth": 5,
                        "order": [
                            "market_uncertainty",
                            "social_security_claiming",
                            "retirement_timing",
                        ],
                    },
                ),
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
            level="workspace",
            name="summary",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "workspace.identity.name",
            ],
            description=("Summary view of workspace status"),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
