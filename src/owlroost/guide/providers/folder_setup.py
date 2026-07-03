# src/owlroost/guide/providers/folder_setup.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning context workflow guides.

Notes
-----
Registers the workflow guides that
describe how a user progresses from an
empty planning context toward an
initialized ROOST workspace.

Each guide consumes semantic variables
already materialized by the workspace
subsystem.

Provider discovery automatically imports
this module and invokes:

    register(reg)
"""

from __future__ import annotations

from typing import Any

from owlroost.catalog.ontology import (
    ONTOLOGY_DIMENSIONS,
    CatalogNodeType,
)
from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.guide.specs import (
    GuideSpec,
    Requirement,
)

# =========================================================
# Ontology
# =========================================================

GUIDE_ONTOLOGY: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="planning",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="context",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Workflow Guides
# =========================================================

TRANSFORMS = [
    # -----------------------------------------------------
    # Always available
    # -----------------------------------------------------
    dict(
        name="current.context",
        title="Where am I?",
        description="Display the current planning context.",
        command="roost .",
        priority=10,
    ),
    # -----------------------------------------------------
    # Directory preparation
    # -----------------------------------------------------
    dict(
        name="folder.create",
        title="Create New Folder",
        description=("Create an empty directory before starting a new ROOST workspace."),
        command="mkdir my-study",
        priority=20,
        requirements=[
            Requirement(
                "context.workspace_suitable",
                "==",
                False,
            ),
        ],
    ),
    dict(
        name="folder.change",
        title="Change Into New Folder",
        description=("Move into the newly created directory before initializing a workspace."),
        command="cd my-study",
        priority=21,
        requirements=[
            Requirement(
                "context.workspace_suitable",
                "==",
                False,
            ),
        ],
    ),
    # -----------------------------------------------------
    # Workspace lifecycle
    # -----------------------------------------------------
    dict(
        name="workspace.initialize",
        title="Initialize Workspace",
        description=("Create a planning workspace in the current directory."),
        command="roost workspace --init",
        priority=30,
        requirements=[
            Requirement(
                "context.workspace_initialized",
                "==",
                False,
            ),
            Requirement(
                "context.workspace_parent_count",
                "==",
                0,
            ),
            Requirement(
                "context.workspace_child_count",
                "==",
                0,
            ),
            Requirement(
                "context.directory_kind",
                "in",
                [
                    "empty",
                    "planning",
                ],
            ),
        ],
    ),
    dict(
        name="workspace.view",
        title="Review Workspace",
        description="Inspect the initialized workspace.",
        command="roost workspace .",
        priority=40,
        requirements=[
            Requirement(
                "context.workspace_initialized",
                "==",
                True,
            ),
        ],
    ),
    # -----------------------------------------------------
    # Case workflow
    # -----------------------------------------------------
    dict(
        name="cases.review",
        title="Review Cases",
        description="Review available planning cases.",
        command="roost cases",
        priority=50,
        requirements=[
            Requirement(
                "context.valid_case_count",
                ">",
                0,
            ),
        ],
    ),
]

# =========================================================
# Registration
# =========================================================


def register(
    reg,
):
    """
    Register planning workflow guides.
    """

    for transform in TRANSFORMS:
        ontology = dict(
            GUIDE_ONTOLOGY,
        )

        for dimension in ONTOLOGY_DIMENSIONS:
            field = dimension.field_name

            if field in transform:
                ontology[field] = transform[field]

        reg.register(
            GuideSpec(
                **transform,
                **ontology,
            )
        )
