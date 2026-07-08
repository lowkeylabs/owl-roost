# tests/household/test_specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for Household specifications.

Notes
-----
Verifies the canonical representation
of Household Libraries and Household
Projects.
"""

from __future__ import annotations

from pathlib import Path

from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
)


def _library(
    root: Path,
) -> HouseholdLibrarySpec:
    """
    Construct a writable Household
    Library for testing.
    """

    return HouseholdLibrarySpec(
        name="test",
        root=root.parent,
        read_only=False,
    )


def test_household_library_spec_attributes(
    tmp_path,
):
    """
    Constructor preserves supplied
    attributes.
    """

    library = HouseholdLibrarySpec(
        name="workspace",
        root=tmp_path,
        read_only=False,
    )

    assert library.name == "workspace"
    assert library.root == tmp_path
    assert not library.read_only
    assert library.writable


def test_household_library_spec_readonly(
    tmp_path,
):
    """
    Read-only libraries are not
    writable.
    """

    library = HouseholdLibrarySpec(
        name="builtin",
        root=tmp_path,
        read_only=True,
    )

    assert library.read_only
    assert not library.writable


def test_household_spec_attributes(
    tmp_path,
):
    """
    Constructor preserves supplied
    attributes.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example Household",
        library=_library(tmp_path),
        root=tmp_path,
        description="Example description.",
        tags=(
            "example",
            "tutorial",
        ),
    )

    assert spec.id == "example"
    assert spec.title == "Example Household"
    assert spec.library.name == "test"
    assert spec.root == tmp_path
    assert spec.description == "Example description."
    assert spec.tags == (
        "example",
        "tutorial",
    )


def test_household_file(
    tmp_path,
):
    """
    Canonical executable specification.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.household_file == (tmp_path / "household.py")


def test_manifest_file(
    tmp_path,
):
    """
    Canonical manifest file.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.manifest_file == (tmp_path / "manifest.toml")


def test_readme_file(
    tmp_path,
):
    """
    Canonical README.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.readme_file == (tmp_path / "README.md")


def test_case_file(
    tmp_path,
):
    """
    Canonical OWL case file.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.case_file == (tmp_path / "case.toml")


def test_hfp_file(
    tmp_path,
):
    """
    Canonical HFP workbook.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.hfp_file == (tmp_path / "HFP.xlsx")


def test_exists_false(
    tmp_path,
):
    """
    Missing project directories
    report False.
    """

    missing = tmp_path / "missing"

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(missing),
        root=missing,
    )

    assert not spec.exists


def test_exists_true(
    tmp_path,
):
    """
    Existing project directories
    report True.
    """

    project = tmp_path / "example"

    project.mkdir()

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(project),
        root=project,
    )

    assert spec.exists


def test_artifact_names_empty(
    tmp_path,
):
    """
    Empty projects contain no
    artifacts.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.artifact_names == ()


def test_artifact_names(
    tmp_path,
):
    """
    Artifact names are returned in
    canonical order.
    """

    (tmp_path / "z.txt").write_text("")
    (tmp_path / "a.txt").write_text("")
    (tmp_path / "b.txt").write_text("")

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.artifact_names == (
        "a.txt",
        "b.txt",
        "z.txt",
    )


def test_has_artifact(
    tmp_path,
):
    """
    Artifact lookup by filename.
    """

    (tmp_path / "README.md").write_text(
        "# Example\n",
    )

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
    )

    assert spec.has_artifact(
        "README.md",
    )

    assert not spec.has_artifact(
        "case.toml",
    )


def test_name(
    tmp_path,
):
    """
    Household name is derived from the
    project directory.
    """

    project = tmp_path / "smith"

    project.mkdir()

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(project),
        root=project,
    )

    assert spec.name == "smith"


def test_to_row(
    tmp_path,
):
    """
    HouseholdSpec materializes into
    a display row.
    """

    spec = HouseholdSpec(
        id="example",
        title="Example",
        library=_library(tmp_path),
        root=tmp_path,
        description="Example description.",
        tags=(
            "tutorial",
            "builtin",
        ),
    )

    row = spec.to_row()

    assert row["household.id"] == "example"

    assert row["household.title"] == "Example"

    assert row["household.description"] == "Example description."

    assert row["household.root"] == str(tmp_path)

    assert row["household.exists"]

    assert row["household.artifact_count"] == 0

    assert row["household.tags"] == (
        "tutorial",
        "builtin",
    )
