# src/owlroost/workspace/loaders.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace loaders.

Notes
-----
Owns discovery and loading of
workspace definitions.

A workspace is currently defined as
a directory containing:

    workspace.toml

Responsibilities
----------------
* Discover workspaces
* Load workspace metadata
* Materialize workspace rows

Does NOT
---------
* Render output
* Materialize tables
* Perform workspace operations
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from owlroost.exceptions import RoostError


def _load_workspace_toml(
    path: Path,
):
    """
    Load workspace.toml.

    Returns
    -------
    dict
        Parsed TOML.

    Empty dict on failure.
    """

    try:
        return tomllib.loads(
            path.read_text(),
        )

    except Exception:
        return {}


def _workspace_row(
    workspace_dir: Path,
):
    """
    Build canonical workspace row.

    Parameters
    ----------
    workspace_dir
        Directory containing workspace.toml.
    """

    workspace_file = workspace_dir / "workspace.toml"

    workspace = _load_workspace_toml(
        workspace_file,
    )

    cases_dir = (
        workspace_dir
        / workspace.get(
            "cases_dir",
            ("cases" if (workspace_dir / "cases").exists() else "."),
        )
    ).resolve()

    results_dir = (
        workspace_dir
        / workspace.get(
            "results_dir",
            "results",
        )
    ).resolve()

    inventory = {
        "studies": [],
        "experiments": [],
        "cases": [],
        "sessions": [],
        "runs": [],
        "trials": [],
    }

    return {
        "_path": workspace_dir.resolve(),
        "_meta": {
            "level": "workspace",
        },
        "_workspace": {
            # ---------------------------------------------
            # Identity
            # ---------------------------------------------
            "identity": {
                "name": workspace.get(
                    "name",
                    workspace_dir.name,
                ),
                "title": workspace.get(
                    "title",
                    "",
                ),
                "description": (
                    workspace.get(
                        "description",
                        "",
                    )
                    .replace(
                        "\n",
                        " ",
                    )
                    .strip()
                ),
            },
            # ---------------------------------------------
            # Definition
            # ---------------------------------------------
            "definition": workspace,
            "definition_file": str(
                workspace_file.resolve(),
            ),
            # ---------------------------------------------
            # Filesystem Layout
            # ---------------------------------------------
            "paths": {
                "workspace": str(
                    workspace_dir.resolve(),
                ),
                "cases": str(
                    cases_dir,
                ),
                "results": str(
                    results_dir,
                ),
            },
            # ---------------------------------------------
            # Inventory Summary
            #
            # Materialized inventory metrics
            # populate this structure.
            #
            # Seed values only.
            # ---------------------------------------------
            "summary": {
                "has_cases": len(inventory.get("cases", [])) > 0,
                "has_results": len(inventory.get("runs", [])) > 0,
            },
            # ---------------------------------------------
            # Inventory
            #
            # Detailed realizations discovered
            # from the workspace.
            #
            # Inventory materializers own
            # population of these collections.
            # ---------------------------------------------
            "inventory": inventory,
        },
    }


def find_workspaces(
    source=".",
):
    """
    Discover workspaces.

    A workspace is any immediate
    subdirectory containing workspace.toml.

    Parameters
    ----------
    source
        Root directory containing
        workspaces.

    Returns
    -------
    list[Path]
    """

    source = Path(
        source,
    )

    if not source.exists():
        return []

    workspaces = []

    for child in sorted(
        source.iterdir(),
        key=lambda p: p.name.lower(),
    ):
        if not child.is_dir():
            continue

        if (child / "workspace.toml").exists():
            workspaces.append(
                child,
            )

    return workspaces


def load_workspace_row(
    workspace_dir=".",
):
    """
    Load a single workspace row.
    """

    workspace_dir = Path(
        workspace_dir,
    ).resolve()

    workspace_file = workspace_dir / "workspace.toml"

    if not workspace_file.exists():
        raise RoostError(f"Missing workspace.toml: {workspace_file}")

    return _workspace_row(
        workspace_dir,
    )


def load_workspace_rows(
    source=".",
):
    """
    Load workspace rows.

    Parameters
    ----------
    source
        Directory containing
        workspaces.

    Returns
    -------
    list[dict]
    """

    rows = []

    for idx, workspace_dir in enumerate(
        find_workspaces(
            source,
        ),
    ):
        row = load_workspace_row(
            workspace_dir,
        )

        row["_meta"]["workspace_id"] = idx

        rows.append(
            row,
        )

    return rows
