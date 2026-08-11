# src/owlroost/workspace/levers/context.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning context semantic levers.

## Notes

Defines semantic observations describing
the current planning context.

These observations characterize:

* filesystem inventory
* workspace state
* planning artifacts
* workflow readiness
* configured workspace paths

Workspace configuration is loaded and
composed by workspace.loaders.

Configuration defaults are defined
exclusively by the packaged workspace.toml
template. This module interprets effective
configuration but does not define
configuration defaults.

Household Library configuration is owned
by workspace.toml, but interpretation of
that configuration belongs to the
household subsystem.

## Architectural Invariants

WorkspaceSpec describes stable semantic
observations.

Dynamic workspace configuration is
provided through:

    row["_workspace"]["definition"]

Compute functions explicitly consume
configuration when required.

The workspace registry and materializers
do not implement configuration override
policy.

Household Library resolution does not
belong here. The household subsystem
interprets:

    context.households

from the effective workspace definition
and constructs HouseholdLibrarySpec
objects.
"""

from __future__ import annotations

from enum import StrEnum
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
    defined_in=normalize_module_path(
        __file__,
    ),
)


# =========================================================
# Directory Characterization
# =========================================================


class DirectoryKind(StrEnum):
    """
    Semantic characterization of the
    current directory.

    This classification is independent
    of workflow recommendations.

    It answers:

        "What kind of directory is this?"
    """

    EMPTY = "empty"

    PLANNING = "planning"

    WORKSPACE = "workspace"

    MIXED = "mixed"

    FOREIGN = "foreign"


# =========================================================
# File System Inventory
# =========================================================


class FilesystemInventory(TypedDict):
    """
    Direct observations gathered from one
    filesystem location.

    Inventory contains no interpretation.
    """

    # =====================================================
    # Identity
    # =====================================================

    root: Path

    directory_name: str

    # =====================================================
    # Inventory
    # =====================================================

    files: list[Path]

    directories: list[Path]

    case_files: list[Path]

    valid_case_files: list[Path]

    hfp_files: list[Path]

    # =====================================================
    # Workspace Inventory
    # =====================================================

    workspace_initialized: bool

    workspace_parent_count: int

    workspace_child_count: int

    workspace_children: list[Path]


# =========================================================
# File System Characterization
# =========================================================


class FilesystemCharacterization(
    FilesystemInventory,
):
    """
    Semantic interpretation of a
    filesystem inventory.

    Characterization adds meaning and
    workflow readiness to the observed
    inventory.
    """

    # =====================================================
    # Characterization
    # =====================================================

    directory_kind: DirectoryKind

    # =====================================================
    # Workflow Readiness
    # =====================================================

    can_initialize_workspace: bool

    can_create_workspace: bool

    has_results: bool


# =========================================================
# Helpers
# =========================================================


def _root(
    root=".",
) -> Path:
    """
    Resolve a planning context root.
    """

    return Path(
        root,
    ).resolve()


def _workspace_definition(
    row,
):
    """
    Return the effective workspace
    configuration attached to a row.

    The definition has already been
    composed by workspace.loaders from
    canonical template defaults and
    local workspace overrides.

    A planning context that is not an
    initialized workspace has no
    workspace definition.
    """

    return row.get(
        "_workspace",
        {},
    ).get(
        "definition",
        {},
    )


def _configuration_value(
    definition,
    path: tuple[str, ...],
):
    """
    Resolve a value from the effective
    workspace definition.

    Parameters
    ----------
    definition
        Effective workspace definition.

    path
        Nested configuration path.

    Returns
    -------
    object
        Configured value.

    Raises
    ------
    KeyError
        Configuration path does not
        exist.
    """

    value = definition

    for key in path:
        value = value[key]

    return value


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
        stream = StringIO()

        diconf, dirname, _ = load_toml(
            str(
                filename,
            ),
        )

        config_to_plan(
            diconf,
            dirname=dirname,
            logstreams=[
                stream,
                stream,
            ],
        )

        return True

    except Exception:
        return False


# =========================================================
# Planning Artifacts
# =========================================================


def is_planning_artifact(
    path: Path,
) -> bool:
    """
    Determine whether a filesystem entry
    naturally belongs within a ROOST
    planning directory.

    Planning artifacts include inputs,
    documentation, generated reports,
    Quarto support files, and workspace
    metadata.
    """

    name = path.name

    # -----------------------------------------------------
    # Hidden support directories
    # -----------------------------------------------------

    if path.is_dir():
        return name in {
            ".quarto",
            "cases",
            "library",
            "studies",
            "results",
            "reports",
            "docs",
        }

    # -----------------------------------------------------
    # Workspace metadata
    # -----------------------------------------------------

    if name in {
        "workspace.toml",
        "study.toml",
        "_quarto.yml",
        "_variables.yml",
        "README.md",
    }:
        return True

    # -----------------------------------------------------
    # Quarto documents
    # -----------------------------------------------------

    if path.suffix.lower() == ".qmd":
        return True

    # -----------------------------------------------------
    # Makefiles
    # -----------------------------------------------------

    if name == "Makefile" or name.startswith("makefile"):
        return True

    # -----------------------------------------------------
    # Case definitions
    # -----------------------------------------------------

    if path.suffix.lower() == ".toml" and name.lower().startswith("case"):
        return True

    # -----------------------------------------------------
    # Household Financial Profile
    # -----------------------------------------------------

    if path.suffix.lower() == ".xlsx" and name.lower().startswith("hfp"):
        return True

    return False


# =========================================================
# Directory Characterization
# =========================================================


def characterize_directory_kind(
    fs: FilesystemInventory,
) -> DirectoryKind:
    """
    Classify the semantic purpose of the
    current directory.

    The classification intentionally
    describes what the directory is,
    rather than recommending any
    particular workflow.
    """

    # -----------------------------------------------------
    # Already initialized
    # -----------------------------------------------------

    if fs["workspace_initialized"]:
        return DirectoryKind.WORKSPACE

    # -----------------------------------------------------
    # Empty
    # -----------------------------------------------------

    if not fs["files"] and not fs["directories"]:
        return DirectoryKind.EMPTY

    planning = 0
    foreign = 0

    # -----------------------------------------------------
    # Count recognized artifacts
    # -----------------------------------------------------

    for path in fs["files"] + fs["directories"]:
        if is_planning_artifact(
            path,
        ):
            planning += 1

        else:
            foreign += 1

    # -----------------------------------------------------
    # Entirely planning content
    # -----------------------------------------------------

    if planning > 0 and foreign == 0:
        return DirectoryKind.PLANNING

    # -----------------------------------------------------
    # Mixture of planning and unrelated content
    # -----------------------------------------------------

    if planning > 0 and foreign > 0:
        return DirectoryKind.MIXED

    # -----------------------------------------------------
    # Nothing recognizable
    # -----------------------------------------------------

    return DirectoryKind.FOREIGN


# =========================================================
# Workflow Readiness
# =========================================================


def characterize_can_initialize_workspace(
    inventory: FilesystemInventory,
    directory_kind: DirectoryKind,
) -> bool:
    """
    Determine whether the current
    directory can be initialized as a
    workspace.
    """

    if inventory["workspace_initialized"]:
        return False

    if inventory["workspace_parent_count"] > 0:
        return False

    if inventory["workspace_child_count"] > 0:
        return False

    return directory_kind in {
        DirectoryKind.EMPTY,
        DirectoryKind.PLANNING,
    }


def characterize_can_create_workspace(
    inventory: FilesystemInventory,
) -> bool:
    """
    Determine whether a child workspace
    may be created beneath the current
    planning context.
    """

    return inventory["workspace_parent_count"] == 0


# =========================================================
# Filesystem Inventory
# =========================================================


@cache
def inventory_filesystem(
    root=".",
) -> FilesystemInventory:
    """
    Collect direct observations about one
    filesystem location.

    Inventory intentionally performs no
    semantic interpretation.

    It gathers only observable facts.
    """

    root = _root(
        root,
    )

    workspace_file = root / "workspace.toml"

    # -----------------------------------------------------
    # Immediate inventory
    # -----------------------------------------------------

    files = sorted(path for path in root.iterdir() if path.is_file())

    directories = sorted(path for path in root.iterdir() if path.is_dir())

    case_files = [
        path
        for path in files
        if (path.name.lower().startswith("c") and path.suffix.lower() == ".toml")
    ]

    valid_case_files = [
        path
        for path in case_files
        if is_valid_case(
            path,
        )
    ]

    hfp_files = [path for path in files if path.suffix.lower() == ".xlsx"]

    # -----------------------------------------------------
    # Parent workspaces
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

    child_workspaces = [
        directory for directory in directories if (directory / "workspace.toml").exists()
    ]

    # -----------------------------------------------------
    # Inventory
    # -----------------------------------------------------

    return FilesystemInventory(
        root=root,
        directory_name=root.name,
        files=files,
        directories=directories,
        case_files=case_files,
        valid_case_files=valid_case_files,
        hfp_files=hfp_files,
        workspace_initialized=(workspace_file.exists()),
        workspace_parent_count=(parent_count),
        workspace_child_count=len(
            child_workspaces,
        ),
        workspace_children=(child_workspaces),
    )


# =========================================================
# Filesystem Characterization
# =========================================================


@cache
def characterize_filesystem(
    root=".",
) -> FilesystemCharacterization:
    """
    Characterize the filesystem state of
    a planning context.
    """

    inventory = inventory_filesystem(
        root,
    )

    directory_kind = characterize_directory_kind(
        inventory,
    )

    return FilesystemCharacterization(
        **inventory,
        directory_kind=directory_kind,
        can_initialize_workspace=(
            characterize_can_initialize_workspace(
                inventory,
                directory_kind,
            )
        ),
        can_create_workspace=(
            characterize_can_create_workspace(
                inventory,
            )
        ),
    )


# =========================================================
# Context Identity
# =========================================================


def directory_name(
    root=".",
):
    """
    Return the current planning context
    directory name.
    """

    return characterize_filesystem(
        root,
    )["directory_name"]


# =========================================================
# Inventory
# =========================================================


def case_count(
    root=".",
):
    """
    Count OWL case files.
    """

    return len(
        characterize_filesystem(
            root,
        )["case_files"]
    )


def valid_case_count(
    root=".",
):
    """
    Count loadable OWL case files.
    """

    return len(
        characterize_filesystem(
            root,
        )["valid_case_files"]
    )


def workspace_initialized(
    root=".",
):
    """
    Return whether the current directory
    is an initialized workspace.
    """

    return characterize_filesystem(
        root,
    )["workspace_initialized"]


def workspace_parent_count(
    root=".",
):
    """
    Count parent workspaces.
    """

    return characterize_filesystem(
        root,
    )["workspace_parent_count"]


def workspace_child_count(
    root=".",
):
    """
    Count immediate child workspaces.

    This intentionally does not recurse.
    """

    return characterize_filesystem(
        root,
    )["workspace_child_count"]


# =========================================================
# Configured Semantic Values
# =========================================================


def context_results_path(
    root,
    value: str,
) -> Path:
    """
    Resolve the configured results
    directory relative to the planning
    context root.
    """

    path = Path(
        value,
    ).expanduser()

    if not path.is_absolute():
        path = _root(root) / path

    return path.resolve()


def context_cases_path(
    root,
    value: str,
) -> Path:
    """
    Resolve the configured case directory
    relative to the planning context root.
    """

    path = Path(
        value,
    ).expanduser()

    if not path.is_absolute():
        path = _root(root) / path

    return path.resolve()


def context_workspace_path(
    root=".",
) -> Path:
    """
    Return the absolute planning context
    root.
    """

    return _root(
        root,
    )


# =========================================================
# Workflow Readiness
# =========================================================


def has_valid_case(
    root=".",
):
    """
    Return whether the planning context
    contains at least one valid case.
    """

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
    Return whether the current directory
    may be initialized as a workspace.
    """

    return characterize_filesystem(
        root,
    )["can_initialize_workspace"]


def can_create_workspace(
    root=".",
):
    """
    Return whether a child workspace may
    be created.
    """

    return characterize_filesystem(
        root,
    )["can_create_workspace"]


def directory_kind(
    root=".",
):
    """
    Return the semantic directory
    classification.
    """

    return characterize_filesystem(
        root,
    )["directory_kind"]


# =========================================================
# Lever Definitions
# =========================================================


LEVERS = [
    # -----------------------------------------------------
    # Context identity
    # -----------------------------------------------------
    dict(
        name="workspace.directory_name",
        dtype=str,
        compute_fn=directory_name,
        description=("Current planning context directory name."),
    ),
    # -----------------------------------------------------
    # Case inventory
    # -----------------------------------------------------
    dict(
        name="workspace.case_count",
        dtype=int,
        compute_fn=case_count,
        description=("Count of OWL case files in the current planning context."),
    ),
    dict(
        name="workspace.valid_case_count",
        dtype=int,
        compute_fn=valid_case_count,
        description=("Count of loadable OWL case files in the current planning context."),
    ),
    # -----------------------------------------------------
    # Workspace inventory
    # -----------------------------------------------------
    dict(
        name="workspace.initialized",
        dtype=bool,
        compute_fn=workspace_initialized,
        description=("Current directory is an initialized workspace."),
    ),
    dict(
        name="workspace.parent_count",
        dtype=int,
        compute_fn=workspace_parent_count,
        description=("Number of parent workspaces above current subdirectory."),
    ),
    dict(
        name="workspace.child_count",
        dtype=int,
        compute_fn=workspace_child_count,
        description=("Number of immediate child workspaces."),
    ),
    # -----------------------------------------------------
    # Workflow readiness
    # -----------------------------------------------------
    dict(
        name="has_valid_case",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=has_valid_case,
        description=("Planning context contains at least one valid OWL case."),
    ),
    dict(
        name="can_initialize_workspace",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=can_initialize_workspace,
        description=("Current directory satisfies the requirements for workspace initialization."),
    ),
    dict(
        name="can_create_workspace",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=can_create_workspace,
        description=("A new child workspace may be created beneath the current directory."),
    ),
    dict(
        name="workspace.directory_kind",
        dtype=str,
        compute_fn=directory_kind,
        description=("Semantic classification of the current directory."),
    ),
    # -----------------------------------------------------
    # Paths
    # -----------------------------------------------------
    dict(
        name="paths.workspace",
        dtype=Path,
        compute_fn=context_workspace_path,
        description=("Absolute path to the current planning context root."),
    ),
    dict(
        name="paths.cases",
        dtype=Path,
        compute_fn=context_cases_path,
        config_path=(
            "context",
            "paths",
            "cases",
        ),
        description=("Absolute path to the directory containing household case files."),
    ),
    dict(
        name="paths.results",
        dtype=Path,
        compute_fn=context_results_path,
        config_path=(
            "context",
            "paths",
            "results",
        ),
        description=("Absolute path to the directory used for generated planning results."),
    ),
]


# =========================================================
# Registration
# =========================================================


def make_compute_fn(
    fn,
    config_path=None,
):
    """
    Adapt a context computation to the
    WorkspaceSpec row interface.

    Computations without a configuration
    path receive only the planning context
    root.

    Configured computations receive the
    effective value supplied by the nested
    workspace.toml definition.
    """

    def compute(
        row,
    ):
        root = row["_path"]

        if config_path is None:
            return fn(
                root,
            )

        definition = _workspace_definition(
            row,
        )

        value = _configuration_value(
            definition,
            config_path,
        )

        return fn(
            root,
            value,
        )

    return compute


def register_levers(
    reg,
):
    """
    Register planning context semantic
    observations.
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
                name=(f"context.{lever['name']}"),
                dtype=lever["dtype"],
                compute_fn=make_compute_fn(
                    lever["compute_fn"],
                    lever.get(
                        "config_path",
                    ),
                ),
                description=lever["description"],
                **ontology,
            )
        )
