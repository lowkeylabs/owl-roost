# src/owlroost/household/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household subsystem bootstrap.

Notes
-----
Construct the Household Registry by
discovering Household Projects within
the effective Household Libraries for
the current planning context.

Architectural Invariants
------------------------

Bootstrap owns:

    * Registry construction
    * Registry assembly

Bootstrap does not own:

    * Planning context resolution
    * Filesystem discovery
    * Manifest parsing
    * Household construction
    * Household mutation

Planning context resolution belongs to
the workspace subsystem.

Filesystem discovery belongs to the
household loaders.

Registration belongs to the registry.

Future Directions
-----------------

Future revisions may construct
registries for alternate planning
contexts or explicitly supplied
household libraries.

The public interface should remain
stable:

    build_household_registry()
"""

from __future__ import annotations

from owlroost.catalog.context import (
    build_catalog_context,
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
from owlroost.operations.resolve import (
    build_resolver,
)
from owlroost.workspace.loaders import (
    load_context_row,
)
from owlroost.workspace.materializers import (
    materialize_planning_context,
)

# =========================================================
# Household Libraries
# =========================================================


def household_libraries(
    root=".",
) -> list[HouseholdLibrarySpec]:
    """
    Return the effective Household
    Libraries visible to the current
    planning context.

    Parameters
    ----------
    root
        Planning context root.

    Returns
    -------
    list[HouseholdLibrarySpec]
    """

    catalog = build_catalog_context()

    planning_context = materialize_planning_context(
        load_context_row(
            root,
        ),
        catalog,
    )

    resolve = build_resolver(
        catalog,
        planning_context,
    )

    return resolve(
        "context.household.libraries",
    )


def household_library(
    name: str,
    root=".",
) -> HouseholdLibrarySpec:
    """
    Return one configured household
    library.

    Raises
    ------
    KeyError
        Unknown household library.
    """

    for library in household_libraries(root):
        if library.name == name:
            return library

    raise KeyError(f"Unknown household library: {name}")


# =========================================================
# Registry
# =========================================================


def build_household_registry() -> HouseholdRegistry:
    """
    Construct the complete Household
    Registry.

    Returns
    -------
    HouseholdRegistry
    """

    registry = HouseholdRegistry()

    for library in household_libraries():
        registry.register_many(
            discover_household_library(
                library,
            )
        )

    return registry
