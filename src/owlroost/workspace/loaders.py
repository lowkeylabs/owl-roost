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

# =========================================================
# Helpers
# =========================================================


WORKSPACE_TOML = "workspace.toml"


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


def _load_workspace_definition(
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

    workspace_file = workspace_dir / WORKSPACE_TOML

    workspace = _load_workspace_toml(
        workspace_file,
    )

    row["_workspace"] = {
        # ---------------------------------------------
        # Original context
        # ---------------------------------------------
        "definition": workspace,
        "definition_file": str(
            workspace_file.resolve(),
        ),
        "definition_note": "see ./workspace/loaders.py",
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
        if child.is_dir() and (child / WORKSPACE_TOML).exists():
            workspaces.append(
                child,
            )

    return workspaces


# =========================================================
# Public Loaders
# =========================================================


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

    row = _build_context_row(
        workspace_dir,
    )

    workspace_file = workspace_dir / WORKSPACE_TOML

    if workspace_file.exists():
        row = _load_workspace_definition(
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
