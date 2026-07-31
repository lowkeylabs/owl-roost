# src/owlroost/workspace/builders.py
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

from datetime import datetime

from owlroost.workspace.specs import (
    HouseholdPlanningContext,
    WorkspacePlanningContext,
)


def build_household_planning_context(
    row,
):
    return HouseholdPlanningContext(
        name="default",
        title="Current Household",
        description="Household characterization is under development. See./workspace/builders.py",
    )


def build_workspace_planning_context(
    row,
):
    household = build_household_planning_context(
        row,
    )

    return WorkspacePlanningContext(
        workspace_name=row.get(
            "context.workspace.directory_name",
            ".",
        ),
        overview="Planning context generation is under development. See ./workspace/builders.py",
        generated_at=datetime.now(),
        households=(household,),
    )
