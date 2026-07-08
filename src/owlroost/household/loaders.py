# src/owlroost/household/loaders.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household project loaders.

Notes
-----
Owns filesystem interaction for
Household Projects.

Responsibilities include:

    * Household Library discovery
    * Manifest parsing
    * Manifest validation
    * HouseholdSpec construction
    * Household row materialization

Architectural Invariants
------------------------

Loaders own:

    * Filesystem discovery
    * Filesystem inspection
    * Manifest parsing
    * Manifest validation
    * HouseholdSpec construction
    * Row materialization

Loaders do not own:

    * Search policy
    * Registry population
    * Household construction
    * Filesystem mutation
    * Display rendering

Future Directions
-----------------

Future revisions may support:

* Manifest version upgrades
* Rich validation diagnostics
* Imported household formats
* Additional project artifacts
* Capability discovery
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from owlroost.household.registry import (
    HouseholdRegistry,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
)

MANIFEST_FILENAME = "manifest.toml"

CURRENT_MANIFEST_VERSION = 1


def load_household_manifest(
    project_dir: Path,
    library: HouseholdLibrarySpec,
) -> HouseholdSpec:
    """
    Load one Household Project.

    Parameters
    ----------
    project_dir
        Household Project directory.

    library
        Household Library containing
        the project.

    Returns
    -------
    HouseholdSpec

    Raises
    ------
    FileNotFoundError
        Manifest not found.

    ValueError
        Invalid or unsupported
        manifest contents.
    """

    manifest = project_dir / MANIFEST_FILENAME

    if not manifest.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest}")

    try:
        with manifest.open(
            "rb",
        ) as fp:
            data = tomllib.load(
                fp,
            )

    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Invalid TOML: {manifest}") from exc

    required_fields = (
        "id",
        "title",
    )

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise ValueError(
            f"{manifest}: missing required field(s): "
            + ", ".join(
                missing_fields,
            )
        )

    manifest_version = data.get(
        "manifest_version",
        CURRENT_MANIFEST_VERSION,
    )

    if manifest_version != CURRENT_MANIFEST_VERSION:
        raise ValueError(f"{manifest}: unsupported manifest_version {manifest_version}")

    household_id = data["id"]

    title = data["title"]

    if not isinstance(
        household_id,
        str,
    ):
        raise ValueError(f"{manifest}: 'id' must be a string.")

    if not isinstance(
        title,
        str,
    ):
        raise ValueError(f"{manifest}: 'title' must be a string.")

    tags = data.get(
        "tags",
        (),
    )

    if not isinstance(
        tags,
        (
            list,
            tuple,
        ),
    ):
        raise ValueError(f"{manifest}: 'tags' must be a list.")

    return HouseholdSpec(
        id=household_id,
        title=title,
        library=library,
        root=project_dir,
        description=data.get(
            "description",
            "",
        ),
        tags=tuple(
            tags,
        ),
    )


def discover_household_library(
    library: HouseholdLibrarySpec,
) -> list[HouseholdSpec]:
    """
    Discover Household Projects within a
    Household Library.

    Parameters
    ----------
    library
        Household Library to
        discover.

    Returns
    -------
    list[HouseholdSpec]

    Notes
    -----
    Every immediate subdirectory
    containing a manifest.toml file
    is considered a Household Project.

    Missing libraries produce an
    empty result.
    """

    if not library.root.is_dir():
        return []

    households: list[HouseholdSpec] = []

    for project_dir in sorted(
        library.root.iterdir(),
        key=lambda p: p.name.lower(),
    ):
        if not project_dir.is_dir():
            continue

        if not (project_dir / MANIFEST_FILENAME).is_file():
            continue

        households.append(
            load_household_manifest(
                project_dir,
                library,
            )
        )

    return households


def load_household_row(
    spec: HouseholdSpec,
) -> dict[str, object]:
    """
    Materialize one Household Project
    into a display row.

    Parameters
    ----------
    spec
        Household specification.

    Returns
    -------
    dict[str, object]
    """

    return spec.to_row()


def load_household_rows(
    registry: HouseholdRegistry,
) -> list[dict[str, object]]:
    """
    Materialize Household Registry
    rows.

    Parameters
    ----------
    registry
        Household registry.

    Returns
    -------
    list[dict[str, object]]
    """

    return [
        load_household_row(
            spec,
        )
        for spec in registry.household_specs()
    ]
