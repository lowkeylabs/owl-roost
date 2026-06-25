# src/owlroost/workspace/bootstrap.py
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

from owlroost.workspace.inventory import (
    register_inventory,
)
from owlroost.workspace.levers import register_all_levers
from owlroost.workspace.registry import (
    WorkspaceRegistry,
)


def build_workspace_registry():
    """
    Construct WorkspaceRegistry.
    """

    reg = WorkspaceRegistry()

    register_inventory(
        reg,
    )

    register_all_levers(reg)

    return reg
