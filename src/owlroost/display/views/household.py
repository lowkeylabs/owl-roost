# src/owlroost/display/views/household.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household display views.

Notes
-----
Display views for registered
Household Projects.
"""

from __future__ import annotations

from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.display.specs import (
    DisplayView,
)

SHARED_VIEW_ONTOLOGY = dict(
    defined_in=normalize_module_path(
        __file__,
    ),
)


def register_display_views(
    reg,
):
    """
    Register household display views.
    """

    reg.register_view(
        DisplayView(
            level="household",
            name="household",
            entries=[
                # =====================================
                # Identity
                # =====================================
                ("section", "Identity"),
                "household.id",
                "household.library",
                "household.title",
                # ("description",{"mode":"pivot"}),
                "household.tags",
                # =====================================
                # Project
                # =====================================
                # ("section", "Project"),
                # "root",
            ],
            description=(
                "Canonical Household Project view. "
                "Table mode supports browsing and "
                "selection of registered households. "
                "Pivot mode exposes the complete "
                "Household Project metadata."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
