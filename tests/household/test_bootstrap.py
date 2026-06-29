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
Registry from the built-in Household
Library.
"""

from __future__ import annotations

from pathlib import Path

from owlroost.household.bootstrap import (
    build_household_registry,
    household_search_paths,
)
from owlroost.household.households import (
    BUILTIN_HOUSEHOLD_LIBRARY,
)


def test_household_search_paths_returns_builtin_library():
    """
    The built-in Household Library
    participates in the default
    search path.
    """

    paths = household_search_paths()

    assert BUILTIN_HOUSEHOLD_LIBRARY in paths


def test_household_search_paths_returns_paths():
    """
    Every search path is represented
    as a pathlib.Path.
    """

    paths = household_search_paths()

    assert paths

    assert all(
        isinstance(
            path,
            Path,
        )
        for path in paths
    )


def test_build_household_registry_returns_registry():
    """
    The public bootstrap constructs
    a Household Registry.
    """

    registry = build_household_registry()

    assert registry is not None


def test_build_household_registry_discovers_households():
    """
    The built-in Household Library
    contributes at least one
    Household Project.
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

    ids = registry.household_ids()

    assert "minimum" in ids
