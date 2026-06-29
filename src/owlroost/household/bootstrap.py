# src/owlroost/household/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household subsystem bootstrap.

Notes
-----
Builds the complete Household Registry by
discovering Household Projects from all
visible Household Libraries.

Architectural Invariants
------------------------

Bootstrap owns:

    * Registry construction
    * Search policy
    * Registry assembly

Bootstrap does not own:

    * Filesystem discovery
    * Manifest parsing
    * Household construction
    * Household mutation

Filesystem discovery belongs to the
loaders.

Registration belongs to the registry.

Future Directions
-----------------

Future revisions may search additional
libraries including:

* Current workspace
* User household library (XDG)
* CLI-specified libraries
* Package-installed libraries

The public interface should remain stable:

    build_household_registry()
"""

from __future__ import annotations

from pathlib import Path

from owlroost.household.households import (
    BUILTIN_HOUSEHOLD_LIBRARY,
)
from owlroost.household.loaders import (
    discover_household_library,
)
from owlroost.household.registry import (
    HouseholdRegistry,
)


def household_search_paths() -> list[Path]:
    """
    Return Household Libraries searched by
    default.

    Libraries are searched in precedence
    order.

    Missing directories are ignored by the
    loaders.

    Returns
    -------
    list[Path]
    """

    return [
        #
        # Current project library.
        #
        Path.cwd() / "households",
        #
        # Future:
        #
        # XDG user household library.
        #
        # Path.home()
        #     / ".local"
        #     / "share"
        #     / "roost"
        #     / "households",
        #
        # Built-in library.
        #
        BUILTIN_HOUSEHOLD_LIBRARY,
    ]


def build_household_registry() -> HouseholdRegistry:
    """
    Construct the complete Household
    Registry.

    Returns
    -------
    HouseholdRegistry
    """

    registry = HouseholdRegistry()

    for library in household_search_paths():
        for household in discover_household_library(
            library,
        ):
            registry.register_household(
                household,
            )

    return registry
