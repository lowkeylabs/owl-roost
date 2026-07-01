# src/owlroost/guide/providers/studies.py
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
            name="workspace.view",
            title="Review Workspace",
            description=("Inspect the initialized workspace."),
            command="roost workspace .",
            priority=40,
            requirements=[
                Requirement(
                    "context.workspace_initialized",
                    "==",
                    True,
                ),
            ],
        )
    )
