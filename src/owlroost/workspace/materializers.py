# src/owlroost/workspace/materializers.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from collections.abc import Callable


def workspace_lookup(
    field_name: str,
) -> Callable:
    """
    Resolve workspace values from
    row["_workspace"].

    Example
    -------
    workspace.name

        -> _workspace.name

    workspace.paths.results

        -> _workspace.paths.results
    """

    path_parts = field_name.split(".")[1:]

    def compute_fn(
        row,
    ):
        value = row.get(
            "_workspace",
            {},
        )

        for part in path_parts:
            if not isinstance(
                value,
                dict,
            ):
                return None

            value = value.get(
                part,
            )

            if value is None:
                return None

        return value

    return compute_fn


# =========================================================
# Nested Assignment
# =========================================================


def _set_workspace_value(
    row,
    field_name,
    value,
):
    """
    Store a workspace observation
    into row["_workspace"].

    Example
    -------

    workspace.has_results

        -> _workspace["has_results"]

    workspace.paths.results

        -> _workspace["paths"]["results"]
    """

    current = row.setdefault(
        "_workspace",
        {},
    )

    parts = field_name.split(".")[1:]

    for part in parts[:-1]:
        current = current.setdefault(
            part,
            {},
        )

    current[parts[-1]] = value


def materialize_workspace(
    row,
    workspace_registry,
):
    """
    Materialize workspace observations.

    Writes values into:

        row["_workspace"]
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    for field in workspace_registry.all():
        if field.compute_fn is None:
            continue

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        _set_workspace_value(
            row,
            field.name,
            value,
        )

    return row
