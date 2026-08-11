# src/owlroost/household/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household subsystem bootstrap.

Notes
-----
Constructs the Household Registry by
discovering Household Projects within
the Household Libraries configured for
the current workspace context.

Household Library configuration is
defined by the effective workspace
definition:

    workspace.toml

The workspace loader owns composition of
canonical workspace defaults and local
workspace overrides.

This module interprets the resulting
household library configuration and
converts it into HouseholdLibrarySpec
objects.

Architectural Invariants
------------------------

Workspace owns:

    * workspace configuration
    * workspace configuration defaults
    * composition of local overrides
    * household library search policy

Household bootstrap owns:

    * interpretation of configured
      household libraries
    * resolution of library filesystem
      roots
    * HouseholdLibrarySpec construction
    * HouseholdRegistry assembly

Household loaders own:

    * filesystem discovery
    * manifest parsing
    * HouseholdSpec construction

Household registry owns:

    * registration
    * lookup
    * enumeration

The Household subsystem does not require
workspace configuration to be represented
as WorkspaceSpec observations.
"""

from __future__ import annotations

from pathlib import Path

from owlroost.core.settings import (
    get_workspace_template_dir,
)
from owlroost.household.loaders import (
    discover_household_library,
)
from owlroost.household.registry import (
    HouseholdRegistry,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
)
from owlroost.workspace.loaders import (
    load_workspace_definition,
)

# =========================================================
# Library Root Resolution
# =========================================================


def _resolve_household_library_root(
    name: str,
    location: str,
    workspace_root: Path,
) -> Path:
    """
    Resolve one configured Household
    Library location.
    """

    path = Path(
        location,
    ).expanduser()

    if path.is_absolute():
        return path.resolve()

    if name == "builtin":
        return (get_workspace_template_dir() / path).resolve()

    return (workspace_root / path).resolve()


# =========================================================
# Household Libraries
# =========================================================


def household_libraries(
    root=".",
) -> list[HouseholdLibrarySpec]:
    """
    Return the effective Household
    Libraries visible to the current
    workspace context.

    Parameters
    ----------
    root
        Workspace root.

    Returns
    -------
    list[HouseholdLibrarySpec]
        Household Libraries in configured
        search order.

    Notes
    -----
    Library ordering is significant.

    Household discovery follows the order
    declared by:

        context.households

    in the effective workspace definition.
    """

    workspace_root = Path(
        root,
    ).resolve()

    definition = load_workspace_definition(
        workspace_root,
    )

    context = definition.get(
        "context",
        {},
    )

    configured_libraries = context.get(
        "households",
        [],
    )

    libraries: list[HouseholdLibrarySpec] = []

    for configured in configured_libraries:
        name = configured.get(
            "name",
        )

        location = configured.get(
            "location",
        )

        if not name:
            raise ValueError("Household library configuration requires 'name'.")

        if not location:
            raise ValueError(f"Household library {name!r} requires 'location'.")

        root_path = _resolve_household_library_root(
            name=name,
            location=location,
            workspace_root=workspace_root,
        )

        #
        # Built-in libraries are package
        # resources and therefore
        # immutable from the household
        # subsystem.
        #

        read_only = name == "builtin"

        libraries.append(
            HouseholdLibrarySpec(
                name=name,
                root=root_path,
                read_only=read_only,
            )
        )

    return libraries


def household_library(
    name: str,
    root=".",
) -> HouseholdLibrarySpec:
    """
    Return one configured Household
    Library.

    Parameters
    ----------
    name
        Logical Household Library name.

    root
        Workspace root.

    Returns
    -------
    HouseholdLibrarySpec

    Raises
    ------
    KeyError
        Unknown Household Library.
    """

    for library in household_libraries(
        root,
    ):
        if library.name == name:
            return library

    raise KeyError(f"Unknown household library: {name}")


# =========================================================
# Registry
# =========================================================


def build_household_registry(
    root=".",
) -> HouseholdRegistry:
    """
    Construct the Household Registry
    visible to a workspace context.

    Parameters
    ----------
    root
        Workspace root.

    Returns
    -------
    HouseholdRegistry
    """

    registry = HouseholdRegistry()

    for library in household_libraries(
        root,
    ):
        registry.register_many(
            discover_household_library(
                library,
            )
        )

    return registry
