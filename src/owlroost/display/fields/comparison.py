# src/owlroost/display/fields/comparison.py
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
from owlroost.core.utils import normalize_module_path

COMPARISON_DESIGN_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="design",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="comparative",
    materialization_level="run",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

COMPARISON_DECISION_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="decision",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="comparative",
    materialization_level="run",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Registration
# =========================================================


def register_display_fields(
    reg,
):
    """
    Register comparison display fields.
    """

    # =====================================================
    # Register comparison overrides here
    # =====================================================
