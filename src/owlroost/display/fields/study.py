# src/owlroost/display/fields/study.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study display field registration.

Notes
-----
Registers the canonical Study and
Experiment display fields.

Architectural Invariants
------------------------

This module owns display registration
only.

The canonical study field definitions
are owned by ``study.specs``.
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
from owlroost.study.specs import (
    EXPERIMENT_FIELDS,
    STUDY_FIELDS,
    experiment_field_name,
    study_field_name,
)

STUDY_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="study",
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
    Register canonical Study and
    Experiment display fields.
    """

    # -----------------------------------------------------
    # Study fields
    # -----------------------------------------------------

    for field in STUDY_FIELDS:
        reg.register_display_field(
            DisplayField.field(
                study_field_name(
                    field.name,
                ),
                description=field.description,
                **STUDY_ONTOLOGY,
            )
        )

    # -----------------------------------------------------
    # Experiment fields
    # -----------------------------------------------------

    for field in EXPERIMENT_FIELDS:
        reg.register_display_field(
            DisplayField.field(
                experiment_field_name(
                    field.name,
                ),
                description=field.description,
                **STUDY_ONTOLOGY,
            )
        )
