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
    HouseholdSpec,
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

    spec = HouseholdSpec(
        id="example",
        title="Example",
        root=Path("/tmp/example"),
    )

    registry.register_household(
        spec,
    )

    assert len(registry) == 1

    assert registry.has_household(
        "example",
    )

    assert "example" in registry


def test_register_duplicate_household_raises():
    """
    Duplicate household ids are
    rejected.
    """

    registry = HouseholdRegistry()

    spec = HouseholdSpec(
        id="example",
        title="Example",
        root=Path("/tmp/example"),
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
            HouseholdSpec(
                id="a",
                title="A",
                root=Path("/tmp/a"),
            ),
            HouseholdSpec(
                id="b",
                title="B",
                root=Path("/tmp/b"),
            ),
        ]
    )

    assert (
        len(
            registry,
        )
        == 2
    )

    assert registry.household_ids() == (
        "a",
        "b",
    )


def test_get_household():
    """
    Registered households may be
    retrieved by id.
    """

    registry = HouseholdRegistry()

    spec = HouseholdSpec(
        id="example",
        title="Example",
        root=Path("/tmp/example"),
    )

    registry.register_household(
        spec,
    )

    assert (
        registry.get_household(
            "example",
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
            "missing",
        )


def test_household_ids_sorted():
    """
    Household ids are returned in
    canonical order.
    """

    registry = HouseholdRegistry()

    registry.register_household(
        HouseholdSpec(
            id="zebra",
            title="Zebra",
            root=Path("/tmp/zebra"),
        )
    )

    registry.register_household(
        HouseholdSpec(
            id="alpha",
            title="Alpha",
            root=Path("/tmp/alpha"),
        )
    )

    assert registry.household_ids() == (
        "alpha",
        "zebra",
    )


def test_household_specs_sorted():
    """
    Household specifications follow
    canonical id ordering.
    """

    registry = HouseholdRegistry()

    registry.register_household(
        HouseholdSpec(
            id="zebra",
            title="Zebra",
            root=Path("/tmp/zebra"),
        )
    )

    registry.register_household(
        HouseholdSpec(
            id="alpha",
            title="Alpha",
            root=Path("/tmp/alpha"),
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
        HouseholdSpec(
            id="b",
            title="B",
            root=Path("/tmp/b"),
        )
    )

    registry.register_household(
        HouseholdSpec(
            id="a",
            title="A",
            root=Path("/tmp/a"),
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
        "minimum",
    )

    spec = registry.get_household(
        "minimum",
    )

    assert spec.id == "minimum"

    assert spec.title == "Minimum Household"
