# src/owlroost/display/views/guide.py
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
            name="guide",
            entries=[
                # =====================================
                # Workspace Inventory
                # =====================================
                ("tree", {"root": "guide_tree", "depth": 2}),
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
