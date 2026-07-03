# src/owlroost/workspace/levers/context.py
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

from functools import cache
from io import StringIO
from pathlib import Path
from typing import Any, TypedDict

from owlplanner.config.plan_bridge import (
    config_to_plan,
)
from owlplanner.config.toml_io import (
    load_toml,
)

from owlroost.catalog.ontology import (
    ONTOLOGY_DIMENSIONS,
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

LEVER_ONTOLOGY: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="planning",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="context",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)


class FilesystemCharacterization(TypedDict):
    root: Path
    directory_name: str

    files: list[Path]
    directories: list[Path]

    case_files: list[Path]
    valid_case_files: list[Path]
    hfp_files: list[Path]

    workspace_initialized: bool
    workspace_parent_count: int
    workspace_child_count: int
    workspace_children: list[Path]


# =========================================================
# Helpers
# =========================================================


def _root(
    root=".",
) -> Path:
    return Path(root).resolve()


# =========================================================
# Case Validation
# =========================================================


@cache
def is_valid_case(
    filename: Path | None = None,
):
    """
    Determine whether an OWL case
    successfully loads.
    """

    if filename is None:
        return False

    try:
        s = StringIO()

        diconf, dirname, _ = load_toml(
            str(filename),
        )

        config_to_plan(
            diconf,
            dirname=dirname,
            logstreams=[s, s],
        )

        return True

    except Exception:
        return False


# =========================================================
# Filesystem Characterization
# =========================================================


@cache
def characterize_filesystem(
    root=".",
) -> FilesystemCharacterization:
    """
    Characterize the current planning
    context.

    The filesystem is intentionally
    traversed exactly once.

    Every context lever derives from
    this characterization.
    """

    root = _root(root)

    workspace_file = root / "workspace.toml"

    # -----------------------------------------------------
    # Immediate inventory
    # -----------------------------------------------------

    files = sorted(p for p in root.iterdir() if p.is_file())

    directories = sorted(p for p in root.iterdir() if p.is_dir())

    case_files = [
        p for p in files if (p.name.lower().startswith("c") and p.suffix.lower() == ".toml")
    ]

    valid_case_files = [p for p in case_files if is_valid_case(p)]

    hfp_files = [p for p in files if p.suffix.lower() == ".xlsx"]

    # -----------------------------------------------------
    # Parent workspace
    # -----------------------------------------------------

    parent_count = 0

    current = root.parent

    while current != current.parent:
        if (current / "workspace.toml").exists():
            parent_count += 1

        current = current.parent

    # -----------------------------------------------------
    # Immediate child workspaces
    # -----------------------------------------------------

    child_workspaces = [d for d in directories if (d / "workspace.toml").exists()]

    return FilesystemCharacterization(
        root=root,
        directory_name=root.name,
        files=files,
        directories=directories,
        case_files=case_files,
        valid_case_files=valid_case_files,
        hfp_files=hfp_files,
        workspace_initialized=workspace_file.exists(),
        workspace_parent_count=parent_count,
        workspace_child_count=len(
            child_workspaces,
        ),
        workspace_children=child_workspaces,
    )


# =========================================================
# Context Identity
# =========================================================


def directory_name(
    root=".",
):
    return characterize_filesystem(
        root,
    )["directory_name"]


# =========================================================
# Inventory
# =========================================================


def case_count(
    root=".",
):
    return len(
        characterize_filesystem(
            root,
        )["case_files"]
    )


def valid_case_count(
    root=".",
):
    return len(
        characterize_filesystem(
            root,
        )["valid_case_files"]
    )


def workspace_initialized(
    root=".",
):
    return characterize_filesystem(
        root,
    )["workspace_initialized"]


def workspace_parent_count(
    root=".",
):
    return characterize_filesystem(
        root,
    )["workspace_parent_count"]


def workspace_child_count(
    root=".",
):
    """
    Count immediate child
    workspaces.

    This intentionally does
    not recurse.
    """

    return characterize_filesystem(
        root,
    )["workspace_child_count"]


# =========================================================
# Workflow Readiness
# =========================================================


def has_valid_case(
    root=".",
):
    return (
        valid_case_count(
            root,
        )
        > 0
    )


def can_initialize_workspace(
    root=".",
):
    """
    Current directory satisfies all
    workspace initialization
    invariants.
    """

    fs = characterize_filesystem(
        root,
    )

    return (
        not fs["workspace_initialized"]
        and fs["workspace_parent_count"] == 0
        and fs["workspace_child_count"] == 0
    )


def can_create_workspace(
    root=".",
):
    """
    A child workspace may be created
    beneath this directory.
    """

    fs = characterize_filesystem(
        root,
    )

    return fs["workspace_parent_count"] == 0


# =========================================================
# Lever Definitions
# =========================================================

LEVERS = [
    # -----------------------------------------------------
    # Context identity
    # -----------------------------------------------------
    dict(
        name="directory_name",
        dtype=str,
        compute_fn=directory_name,
        description="Current planning context directory name.",
    ),
    # -----------------------------------------------------
    # Case inventory
    # -----------------------------------------------------
    dict(
        name="case_count",
        dtype=int,
        compute_fn=case_count,
        description="Count of OWL case files in the current planning context.",
    ),
    dict(
        name="valid_case_count",
        dtype=int,
        compute_fn=valid_case_count,
        description="Count of loadable OWL case files in the current planning context.",
    ),
    # -----------------------------------------------------
    # Workspace inventory
    # -----------------------------------------------------
    dict(
        name="workspace_initialized",
        dtype=bool,
        compute_fn=workspace_initialized,
        description="Current directory is an initialized workspace.",
    ),
    dict(
        name="workspace_parant_count",
        dtype=int,
        compute_fn=workspace_parent_count,
        description="Number of parent workspaces above current subdirectory.",
    ),
    dict(
        name="workspace_child_count",
        dtype=int,
        compute_fn=workspace_child_count,
        description="Number of immediate child workspaces.",
    ),
    # -----------------------------------------------------
    # Workflow readiness
    # -----------------------------------------------------
    dict(
        name="has_valid_case",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=has_valid_case,
        description="Planning context contains at least one valid OWL case.",
    ),
    dict(
        name="can_initialize_workspace",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=can_initialize_workspace,
        description="Current directory satisfies the requirements for workspace initialization.",
    ),
    dict(
        name="can_create_workspace",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=can_create_workspace,
        description="A new child workspace may be created beneath the current directory.",
    ),
]

# =========================================================
# Registration
# =========================================================


def make_compute_fn(fn):
    """
    Adapt a filesystem characterization
    function into a workspace lever.
    """

    return lambda row: fn(
        row["_path"],
    )


def register_levers(
    reg,
):
    """
    Register planning context levers.
    """

    for lever in LEVERS:
        ontology = dict(
            LEVER_ONTOLOGY,
        )

        for dimension in ONTOLOGY_DIMENSIONS:
            field = dimension.field_name

            if field in lever:
                ontology[field] = lever[field]

        reg.register(
            WorkspaceSpec(
                name=f"context.{lever['name']}",
                dtype=lever["dtype"],
                compute_fn=make_compute_fn(lever["compute_fn"]),
                description=lever["description"],
                **ontology,
            )
        )
