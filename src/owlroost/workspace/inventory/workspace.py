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
from owlroost.workspace.specs import (
    OverridePolicy,
    WorkspaceSpec,
)

# =========================================================
# Ontology
# =========================================================

WORKSPACE_VARIABLE: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="execution",
    value_origin="user-specified",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="workspace",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Inventory Definitions
# =========================================================


def compute_workspace_name(row):
    """
    Compute the workspace name.

    Returns
    -------
    str
        Workspace title.
    """
    title = row.get("_workspace", {}).get("definition", {}).get("name", None)
    if not title:
        title = row.get("_context", {}).get("workspace", {}).get("directory_name", "(undefined)")


def compute_workspace_overrides(row):
    """
    Compute the workspace overrides.

    Returns
    -------
    list[str]
        Workspace overrides.
    """
    overrides = row.get("_workspace", {}).get("definition", {}).get("overrides", [])
    try:
        overrides = [f"{line['key']}={line['value']}" for line in overrides]
    except Exception as e:
        #print(e)
        raise e
        pass
    return overrides


WORKSPACE_FIELDS: list[dict[str, Any]] = [
    dict(
        name="workspace.name",
        description="Name of workspace.",
        override_policy=OverridePolicy.REPLACE,
        default=compute_workspace_name,
    ),
    dict(
        name="workspace.overrides",
        description="Overrides for the workspace.",
        override_policy=OverridePolicy.REPLACE,
        default=compute_workspace_overrides,
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

    for field in WORKSPACE_FIELDS:
        default = field["default"]

        #
        # Convert the declared default into
        # a compute function.
        #
        if callable(default):
            compute_fn = default

        else:

            def compute_fn(
                row,
                value=default,
            ):
                return value

        reg.register(
            WorkspaceSpec(
                name=field["name"],
                dtype=str,
                compute_fn=compute_fn,
                override_policy=field.get(
                    "override_policy",
                    OverridePolicy.REPLACE,
                ),
                description=field["description"],
                **WORKSPACE_VARIABLE,
            )
        )
