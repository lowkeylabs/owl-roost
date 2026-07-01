# src/owlroost/guide/providers/workspace.py
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

from owlroost.guide.specs import (
    Requirement,
    SuggestionSpec,
)


def register(
    reg,
):
    reg.register(
        SuggestionSpec(
            name="workspace.initialize",
            title="Initialize Workspace",
            description=("Create a planning workspace in the current directory."),
            command="roost workspace --init",
            priority=20,
            requirements=[
                Requirement(
                    "context.workspace_initialized",
                    "==",
                    False,
                ),
            ],
        )
    )
