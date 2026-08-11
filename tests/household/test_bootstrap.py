# tests/household/test_bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for household bootstrap.

## Notes

Verifies that the public bootstrap
constructs a populated Household
Registry from the effective Household
Libraries configured by an explicit
workspace context.
"""

from __future__ import annotations

from owlroost.household.bootstrap import (
    build_household_registry,
    household_libraries,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
)


def test_household_libraries_returns_library_specs(
    workspace_root,
):
    """
    Household libraries are represented
    by HouseholdLibrarySpec objects.
    """

    libraries = household_libraries(
        root=workspace_root,
    )

    assert libraries

    assert all(
        isinstance(
            library,
            HouseholdLibrarySpec,
        )
        for library in libraries
    )


def test_household_libraries_contains_builtin(
    workspace_root,
):
    """
    The built-in Household Library is
    visible through the workspace
    context.
    """

    libraries = household_libraries(
        root=workspace_root,
    )

    assert any(library.name == "builtin" for library in libraries)


def test_build_household_registry_returns_registry(
    workspace_root,
):
    """
    The public bootstrap constructs
    a Household Registry.
    """

    registry = build_household_registry(
        root=workspace_root,
    )

    assert registry is not None


def test_build_household_registry_discovers_households(
    workspace_root,
):
    """
    At least one Household Project is
    discovered.
    """

    registry = build_household_registry(
        root=workspace_root,
    )

    assert len(registry) >= 1


def test_build_household_registry_discovers_minimum(
    workspace_root,
):
    """
    The built-in minimum household
    is registered.
    """

    registry = build_household_registry(
        root=workspace_root,
    )

    assert registry.has_household(
        "builtin/minimum",
    )


def test_build_household_registry_contains_expected_ids(
    workspace_root,
):
    """
    Household identifiers are
    discoverable through the public
    registry interface.
    """

    registry = build_household_registry(
        root=workspace_root,
    )

    assert "builtin/minimum" in registry.household_ids()


def test_build_household_registry_minimum_spec(
    workspace_root,
):
    """
    The built-in minimum household
    exposes both local and global
    identifiers.
    """

    registry = build_household_registry(
        root=workspace_root,
    )

    spec = registry.get_household(
        "builtin/minimum",
    )

    assert spec.id == "minimum"

    assert spec.global_id == "builtin/minimum"

    assert spec.library.name == "builtin"
