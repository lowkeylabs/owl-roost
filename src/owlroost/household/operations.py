# src/owlroost/household/operations.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household project operations.

Notes
-----
Owns filesystem mutations involving
Household Projects.

Architectural Invariants
------------------------

This module owns operations that create,
rename, import, export, and delete
Household Projects.

It does not:

    * discover household projects
    * populate registries
    * parse manifests
    * render displays

Those responsibilities belong to the
loaders, registry, and display
subsystems.

Future Directions
-----------------

Future revisions may support:

* import from OWL case files
* import from existing workspaces
* executable household specifications
* export workflows
* validation
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
)
from owlroost.workspace.owl_utils import (
    resolve_household,
    save_household,
)

# =========================================================
# Helpers
# =========================================================


def household_root(
    library: HouseholdLibrarySpec,
    name: str,
) -> Path:
    """
    Return the canonical project root
    within a household library.
    """

    return library.root / name


def household_name_from_case(
    case_file: Path,
) -> str:
    """
    Return the canonical household
    project name derived from a
    ROOST case filename.

    Parameters
    ----------
    case_file
        ROOST case TOML.

    Returns
    -------
    str
    """

    name = Path(case_file).stem

    #
    # Strip the conventional prefix.
    #

    if name.lower().startswith(
        "case_",
    ):
        name = name[5:]

    #
    # Canonical filesystem name.
    #

    name = name.lower()

    # while not good practice, "+" is allowable.
    if 0:
        name = name.replace(
            "+",
            "-",
        )

    name = name.replace(
        "_",
        "-",
    )

    name = re.sub(
        r"[^a-z0-9-]+",
        "-",
        name,
    )

    name = re.sub(
        r"-+",
        "-",
        name,
    )

    return name.strip("-")


# =========================================================
# Manifest
# =========================================================


def write_manifest(
    household: HouseholdSpec,
) -> Path:
    """
    Write the canonical household
    manifest.

    Parameters
    ----------
    household
        Household to serialize.

    Returns
    -------
    Path
        Manifest filename.
    """

    manifest = household.root / "manifest.toml"

    lines: list[str] = [
        "manifest_version = 1",
        "",
        f'title = "{household.title}"',
    ]

    if household.description:
        lines.extend(
            [
                "",
                'description = """',
                household.description.rstrip(),
                '"""',
            ]
        )

    if household.tags:
        lines.extend(
            [
                "",
                "tags = [",
            ]
        )

        for tag in household.tags:
            lines.append(f'    "{tag}",')

        lines.append("]")

    manifest.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return manifest


# =========================================================
# Creation
# =========================================================


def create_household(
    library: HouseholdLibrarySpec,
    name: str,
) -> Path:
    """
    Create an empty Household Project.

    Parameters
    ----------
    library
        Destination household library.

    name
        Project directory name.

    Returns
    -------
    Path
        Newly created project root.

    Raises
    ------
    PermissionError
        Library is read-only.

    FileExistsError
        Household already exists.
    """

    if library.read_only:
        raise PermissionError(f"Household library '{library.name}' is read-only.")

    root = household_root(
        library,
        name,
    )

    if root.exists():
        raise FileExistsError(root)

    root.mkdir(
        parents=True,
    )

    return root


# =========================================================
# Import / Export
# =========================================================


def import_household(
    source: Path,
    library: HouseholdLibrarySpec,
):
    """
    Import a Household Project into a
    household library.

    Notes
    -----
    Placeholder for future
    implementation.
    """

    raise NotImplementedError


def export_household(
    household: HouseholdSpec,
    destination: Path,
):
    """
    Export a Household Project.

    Notes
    -----
    Placeholder for future
    implementation.
    """

    raise NotImplementedError


# =========================================================
# Rename
# =========================================================


def rename_household(
    household: HouseholdSpec,
    new_name: str,
) -> Path:
    """
    Rename a Household Project.

    Parameters
    ----------
    household
        Household to rename.

    new_name
        New project directory name.

    Returns
    -------
    Path
        New project root.
    """

    if household.library.read_only:
        raise PermissionError(f"Household library '{household.library.name}' is read-only.")

    destination = household.root.with_name(
        new_name,
    )

    household.root.rename(
        destination,
    )

    return destination


# =========================================================
# Deletion
# =========================================================


def delete_household(
    household: HouseholdSpec,
) -> None:
    """
    Delete a Household Project.

    Parameters
    ----------
    household
        Household project to remove.
    """

    if household.library.read_only:
        raise PermissionError(f"Household library '{household.library.name}' is read-only.")

    shutil.rmtree(
        household.root,
    )


def import_case(
    case_file: Path,
    library: HouseholdLibrarySpec,
) -> HouseholdSpec:
    """
    Import one ROOST case into a
    Household Library.

    Parameters
    ----------
    case_file
        Source case.toml file.

    library
        Destination household library.

    Returns
    -------
    HouseholdSpec
        Imported household.
    """

    case_file = Path(
        case_file,
    ).resolve()

    #
    # Canonical project name.
    #

    project_name = household_name_from_case(
        case_file,
    )

    project_root = create_household(
        library,
        project_name,
    )

    #
    # Construct and resolve the
    # OWL household.
    #

    plan = resolve_household(
        case_file,
    )

    #
    # Save canonical household
    # artifacts.
    #

    household = HouseholdSpec(
        root=project_root,
        title=project_name.replace("-", " ").title(),
        library=library,
    )

    write_manifest(
        household,
    )

    save_household(
        plan,
        project_root,
        case_file="case_household.toml",
        hfp_file="case_household.xlsx",
    )

    #
    # Return the corresponding
    # HouseholdSpec.
    #

    return HouseholdSpec(
        root=project_root,
        title=project_name,
        library=library,
    )


def export_case(
    household: HouseholdSpec,
    destination: Path,
) -> tuple[Path, Path]:
    """
    Export one Household Project as a
    ROOST case into a workspace.

    Parameters
    ----------
    household
        Household to export.

    destination
        Destination directory.

    Returns
    -------
    tuple[Path, Path]
        Written case TOML and HFP paths.

    Raises
    ------
    FileExistsError
        One or more destination files
        already exist.
    """

    destination = Path(
        destination,
    ).resolve()

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    #
    # Canonical destination names.
    #

    case_file = destination / f"case_{household.id}.toml"

    hfp_file = destination / f"HFP_{household.id}.xlsx"

    #
    # Refuse to overwrite.
    #

    duplicates = []

    if case_file.exists():
        duplicates.append(case_file)

    if hfp_file.exists():
        duplicates.append(hfp_file)

    if duplicates:
        raise FileExistsError(
            "Destination file(s) already exist: " + ", ".join(str(path) for path in duplicates)
        )

    #
    # Construct the OWL Plan.
    #

    plan = resolve_household(
        household.case_file,
    )

    #
    # Save canonical workspace artifacts.
    #

    save_household(
        plan,
        destination,
        case_file=case_file.name,
        hfp_file=hfp_file.name,
    )

    return (
        case_file,
        hfp_file,
    )
