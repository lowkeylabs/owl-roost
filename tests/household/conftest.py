# tests/household/conftest.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household test fixtures.

Notes
-----
Provides reusable fixtures for the
Household subsystem test suite.

Architectural Invariants
------------------------

Tests should construct Household
Registries through the public
bootstrap interface whenever
practical.

Temporary Household Libraries
should be used for filesystem
mutation tests.
"""

from __future__ import annotations

import pytest

from owlroost.household.bootstrap import (
    build_household_registry,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
)


@pytest.fixture
def registry():
    """
    Return the populated Household
    Registry.
    """

    return build_household_registry()


@pytest.fixture
def writable_library(
    tmp_path,
):
    """
    Temporary writable Household
    Library.
    """

    root = tmp_path / "households"

    root.mkdir()

    return HouseholdLibrarySpec(
        name="test",
        root=root,
        read_only=False,
    )


@pytest.fixture
def readonly_library(
    tmp_path,
):
    """
    Temporary read-only Household
    Library.
    """

    root = tmp_path / "builtin"

    root.mkdir()

    return HouseholdLibrarySpec(
        name="builtin",
        root=root,
        read_only=True,
    )


@pytest.fixture
def household(
    writable_library,
):
    """
    Temporary Household Project.
    """

    root = writable_library.root / "smith"

    root.mkdir()

    return HouseholdSpec(
        id="smith",
        title="Smith Household",
        library=writable_library,
        root=root,
    )
