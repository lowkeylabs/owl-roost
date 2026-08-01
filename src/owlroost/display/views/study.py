# src/owlroost/display/views/study.py
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
            level="study",
            name="study",
            entries=[
                # =====================================
                # Workspace context
                # =====================================
                "study.name",
                "experiment.name",
                "study.defined_in",
                ("study.run_row_views", {"modes": ["pivot"]}),
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
