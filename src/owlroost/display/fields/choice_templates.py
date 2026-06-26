# src/owlroost/display/fields/choice_templates.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Choice template display fields.

Notes
-----
Dynamically materializes one display
field per registered choice template.

Each field indicates whether the
choice template is applicable to
the current workspace.
"""

from __future__ import annotations

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.display.specs import (
    DisplayField,
)
from owlroost.study.bootstrap import (
    build_study_registry,
)
from owlroost.workspace.tree import (
    tree_contains_field,
)

CHOICE_TEMPLATE_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="decision",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="case",
    node_type=CatalogNodeType.VARIABLE,
)

CHECK_MARK = "✓"

NO_MARK = "-"


def make_display_fn(
    template,
):
    field_name = f"choice_template.{template.name}"

    def display_fn(
        row,
    ):
        tree = row.get(
            "_study",
            {},
        ).get(
            "scenario_families",
        )

        return (
            CHECK_MARK
            if tree_contains_field(
                tree,
                field_name,
            )
            else NO_MARK
        )

    return display_fn


def register_display_fields(
    reg,
):
    study_registry = build_study_registry()

    for template in study_registry.all_choice_templates():
        reg.register_display_field(
            DisplayField.field(
                f"choice_template.{template.name}",
                display_fn=make_display_fn(
                    template,
                ),
                description=template.description,
                profiles=template.profiles,
                **CHOICE_TEMPLATE_ONTOLOGY,
                defined_in=template.defined_in,
            )
        )
