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
planning contexts and workspace
definitions.

A planning context always exists.

A workspace is an optional planning
artifact represented by:

    workspace.toml

Responsibilities
----------------
* Discover workspaces
* Load planning contexts
* Load workspace definitions
* Materialize canonical planning rows

Does NOT
---------
* Render output
* Materialize tables
* Populate inventory
* Perform workspace operations
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from owlroost.exceptions import RoostError

# =========================================================
# Helpers
# =========================================================


def _load_workspace_toml(
    path: Path,
):
    """
    Load workspace.toml.

    Returns
    -------
    dict

    Empty dict on failure.
    """

    try:
        return tomllib.loads(
            path.read_text(),
        )

    except Exception:
        return {}


# =========================================================
# Row Builders
# =========================================================


def _build_context_row(
    root: Path,
):
    """
    Build the canonical planning context.

    Every directory has a planning
    context regardless of whether an
    initialized workspace exists.
    """

    return {
        "_path": root.resolve(),
        "_meta": {
            "level": "workspace",
        },
        "_context": {
            "root": str(
                root.resolve(),
            ),
        },
    }


def _materialize_workspace(
    row,
    workspace_dir: Path,
):
    """
    Attach workspace information to an
    existing planning context.

    Parameters
    ----------
    row
        Context row.

    workspace_dir
        Directory containing
        workspace.toml.
    """

    workspace_file = workspace_dir / "workspace.toml"

    workspace = _load_workspace_toml(
        workspace_file,
    )

    row["_workspace"] = {
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
        # Workspace Layout
        # ---------------------------------------------
        "paths": {
            "workspace": str(
                workspace_dir.resolve(),
            ),
            "cases": str(
                (
                    workspace_dir
                    / workspace.get(
                        "cases_dir",
                        ("cases" if (workspace_dir / "cases").exists() else "."),
                    )
                ).resolve()
            ),
            "results": str(
                (
                    workspace_dir
                    / workspace.get(
                        "results_dir",
                        "results",
                    )
                ).resolve()
            ),
            "reports": str(
                (
                    workspace_dir
                    / workspace.get(
                        "reports_dir",
                        "reports",
                    )
                ).resolve()
            ),
        },
    }

    return row


# =========================================================
# Discovery
# =========================================================


def find_workspaces(
    source=".",
):
    """
    Discover initialized workspaces.

    A workspace is any immediate
    subdirectory containing
    workspace.toml.
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
        if child.is_dir() and (child / "workspace.toml").exists():
            workspaces.append(
                child,
            )

    return workspaces


# =========================================================
# Public Loaders
# =========================================================


def load_context_row(
    root=".",
):
    """
    Load a planning context.

    A planning context always exists.

    If the directory contains an
    initialized workspace, workspace
    information is attached.
    """

    root = Path(
        root,
    ).resolve()

    row = _build_context_row(
        root,
    )

    if (root / "workspace.toml").exists():
        _materialize_workspace(
            row,
            root,
        )

    return row


def load_workspace_row(
    workspace_dir=".",
):
    """
    Load a single initialized
    workspace.
    """

    workspace_dir = Path(
        workspace_dir,
    ).resolve()

    workspace_file = workspace_dir / "workspace.toml"

    if not workspace_file.exists():
        raise RoostError(f"Missing workspace.toml: {workspace_file}")

    row = _build_context_row(
        workspace_dir,
    )

    _materialize_workspace(
        row,
        workspace_dir,
    )

    return row


def load_workspace_rows(
    source=".",
):
    """
    Load discovered workspaces.
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
