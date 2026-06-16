# src/owlroost/display/views/decisions.py
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

from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.display.specs import (
    DisplayView,
)
from owlroost.study.bootstrap import (
    build_study_registry,
)

SHARED_VIEW_ONTOLOGY = dict(
    defined_in=normalize_module_path(
        __file__,
    ),
)


def register_display_views(
    reg,
):
    decision_registry = build_study_registry()

    entries = [
        "case_name",
    ]

    for decision in decision_registry.all_decisions():
        entries.append(f"decision.{decision.name}")

    reg.register_view(
        DisplayView(
            level="row",
            name="decisions",
            entries=entries,
            description=("Decisions available for this case."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
