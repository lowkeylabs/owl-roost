# src/owlroost/comparison/plugins/overrides.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Override comparison observations.

Notes
-----
Registers comparison observations describing
shared and differing Hydra overrides across
comparison scopes.

Values materialize into:

    row["_comparison"]

Examples
--------

    comparison.session.common_overrides

    comparison.session.run_specific_overrides

    comparison.working_set.common_overrides

    comparison.working_set.run_specific_overrides
"""

from __future__ import annotations

from typing import Any

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.comparison.specs import (
    ComparisonSpec,
)
from owlroost.core.utils import (
    normalize_module_path,
)

# =========================================================
# Ontology
# =========================================================

COMPARISON_VARIABLE: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="design",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="comparative",
    materialization_level="comparison",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Lookup Helper
# =========================================================


def comparison_lookup(
    path: str,
):
    """
    Build comparison lookup function.

    Example
    -------

        comparison_lookup(
            "session.common_overrides"
        )

    resolves:

        row["_comparison"]
            ["session"]
            ["common_overrides"]
    """

    parts = path.split(".")

    def compute(
        row,
    ):
        current = row.get(
            "_comparison",
            {},
        )

        for part in parts:
            if not isinstance(
                current,
                dict,
            ):
                return None

            current = current.get(
                part,
            )

            if current is None:
                return None

        return current

    return compute


# =========================================================
# Definitions
# =========================================================

COMPARISON_FIELDS = [
    (
        "comparison.session.common_overrides",
        "session.common_overrides",
        dict,
        ("Overrides shared across all runs within the session comparison group."),
    ),
    (
        "comparison.session.run_specific_overrides",
        "session.run_specific_overrides",
        dict,
        ("Overrides unique to this run within the session comparison group."),
    ),
    (
        "comparison.working_set.common_overrides",
        "working_set.common_overrides",
        dict,
        ("Overrides shared across all visible rows in the current working set."),
    ),
    (
        "comparison.working_set.run_specific_overrides",
        "working_set.run_specific_overrides",
        dict,
        ("Overrides unique to this run within the current working set."),
    ),
    (
        "comparison.session.group_row_ids",
        "session.group_row_ids",
        list,
        ("Row identifiers participating in the session comparison group."),
    ),
    (
        "comparison.working_set.group_row_ids",
        "working_set.group_row_ids",
        list,
        ("Row identifiers participating in the working-set comparison group."),
    ),
]

# =========================================================
# Registration
# =========================================================


def register_comparison_fields(
    reg,
):
    """
    Register override comparison observations.
    """

    for (
        name,
        lookup_path,
        dtype,
        description,
    ) in COMPARISON_FIELDS:
        reg.register(
            ComparisonSpec(
                name=name,
                dtype=dtype,
                compute_fn=comparison_lookup(
                    lookup_path,
                ),
                description=description,
                **COMPARISON_VARIABLE,
            )
        )
