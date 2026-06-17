# src/owlroost/display/views/choice_templates.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Choice template display view.

Notes
-----
Dynamically materializes a view
containing all registered choice
templates.

Each column indicates whether a
particular methodology is applicable
to the selected case.
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
    study_registry = build_study_registry()

    entries = [
        "case_name",
    ]

    for template in study_registry.all_choice_templates():
        entries.append(f"choice_template.{template.name}")

    reg.register_view(
        DisplayView(
            level="row",
            name="choice_templates",
            entries=entries,
            description=("Choice templates available for this case."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
