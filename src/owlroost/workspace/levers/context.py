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
from owlroost.household.households import (
    BUILTIN_HOUSEHOLD_LIBRARY,
)
from owlroost.household.specs import HouseholdLibrarySpec
from owlroost.workspace.specs import (
    OverridePolicy,
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


# =========================================================
# Helpers
# =========================================================


def _root(
    root=".",
) -> Path:
    return Path(root).resolve()


# =========================================================
# Household Libraries
# =========================================================

DEFAULT_HOUSEHOLD_LIBRARY_CONFIG = (
    ("workspace", "./library/households"),
    ("user", "~/.roost/households"),
    ("builtin", "<builtin>"),
)


def default_household_library_config() -> list[tuple[str, str]]:
    """
    Return the canonical household
    library configuration used to
    initialize new workspaces.

    Returns
    -------
    list[tuple[str, str]]
        Ordered pairs of
        (library_name, location).
    """

    return list(
        DEFAULT_HOUSEHOLD_LIBRARY_CONFIG,
    )


def resolve_household_libraries(
    values: list[tuple[str, str]],
    root=".",
) -> list[HouseholdLibrarySpec]:
    """
    Resolve configured household
    library definitions into
    HouseholdLibrarySpec objects.

    Parameters
    ----------
    values
        Ordered household library
        configuration.

    root
        Planning context root.

    Returns
    -------
    list[HouseholdLibrarySpec]
    """

    root = _root(
        root,
    )

    libraries: list[HouseholdLibrarySpec] = []

    for name, location in values:
        read_only = False

        if location == "<builtin>":
            library_root = BUILTIN_HOUSEHOLD_LIBRARY
            read_only = True

        elif location.startswith(
            "~/",
        ):
            library_root = Path(
                location,
            ).expanduser()

        else:
            library_root = (root / location).resolve()

        libraries.append(
            HouseholdLibrarySpec(
                name=name,
                root=library_root,
                read_only=read_only,
            )
        )

    return libraries


def default_household_libraries(
    root=".",
) -> list[HouseholdLibrarySpec]:
    """
    Return the canonical household
    libraries for the current
    planning context.

    Parameters
    ----------
    root
        Planning context root.

    Returns
    -------
    list[HouseholdLibrarySpec]
    """

    return resolve_household_libraries(
        default_household_library_config(),
        root,
    )


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

    #
    # Hidden support directories.
    #
    if path.is_dir():
        return name in {
            ".quarto",
            "cases",
            "studies",
            "results",
            "reports",
            "docs",
        }

    #
    # Workspace metadata.
    #
    if name in {
        "workspace.toml",
        "study.toml",
        "_quarto.yml",
        "_variables.yml",
        "README.md",
    }:
        return True

    #
    # Quarto documents.
    #
    if path.suffix.lower() == ".qmd":
        return True

    #
    # Makefiles.
    #
    if name == "Makefile" or name.startswith("makefile"):
        return True

    #
    # Case definitions.
    #
    if path.suffix.lower() == ".toml" and name.lower().startswith("case"):
        return True

    #
    # Household Financial Profile.
    #
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

    #
    # Already initialized.
    #
    if fs["workspace_initialized"]:
        return DirectoryKind.WORKSPACE

    #
    # Empty.
    #
    if not fs["files"] and not fs["directories"]:
        return DirectoryKind.EMPTY

    planning = 0
    foreign = 0

    #
    # Count recognized artifacts.
    #
    for path in fs["files"] + fs["directories"]:
        if is_planning_artifact(
            path,
        ):
            planning += 1
        else:
            foreign += 1

    #
    # Entirely planning content.
    #
    if planning > 0 and foreign == 0:
        return DirectoryKind.PLANNING

    #
    # Mixture of planning and
    # unrelated content.
    #
    if planning > 0 and foreign > 0:
        return DirectoryKind.MIXED

    #
    # Nothing recognizable as a
    # planning directory.
    #
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

    files = sorted(p for p in root.iterdir() if p.is_file())

    directories = sorted(p for p in root.iterdir() if p.is_dir())

    case_files = [
        p for p in files if (p.name.lower().startswith("c") and p.suffix.lower() == ".toml")
    ]

    valid_case_files = [
        p
        for p in case_files
        if is_valid_case(
            p,
        )
    ]

    hfp_files = [p for p in files if p.suffix.lower() == ".xlsx"]

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

    child_workspaces = [d for d in directories if (d / "workspace.toml").exists()]

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
        workspace_initialized=workspace_file.exists(),
        workspace_parent_count=parent_count,
        workspace_child_count=len(
            child_workspaces,
        ),
        workspace_children=child_workspaces,
    )


# =========================================================
# Filesystem Characterization
# =========================================================


@cache
def characterize_filesystem(
    root=".",
) -> FilesystemCharacterization:
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


def context_name(
    root=".",
    value: str | None = None,
) -> str:
    if value is None:
        value = _root(root).name

    return value


def context_title(
    root=".",
    value: str | None = None,
) -> str:
    if value is None:
        value = _root(root).name

    return value


def context_description(
    root=".",
    value: str | None = None,
) -> str:
    if value is None:
        value = _root(root).name

    return value


def context_results_path(
    root=".",
    value: str | None = None,
) -> Path:
    if value is None:
        value = "./results"

    return (_root(root) / value).resolve()


def context_cases_path(
    root=".",
    value: str | None = None,
) -> Path:
    if value is None:
        value = "."

    return (_root(root) / value).resolve()


def context_workspace_path(
    root=".",
) -> Path:
    return _root(root)


# =========================================================
# Search Paths
# =========================================================


def household_libraries(
    root=".",
    values: list[tuple[str, str]] | None = None,
) -> list[HouseholdLibrarySpec]:
    """
    Return the effective household
    libraries for the current planning
    context.
    """

    if values is None:
        values = default_household_library_config()

    return resolve_household_libraries(
        values,
        root,
    )


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
    return characterize_filesystem(
        root,
    )["can_initialize_workspace"]


def can_create_workspace(
    root=".",
):
    return characterize_filesystem(
        root,
    )["can_create_workspace"]


def directory_kind(
    root=".",
):
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
        description="Current planning context directory name.",
    ),
    # -----------------------------------------------------
    # Case inventory
    # -----------------------------------------------------
    dict(
        name="workspace.case_count",
        dtype=int,
        compute_fn=case_count,
        description="Count of OWL case files in the current planning context.",
    ),
    dict(
        name="workspace.valid_case_count",
        dtype=int,
        compute_fn=valid_case_count,
        description="Count of loadable OWL case files in the current planning context.",
    ),
    # -----------------------------------------------------
    # Workspace inventory
    # -----------------------------------------------------
    dict(
        name="workspace.initialized",
        dtype=bool,
        compute_fn=workspace_initialized,
        description="Current directory is an initialized workspace.",
    ),
    dict(
        name="workspace.parent_count",
        dtype=int,
        compute_fn=workspace_parent_count,
        description="Number of parent workspaces above current subdirectory.",
    ),
    dict(
        name="workspace.child_count",
        dtype=int,
        compute_fn=workspace_child_count,
        description="Number of immediate child workspaces.",
    ),
    #
    # Household Libraries
    #
    dict(
        name="household.libraries",
        dtype=list[HouseholdLibrarySpec],
        compute_fn=household_libraries,
        override_policy=OverridePolicy.RECOMPUTE,
        description=("Ordered household libraries visible to the current planning context."),
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
    dict(
        name="directory_kind",
        dtype=str,
        compute_fn=directory_kind,
        description="Semantic classification of the current directory.",
    ),
    dict(
        name="identity.name",
        dtype=str,
        compute_fn=context_name,
        override_policy=OverridePolicy.NEVER,
        description=("Canonical name of the current planning context."),
    ),
    dict(
        name="identity.title",
        dtype=str,
        compute_fn=context_title,
        override_policy=OverridePolicy.RECOMPUTE,
        description=("Human-readable title of the current planning context."),
    ),
    dict(
        name="identity.description",
        dtype=str,
        compute_fn=context_description,
        override_policy=OverridePolicy.RECOMPUTE,
        description=("Descriptive summary of the current planning context."),
    ),
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
        override_policy=OverridePolicy.RECOMPUTE,
        description=("Absolute path to the directory containing household case files."),
    ),
    dict(
        name="paths.results",
        dtype=Path,
        compute_fn=context_results_path,
        override_policy=OverridePolicy.RECOMPUTE,
        description=("Absolute path to the directory used for generated planning results."),
    ),
]

# =========================================================
# Registration
# =========================================================


def make_compute_fn(fn):
    def compute(
        row,
        override=None,
    ):
        root = row["_path"]

        if override is None:
            return fn(root)

        return fn(
            root,
            override,
        )

    return compute


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
                override_policy=lever.get(
                    "override_policy",
                    OverridePolicy.NEVER,
                ),
                description=lever["description"],
                **ontology,
            )
        )
