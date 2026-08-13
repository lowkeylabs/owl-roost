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

    * workspace identity
    * workspace documentation
    * workspace filesystem layout

rather than realized analytical content.

Workspace configuration is loaded and
composed by workspace.loaders.

Configuration defaults are defined
exclusively by the packaged workspace.toml
template. This module interprets effective
configuration but does not define
configuration defaults.

Architectural Invariant
-----------------------
Inventory-backed workspace observations are
materialized directly from the effective
workspace definition or other already
materialized semantic state.

Dynamic workspace configuration is not
represented in WorkspaceSpec metadata.
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
    defined_in=normalize_module_path(
        __file__,
    ),
)


# =========================================================
# Helpers
# =========================================================


def _workspace_definition(
    row,
):
    """
    Return the effective workspace
    definition.

    The definition has already been
    composed by workspace.loaders from:

        packaged workspace.toml defaults
        +
        local workspace.toml overrides
    """

    return row.get(
        "_workspace",
        {},
    ).get(
        "definition",
        {},
    )


# =========================================================
# Inventory Computation
# =========================================================


def compute_workspace_name(
    row,
):
    """
    Compute the semantic workspace name.

    Workspace identity is derived from
    the planning-context directory name.

    The directory name is a semantic
    filesystem observation rather than
    workspace configuration.
    """

    return (
        row.get(
            "_context",
            {},
        )
        .get(
            "workspace",
            {},
        )
        .get(
            "directory_name",
            "(undefined)",
        )
    )


def compute_workspace_overrides(
    row,
):
    """
    Compute the workspace overrides.

    Workspace overrides are stored in the
    effective workspace definition as
    key=value strings.

    Returns
    -------
    list[str]
        Workspace overrides in configured
        order.
    """

    definition = _workspace_definition(
        row,
    )

    return list(definition["workspace"]["overrides"])


# =========================================================
# Inventory Definitions
# =========================================================


WORKSPACE_FIELDS: list[dict[str, Any]] = [
    dict(
        name="workspace.name",
        dtype=str,
        description="Name of workspace.",
        compute_fn=compute_workspace_name,
    ),
    dict(
        name="workspace.overrides",
        dtype=list[str],
        description="Overrides for the workspace.",
        compute_fn=compute_workspace_overrides,
    ),
]


# =========================================================
# Registration
# =========================================================


def register_inventory(
    reg,
):
    """
    Register canonical workspace
    inventory observations.
    """

    for field in WORKSPACE_FIELDS:
        reg.register(
            WorkspaceSpec(
                name=field["name"],
                dtype=field["dtype"],
                compute_fn=field["compute_fn"],
                description=field["description"],
                **WORKSPACE_VARIABLE,
            )
        )
