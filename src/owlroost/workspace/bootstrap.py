# src/owlroost/workspace/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace semantic registry bootstrap.

Notes
-----
Constructs the canonical WorkspaceRegistry
used by ROOST.

The registry contains stable semantic
workspace observations contributed by
workspace inventory and lever subsystems.

Dynamic workspace configuration is not
registered here. It is defined by the
workspace.toml template and composed by
workspace loaders.
"""

from __future__ import annotations

from owlroost.workspace.inventory import (
    register_inventory,
)
from owlroost.workspace.levers import (
    register_all_levers,
)
from owlroost.workspace.registry import (
    WorkspaceRegistry,
)


def build_workspace_registry():
    """
    Construct the canonical
    WorkspaceRegistry.
    """

    registry = WorkspaceRegistry()

    register_inventory(
        registry,
    )

    register_all_levers(
        registry,
    )

    return registry
