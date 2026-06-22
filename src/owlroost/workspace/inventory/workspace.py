# src/owlroost/workspace/inventory/workspace.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace identity inventory.

Notes
-----
Registers canonical inventory observations
describing the workspace itself.

These observations represent:

    - workspace identity
    - workspace documentation
    - workspace filesystem layout

rather than realized analytical content.

Architectural Invariant
-----------------------
Inventory-backed workspace metrics are
materialized directly from the corresponding
path within:

    row["_workspace"]

The metric name therefore serves as the
canonical inventory path.
"""

from __future__ import annotations

from typing import Any

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.workspace.materializers import (
    workspace_lookup,
)
from owlroost.workspace.specs import (
    WorkspaceSpec,
)

# =========================================================
# Ontology
# =========================================================

WORKSPACE_VARIABLE: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="execution",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="workspace",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Inventory Definitions
# =========================================================

WORKSPACE_FIELDS: list[tuple[str, str]] = [
    (
        "workspace.name",
        "Workspace name.",
    ),
    (
        "workspace.title",
        "Workspace title.",
    ),
    (
        "workspace.description",
        "Workspace description.",
    ),
    (
        "workspace.paths.workspace",
        "Absolute path to the workspace.",
    ),
    (
        "workspace.paths.cases",
        "Absolute path to the cases directory.",
    ),
    (
        "workspace.paths.results",
        "Absolute path to the results directory.",
    ),
]

# =========================================================
# Registration
# =========================================================


def register_inventory(
    reg,
):
    """
    Register workspace identity
    observations.
    """

    for name, description in WORKSPACE_FIELDS:
        reg.register(
            WorkspaceSpec(
                name=name,
                dtype=str,
                compute_fn=workspace_lookup(
                    name,
                ),
                description=description,
                **WORKSPACE_VARIABLE,
            )
        )
