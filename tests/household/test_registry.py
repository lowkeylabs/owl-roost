# tests/household/test_registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for HouseholdRegistry.

Notes
-----
Verifies registration, lookup,
and enumeration.

The registry owns semantic
registration rather than
filesystem inspection or
row materialization.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from owlroost.household.registry import (
    HouseholdRegistry,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
)

TEST_LIBRARY = HouseholdLibrarySpec(
    name="test",
    root=Path("/tmp"),
    read_only=False,
)


def global_id(
    household_id: str,
) -> str:
    """
    Return the registry identifier for
    a test household.
    """

    return f"{TEST_LIBRARY.name}/{household_id}"


def household(
    household_id: str,
    title: str | None = None,
) -> HouseholdSpec:
    """
    Construct a HouseholdSpec for
    registry testing.
    """

    if title is None:
        title = household_id.title()

    root = TEST_LIBRARY.root / household_id

    return HouseholdSpec(
        title=title,
        library=TEST_LIBRARY,
        root=root,
    )


def test_registry_initially_empty():
    """
    Newly constructed registries
    contain no households.
    """

    registry = HouseholdRegistry()

    assert len(registry) == 0

    assert registry.household_ids() == ()

    assert registry.household_specs() == ()


def test_register_household():
    """
    Registering a household makes
    it discoverable.
    """

    registry = HouseholdRegistry()

    spec = household(
        "example",
        "Example",
    )

    registry.register_household(
        spec,
    )

    assert len(registry) == 1

    assert registry.has_household(
        global_id("example"),
    )

    assert global_id("example") in registry


def test_register_duplicate_household_raises():
    """
    Duplicate household ids are
    rejected.
    """

    registry = HouseholdRegistry()

    spec = household(
        "example",
        "Example",
    )

    registry.register_household(
        spec,
    )

    with pytest.raises(
        ValueError,
    ):
        registry.register_household(
            spec,
        )


def test_register_many():
    """
    Multiple households may be
    registered simultaneously.
    """

    registry = HouseholdRegistry()

    registry.register_many(
        [
            household(
                "a",
                "A",
            ),
            household(
                "b",
                "B",
            ),
        ]
    )

    assert len(registry) == 2

    assert registry.household_ids() == (
        global_id("a"),
        global_id("b"),
    )


def test_get_household():
    """
    Registered households may be
    retrieved by id.
    """

    registry = HouseholdRegistry()

    spec = household(
        "example",
        "Example",
    )

    registry.register_household(
        spec,
    )

    assert (
        registry.get_household(
            global_id("example"),
        )
        is spec
    )


def test_unknown_household_raises():
    """
    Unknown household ids raise
    KeyError.
    """

    registry = HouseholdRegistry()

    with pytest.raises(
        KeyError,
    ):
        registry.get_household(
            global_id("missing"),
        )


def test_household_ids_sorted():
    """
    Household ids are returned in
    canonical order.
    """

    registry = HouseholdRegistry()

    registry.register_household(
        household(
            "zebra",
            "Zebra",
        )
    )

    registry.register_household(
        household(
            "alpha",
            "Alpha",
        )
    )

    assert registry.household_ids() == (
        global_id("alpha"),
        global_id("zebra"),
    )


def test_household_specs_sorted():
    """
    Household specifications follow
    canonical id ordering.
    """

    registry = HouseholdRegistry()

    registry.register_household(
        household(
            "zebra",
            "Zebra",
        )
    )

    registry.register_household(
        household(
            "alpha",
            "Alpha",
        )
    )

    specs = registry.household_specs()

    assert [spec.id for spec in specs] == [
        "alpha",
        "zebra",
    ]


def test_registry_iteration():
    """
    Registries iterate in canonical
    order.
    """

    registry = HouseholdRegistry()

    registry.register_household(
        household(
            "b",
            "B",
        )
    )

    registry.register_household(
        household(
            "a",
            "A",
        )
    )

    ids = [spec.id for spec in registry]

    assert ids == [
        "a",
        "b",
    ]


def test_registry_fixture_contains_minimum(
    registry,
):
    """
    The built-in registry contains
    the minimum household.
    """

    assert registry.has_household(
        "builtin/minimum",
    )

    spec = registry.get_household(
        "builtin/minimum",
    )

    assert spec.id == "minimum"

    assert spec.title == "Minimum Household"

    assert spec.library.name == "builtin"
