# src/owlroost/display/fields/household.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household display field registration.

Notes
-----
Registers the canonical Household
display fields.

Architectural Invariants
------------------------

This module owns display registration
only.

The canonical household field
definitions are owned by
``household.specs``.
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
from owlroost.household.specs import (
    HOUSEHOLD_FIELDS,
    household_field_name,
)

HOUSEHOLD_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="planning",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="catalog",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)


def register_display_fields(
    reg,
) -> None:
    """
    Register canonical Household
    display fields.
    """

    for field in HOUSEHOLD_FIELDS:
        reg.register_display_field(
            DisplayField.field(
                household_field_name(
                    field.name,
                ),
                description=field.description,
                **HOUSEHOLD_ONTOLOGY,
            )
        )
