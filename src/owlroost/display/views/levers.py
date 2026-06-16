# src/owlroost/display/views/levers.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Lever display views.

Notes
-----
Case-level decision leverage views.

Views are dynamically constructed
from the registered lever set.
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
    """
    Register lever views.

    Entries are dynamically expanded
    from the lever registry.
    """

    lever_registry = build_study_registry()

    entries = [
        "case_name",
    ]

    for lever in lever_registry.all_levers():
        entries.append(f"lever.{lever.name}")

    reg.register_view(
        DisplayView(
            level="row",
            name="levers",
            entries=entries,
            description=("Levers available for this case."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
