# src/owlroost/display/operations/comparison.py
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

from collections import defaultdict

# =========================================================
# Override filtering
# =========================================================

EXCLUDED_OVERRIDE_PREFIXES = {
    "case.file",
    "case.name",
}

# =========================================================
# Helpers
# =========================================================


def _normalize_overrides(overrides):
    """
    Normalize overrides into a clean dictionary.

    Example:

        solver_options.solver=HiGHS

    becomes:

        {
            "solver_options.solver": "HiGHS"
        }
    """

    if not overrides:
        return {}

    normalized = {}

    for x in overrides:
        x = str(x).strip()

        if not x:
            continue

        if "=" not in x:
            continue

        key, value = x.split(
            "=",
            1,
        )

        key = key.strip()
        value = value.strip()

        if key in EXCLUDED_OVERRIDE_PREFIXES:
            continue

        normalized[key] = value

    return normalized


def _extract_overrides(row):
    """
    Extract Hydra overrides from row metadata.
    """

    meta = row.get(
        "_meta",
        {},
    )

    overrides = meta.get(
        "task_overrides",
        [],
    )

    return _normalize_overrides(
        overrides,
    )


# =========================================================
# Comparison Computation
# =========================================================


def _assign_group_override_metrics(
    rows,
    *,
    scope,
):
    """
    Compute comparison information for a
    comparison scope.

    Stores results in:

        row["_comparison"][scope]
    """

    if not rows:
        return

    override_sets = [_extract_overrides(row) for row in rows]

    common_items = set.intersection(*[set(d.items()) for d in override_sets])

    common = dict(
        common_items,
    )

    group_row_ids = [
        row.get(
            "_row_id",
        )
        for row in rows
    ]

    for row, override_set in zip(
        rows,
        override_sets,
        strict=False,
    ):
        specific = {k: v for k, v in override_set.items() if common.get(k) != v}

        comparison = row.setdefault(
            "_comparison",
            {},
        )

        comparison[scope] = {
            "group_row_ids": group_row_ids,
            "common_overrides": common,
            "run_specific_overrides": specific,
        }


# =========================================================
# Override Comparisons
# =========================================================


def apply_override_comparison(
    rows,
):
    """
    Compute override comparisons for all
    supported scopes.
    """

    if not rows:
        return rows

    # -----------------------------------------------------
    # Working-set scope
    # -----------------------------------------------------

    _assign_group_override_metrics(
        rows,
        scope="working_set",
    )

    # -----------------------------------------------------
    # Session scope
    # -----------------------------------------------------

    groups = defaultdict(list)

    for row in rows:
        meta = row.get(
            "_meta",
            {},
        )

        key = (
            meta.get("case_id"),
            meta.get("session_id"),
        )

        groups[key].append(
            row,
        )

    for group_rows in groups.values():
        _assign_group_override_metrics(
            group_rows,
            scope="session",
        )

    return rows


# =========================================================
# Public API
# =========================================================


def apply_comparisons(
    rows,
):
    """
    Compute all comparison artifacts.

    Notes
    -----
    Comparison artifacts are derived from
    the visible row set after filtering,
    sorting, and projection.

    Results are stored under:

        row["_comparison"]
    """

    if not rows:
        return rows

    apply_override_comparison(
        rows,
    )

    return rows
