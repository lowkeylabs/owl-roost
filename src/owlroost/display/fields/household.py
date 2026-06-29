# src/owlroost/display/fields/household.py
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

HOUSEHOLD_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="household",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="catalog",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)


def register_display_fields(
    reg,
):
    fields = [
        (
            "id",
            "Household identifier.",
        ),
        (
            "title",
            "Household title.",
        ),
        (
            "description",
            "Household description.",
        ),
        (
            "tags",
            "Household tags.",
        ),
        (
            "root",
            "Household project directory.",
        ),
        (
            "artifact_count",
            "Number of files contained in the household project.",
        ),
        (
            "artifact_names",
            "Household project artifacts.",
        ),
    ]

    for name, description in fields:
        reg.register_display_field(
            DisplayField.field(
                name,
                description=description,
                **HOUSEHOLD_ONTOLOGY,
            )
        )
