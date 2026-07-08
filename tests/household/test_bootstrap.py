# tests/household/test_bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for household bootstrap.

Notes
-----
Verifies that the public bootstrap
constructs a populated Household
Registry from the effective
Household Libraries.
"""

from __future__ import annotations

from owlroost.household.bootstrap import (
    build_household_registry,
    household_libraries,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
)


def test_household_libraries_returns_library_specs():
    """
    Household libraries are represented
    by HouseholdLibrarySpec objects.
    """

    libraries = household_libraries()

    assert libraries

    assert all(
        isinstance(
            library,
            HouseholdLibrarySpec,
        )
        for library in libraries
    )


def test_household_libraries_contains_builtin():
    """
    The built-in Household Library is
    visible through the planning
    context.
    """

    libraries = household_libraries()

    assert any(library.name == "builtin" for library in libraries)


def test_build_household_registry_returns_registry():
    """
    The public bootstrap constructs
    a Household Registry.
    """

    registry = build_household_registry()

    assert registry is not None


def test_build_household_registry_discovers_households():
    """
    At least one Household Project is
    discovered.
    """

    registry = build_household_registry()

    assert (
        len(
            registry,
        )
        >= 1
    )


def test_build_household_registry_discovers_minimum():
    """
    The built-in minimum household
    is registered.
    """

    registry = build_household_registry()

    assert registry.has_household(
        "minimum",
    )


def test_build_household_registry_contains_expected_ids():
    """
    Household identifiers are
    discoverable through the public
    registry interface.
    """

    registry = build_household_registry()

    assert "minimum" in registry.household_ids()
