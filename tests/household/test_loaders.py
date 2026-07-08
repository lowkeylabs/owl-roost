# tests/household/test_loaders.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for household project loaders.

Notes
-----
Verifies filesystem discovery,
manifest loading, and row
materialization.

The loaders are intentionally tested
using temporary Household Libraries
rather than the built-in library
whenever practical.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from owlroost.household.loaders import (
    discover_household_library,
    load_household_manifest,
    load_household_row,
    load_household_rows,
)
from owlroost.household.registry import (
    HouseholdRegistry,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
)

# =========================================================
# Helpers
# =========================================================


def library(
    root: Path,
) -> HouseholdLibrarySpec:
    """
    Construct a writable Household
    Library for testing.
    """

    return HouseholdLibrarySpec(
        name="test",
        root=root,
        read_only=False,
    )


def write_manifest(
    project: Path,
    *,
    household_id: str = "example",
    title: str = "Example Household",
) -> None:
    """
    Create a minimal manifest.
    """

    project.mkdir(
        parents=True,
        exist_ok=True,
    )

    (project / "manifest.toml").write_text(
        f"""
manifest_version = 1

id = "{household_id}"

title = "{title}"
""".strip()
        + "\n"
    )


# =========================================================
# Manifest Loading
# =========================================================


def test_load_household_manifest(
    tmp_path,
):
    """
    A valid manifest loads into a
    HouseholdSpec.
    """

    lib = library(tmp_path)

    project = tmp_path / "example"

    write_manifest(
        project,
    )

    spec = load_household_manifest(
        project,
        lib,
    )

    assert spec.id == "example"
    assert spec.title == "Example Household"
    assert spec.library is lib
    assert spec.root == project


def test_load_household_manifest_missing_file(
    tmp_path,
):
    """
    Missing manifests raise
    FileNotFoundError.
    """

    lib = library(tmp_path)

    project = tmp_path / "example"

    project.mkdir()

    with pytest.raises(
        FileNotFoundError,
    ):
        load_household_manifest(
            project,
            lib,
        )


def test_load_household_manifest_requires_id(
    tmp_path,
):
    """
    Household id is required.
    """

    lib = library(tmp_path)

    project = tmp_path / "example"

    project.mkdir()

    (project / "manifest.toml").write_text(
        """
manifest_version = 1

title = "Example"
"""
    )

    with pytest.raises(
        ValueError,
    ):
        load_household_manifest(
            project,
            lib,
        )


def test_load_household_manifest_requires_title(
    tmp_path,
):
    """
    Household title is required.
    """

    lib = library(tmp_path)

    project = tmp_path / "example"

    project.mkdir()

    (project / "manifest.toml").write_text(
        """
manifest_version = 1

id = "example"
"""
    )

    with pytest.raises(
        ValueError,
    ):
        load_household_manifest(
            project,
            lib,
        )


def test_load_household_manifest_invalid_toml(
    tmp_path,
):
    """
    Invalid TOML raises ValueError.
    """

    lib = library(tmp_path)

    project = tmp_path / "example"

    project.mkdir()

    (project / "manifest.toml").write_text(
        """
id =
"""
    )

    with pytest.raises(
        ValueError,
    ):
        load_household_manifest(
            project,
            lib,
        )


# =========================================================
# Library Discovery
# =========================================================


def test_discover_household_library_empty(
    tmp_path,
):
    """
    Empty libraries produce no
    households.
    """

    households = discover_household_library(
        library(tmp_path),
    )

    assert households == []


def test_discover_household_library_discovers_household(
    tmp_path,
):
    """
    A directory containing a
    manifest is discovered.
    """

    lib = library(tmp_path)

    write_manifest(
        tmp_path / "example",
    )

    households = discover_household_library(
        lib,
    )

    assert len(households) == 1

    assert households[0].id == "example"

    assert households[0].library is lib


def test_discover_household_library_ignores_non_projects(
    tmp_path,
):
    """
    Directories lacking a
    manifest are ignored.
    """

    (tmp_path / "foo").mkdir()

    households = discover_household_library(
        library(tmp_path),
    )

    assert households == []


def test_discover_household_library_returns_sorted_households(
    tmp_path,
):
    """
    Household discovery follows
    canonical directory ordering.
    """

    write_manifest(
        tmp_path / "zebra",
        household_id="zebra",
        title="Zebra",
    )

    write_manifest(
        tmp_path / "alpha",
        household_id="alpha",
        title="Alpha",
    )

    households = discover_household_library(
        library(tmp_path),
    )

    assert [spec.id for spec in households] == [
        "alpha",
        "zebra",
    ]


# =========================================================
# Row Materialization
# =========================================================


def test_load_household_row(
    tmp_path,
):
    """
    One HouseholdSpec materializes
    into one display row.
    """

    lib = library(tmp_path)

    project = tmp_path / "example"

    write_manifest(
        project,
    )

    spec = load_household_manifest(
        project,
        lib,
    )

    row = load_household_row(
        spec,
    )

    assert row["household.id"] == "example"
    assert row["household.title"] == "Example Household"
    assert row["household.library"] == "test"


def test_load_household_rows(
    tmp_path,
):
    """
    Registry rows are materialized
    in canonical order.
    """

    registry = HouseholdRegistry()

    write_manifest(
        tmp_path / "zebra",
        household_id="zebra",
        title="Zebra",
    )

    write_manifest(
        tmp_path / "alpha",
        household_id="alpha",
        title="Alpha",
    )

    registry.register_many(
        discover_household_library(
            library(tmp_path),
        )
    )

    rows = load_household_rows(
        registry,
    )

    assert [row["household.id"] for row in rows] == [
        "alpha",
        "zebra",
    ]
