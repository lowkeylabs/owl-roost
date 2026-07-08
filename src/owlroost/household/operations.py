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

import shutil
from pathlib import Path

from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
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
