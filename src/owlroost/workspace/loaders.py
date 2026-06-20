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

    study.toml

Responsibilities
----------------
* Discover workspaces
* Load study metadata
* Materialize display rows

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


def _load_study_toml(
    path: Path,
):
    """
    Load study.toml.

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
    Build a workspace row.

    Parameters
    ----------
    workspace_dir
        Directory containing study.toml.
    """

    study_file = workspace_dir / "study.toml"

    study = _load_study_toml(
        study_file,
    )

    name = study.get(
        "name",
        workspace_dir.name,
    )

    title = study.get(
        "title",
        "",
    )

    description = study.get(
        "description",
        "",
    ).replace("\n", " ")

    cases_dir = workspace_dir / "cases"

    results_dir = workspace_dir / "results"

    return {
        "_path": workspace_dir.resolve(),
        "_meta": {
            "level": "workspace",
        },
        "_study": study,
        "workspace_name": name,
        "workspace_title": title,
        "workspace_description": description,
        "workspace_path": str(
            workspace_dir.resolve(),
        ),
        "study_file": str(
            study_file.resolve(),
        ),
        "cases_dir": str(
            (
                workspace_dir
                / study.get(
                    "cases_dir",
                    "cases" if (workspace_dir / "cases").exists() else ".",
                )
            ).resolve()
        ),
        "results_dir": str(
            (
                workspace_dir
                / study.get(
                    "results_dir",
                    "results",
                )
            ).resolve()
        ),
        "has_cases": cases_dir.exists(),
        "has_results": results_dir.exists(),
    }


def find_workspaces(
    source=".",
):
    """
    Discover workspaces.

    A workspace is any immediate
    subdirectory containing study.toml.

    Parameters
    ----------
    source
        Root directory containing
        workspaces.

    Returns
    -------
    list[Path]
    """

    source = Path(source)

    if not source.exists():
        return []

    workspaces = []

    for child in sorted(
        source.iterdir(),
        key=lambda p: p.name.lower(),
    ):
        if not child.is_dir():
            continue

        if (child / "study.toml").exists():
            workspaces.append(
                child,
            )

    return workspaces


def load_workspace_row(
    workspace_dir=".",
):
    workspace_dir = Path(
        workspace_dir,
    ).resolve()

    study_file = workspace_dir / "study.toml"

    if not study_file.exists():
        raise RoostError(f"Missing study.toml: {study_file}")

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
        find_workspaces(source),
    ):
        row = load_workspace_row(
            workspace_dir,
        )

        row["_meta"]["workspace_id"] = idx

        rows.append(
            row,
        )

    return rows
