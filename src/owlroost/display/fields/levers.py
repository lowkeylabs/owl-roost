# src/owlroost/display/fields/levers.py
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

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.display.specs import (
    DisplayField,
)
from owlroost.study.bootstrap import (
    build_study_registry,
)

LEVER_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="decision",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="case",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

CHECK_MARK = "✓"
NO_MARK = "·"


def make_display_fn(
    lever,
):
    def display_fn(
        row,
    ):
        applicable = lever.applicable_fn(
            row,
        )

        return CHECK_MARK if applicable else NO_MARK

    return display_fn


def register_display_fields(
    reg,
):
    lever_registry = build_study_registry()

    for lever in lever_registry.all_levers():
        reg.register_display_field(
            DisplayField.field(
                f"lever.{lever.name}",
                display_fn=make_display_fn(
                    lever,
                ),
                description=(lever.description),
                profiles=(lever.profiles),
                **LEVER_ONTOLOGY,
            )
        )
