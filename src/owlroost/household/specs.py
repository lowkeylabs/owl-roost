# src/owlroost/household/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household specifications.

Notes
-----
Defines the canonical metadata describing
Household Libraries and Household Projects.

Architectural Invariants
------------------------

HouseholdSpec describes a household project.

It does not contain runtime state.

It does not contain an instantiated OWL Plan.

It does not load household artifacts.

The registry owns discovery.

Loaders own construction.

This module also owns the canonical
household field definitions used by
display, catalogs, and materialization.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# =========================================================
# Household Field Definitions
# =========================================================

HOUSEHOLD_NAMESPACE = "household"


@dataclass(
    frozen=True,
    slots=True,
)
class HouseholdFieldSpec:
    """
    Canonical description of one
    household field.
    """

    name: str

    description: str


HOUSEHOLD_FIELDS: tuple[
    HouseholdFieldSpec,
    ...,
] = (
    HouseholdFieldSpec(
        "id",
        "Stable household identifier.",
    ),
    HouseholdFieldSpec(
        "name",
        "Canonical household project name.",
    ),
    HouseholdFieldSpec(
        "title",
        "Human-readable household title.",
    ),
    HouseholdFieldSpec(
        "description",
        "Household description.",
    ),
    HouseholdFieldSpec(
        "library",
        "Containing household library.",
    ),
    HouseholdFieldSpec(
        "relative_root",
        "Project path relative to the containing household library.",
    ),
    HouseholdFieldSpec(
        "root",
        "Household project directory.",
    ),
    HouseholdFieldSpec(
        "exists",
        "Whether the project directory exists.",
    ),
    HouseholdFieldSpec(
        "tags",
        "Household tags.",
    ),
    HouseholdFieldSpec(
        "artifact_count",
        "Number of project artifacts.",
    ),
    HouseholdFieldSpec(
        "artifact_names",
        "Project artifact filenames.",
    ),
)


def household_field_name(
    name: str,
) -> str:
    """
    Return the fully-qualified household
    field name.
    """

    return f"{HOUSEHOLD_NAMESPACE}.{name}"


# =========================================================
# Household Libraries
# =========================================================


@dataclass(
    frozen=True,
    slots=True,
)
class HouseholdLibrarySpec:
    """
    Canonical description of a household
    library.
    """

    name: str

    root: Path

    read_only: bool = False

    @property
    def writable(
        self,
    ) -> bool:
        """
        Return True if this library
        accepts modifications.
        """

        return not self.read_only


# =========================================================
# Household Projects
# =========================================================


@dataclass(
    frozen=True,
    slots=True,
)
class HouseholdSpec:
    """
    Canonical description of a registered
    household project.
    """

    id: str

    title: str

    library: HouseholdLibrarySpec

    root: Path

    description: str = ""

    tags: tuple[str, ...] = ()

    @property
    def household_file(
        self,
    ) -> Path:
        return self.root / "household.py"

    @property
    def manifest_file(
        self,
    ) -> Path:
        return self.root / "manifest.toml"

    @property
    def readme_file(
        self,
    ) -> Path:
        return self.root / "README.md"

    @property
    def case_file(
        self,
    ) -> Path:
        return self.root / "case.toml"

    @property
    def hfp_file(
        self,
    ) -> Path:
        return self.root / "HFP.xlsx"

    @property
    def exists(
        self,
    ) -> bool:
        return self.root.is_dir()

    @property
    def artifact_names(
        self,
    ) -> tuple[str, ...]:
        artifacts: list[str] = []

        for path in sorted(
            self.root.iterdir(),
            key=lambda p: p.name,
        ):
            if path.is_file():
                artifacts.append(
                    path.name,
                )

        return tuple(
            artifacts,
        )

    @property
    def name(
        self,
    ) -> str:
        """
        Canonical household project name.
        """

        return self.root.name

    @property
    def relative_root(
        self,
    ) -> Path:
        """
        Project path relative to its
        containing library.
        """

        return self.root.relative_to(
            self.library.root,
        )

    def has_artifact(
        self,
        name: str,
    ) -> bool:
        """
        Test whether an artifact exists.
        """

        return (self.root / name).exists()

    def to_row(
        self,
    ) -> dict[str, object]:
        """
        Convert the household
        specification into a catalog row.
        """

        row = {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "library": self.library.name,
            "relative_root": str(
                self.relative_root,
            ),
            "root": str(
                self.root,
            ),
            "exists": self.exists,
            "tags": self.tags,
            "artifact_count": len(
                self.artifact_names,
            ),
            "artifact_names": self.artifact_names,
        }

        return {household_field_name(key): value for key, value in row.items()}
