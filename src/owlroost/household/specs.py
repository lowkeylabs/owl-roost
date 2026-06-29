# src/owlroost/household/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household specifications.

Notes
-----
Defines the canonical metadata describing a registered
Household Project.

Architectural Invariants
------------------------

A HouseholdSpec describes a household project.

It does not contain runtime state.

It does not contain an instantiated OWL Plan.

It does not load household artifacts.

The registry owns discovery.

Loaders own construction.

Future Directions
-----------------

Future revisions may expose additional metadata such as:

* provenance
* supported artifacts
* supported exports
* supported capabilities
* educational metadata

The goal is to keep HouseholdSpec lightweight while
allowing the surrounding project directory to evolve.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True,
)
class HouseholdSpec:
    """
    Canonical description of a registered
    household project.

    Parameters
    ----------
    id
        Stable registry identifier.

    title
        Human-readable household name.

    root
        Root directory of the household
        project.

    description
        Short descriptive text.

    tags
        User-facing tags used for search,
        categorization, and documentation.

    Notes
    -----
    The household project directory is the
    canonical identity of the project.

    Files within that directory represent
    household artifacts.

    HouseholdSpec intentionally avoids
    embedding runtime objects such as an
    instantiated OWL Plan.
    """

    id: str

    title: str

    root: Path

    description: str = ""

    tags: tuple[str, ...] = ()

    @property
    def household_file(
        self,
    ) -> Path:
        """
        Return the executable household
        specification.

        Returns
        -------
        Path
        """

        return self.root / "household.py"

    @property
    def manifest_file(
        self,
    ) -> Path:
        """
        Return metadata file.

        Returns
        -------
        Path
        """

        return self.root / "manifest.toml"

    @property
    def readme_file(
        self,
    ) -> Path:
        """
        Return README.

        Returns
        -------
        Path
        """

        return self.root / "README.md"

    @property
    def case_file(
        self,
    ) -> Path:
        """
        Return canonical OWL case file.

        Returns
        -------
        Path
        """

        return self.root / "case.toml"

    @property
    def hfp_file(
        self,
    ) -> Path:
        """
        Return canonical Household
        Financial Profile workbook.

        Returns
        -------
        Path
        """

        return self.root / "HFP.xlsx"

    @property
    def exists(
        self,
    ) -> bool:
        """
        Return True if the household
        project directory exists.
        """

        return self.root.is_dir()

    @property
    def artifact_names(
        self,
    ) -> tuple[str, ...]:
        """
        Return artifact filenames
        present within the project.

        Returns
        -------
        tuple[str, ...]
        """

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

    def has_artifact(
        self,
        name: str,
    ) -> bool:
        """
        Test whether an artifact exists.

        Parameters
        ----------
        name
            Filename relative to the
            household project root.

        Returns
        -------
        bool
        """

        return (self.root / name).exists()

    def to_row(
        self,
    ) -> dict[str, object]:
        """
        Convert the household
        specification into a display row.

        Returns
        -------
        dict
        """

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tags": ", ".join(
                self.tags,
            ),
            "root": str(
                self.root,
            ),
            "exists": self.exists,
            "artifacts": len(
                self.artifact_names,
            ),
        }
