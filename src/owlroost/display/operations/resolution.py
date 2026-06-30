# src/owlroost/display/operations/resolution.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Display value resolution.

Notes
-----
Resolves semantic display values from
materialized rows.

Architectural Invariant
-----------------------

Semantic namespaces follow the convention:

    namespace.field.subfield

which resolves against:

    row["_namespace"]["field"]["subfield"]

Examples
--------

    context.case_count
        -> row["_context"]["case_count"]

    workspace.identity.name
        -> row["_workspace"]["identity"]["name"]

    study.scenario_families
        -> row["_study"]["scenario_families"]

Resolvers therefore require no knowledge
of individual semantic namespaces.
"""

from __future__ import annotations

# =========================================================
# Path Extraction
# =========================================================


def extract_path(
    data,
    path,
):
    """
    Extract a dotted path from nested dictionaries.
    """

    if data is None:
        return None

    if path == "_path":
        return str(data["_path"])

    cur = data

    for part in path.split("."):
        if not isinstance(
            cur,
            dict,
        ):
            return None

        cur = cur.get(part)

        if cur is None:
            return None

    return cur


# =========================================================
# Semantic Field Resolution
# =========================================================


def resolve_field_value(
    row,
    field_name,
    display_field=None,
):
    """
    Resolve a semantic field value.

    Resolution order
    ----------------

    1. display_fn
    2. explicit display path
    3. _metrics
    4. _meta
    5. semantic namespace (_context, _workspace, ...)
    6. _inputs
    7. top-level row
    """

    # =====================================================
    # Display-derived value
    # =====================================================

    if display_field is not None and display_field.display_fn:
        return display_field.display_fn(
            row,
        )

    # =====================================================
    # Explicit display path
    # =====================================================

    if display_field is not None and display_field.path is not None:
        value = extract_path(
            row,
            display_field.path,
        )

        if value is not None:
            return value

    # =====================================================
    # Metrics
    # =====================================================

    metrics = row.get(
        "_metrics",
        {},
    )

    if field_name in metrics:
        return metrics[field_name]

    # =====================================================
    # Meta
    # =====================================================

    meta = row.get(
        "_meta",
        {},
    )

    if field_name in meta:
        return meta[field_name]

    # =====================================================
    # Semantic namespaces
    # =====================================================

    head, sep, tail = field_name.partition(".")

    if sep:
        semantic_root = row.get(
            f"_{head}",
        )

        if semantic_root is not None:
            value = extract_path(
                semantic_root,
                tail,
            )

            if value is not None:
                return value

    # =====================================================
    # Inputs
    # =====================================================

    value = extract_path(
        row.get(
            "_inputs",
            {},
        ),
        field_name,
    )

    if value is not None:
        return value

    # =====================================================
    # Top-level row
    # =====================================================

    return row.get(
        field_name,
    )


# =========================================================
# Row Value Resolution
# =========================================================


def resolve_row_value(
    row,
    key,
):
    """
    Resolve an operational row value.

    Resolution order
    ----------------

    1. synthetic aliases
    2. _meta
    3. _metrics
    4. semantic namespaces
    5. top-level row
    6. _inputs
    """

    # =====================================================
    # Synthetic aliases
    # =====================================================

    if key == "id":
        return row.get(
            "_row_id",
        )

    # =====================================================
    # Meta
    # =====================================================

    meta = row.get(
        "_meta",
        {},
    )

    if key in meta:
        return meta[key]

    # =====================================================
    # Metrics
    # =====================================================

    metrics = row.get(
        "_metrics",
        {},
    )

    if key in metrics:
        return metrics[key]

    # =====================================================
    # Semantic namespaces
    # =====================================================

    head, sep, tail = key.partition(".")

    if sep:
        semantic_root = row.get(
            f"_{head}",
        )

        if semantic_root is not None:
            value = extract_path(
                semantic_root,
                tail,
            )

            if value is not None:
                return value

    # =====================================================
    # Top-level row
    # =====================================================

    if key in row:
        return row[key]

    # =====================================================
    # _inputs
    # =====================================================

    return extract_path(
        row.get(
            "_inputs",
            {},
        ),
        key,
    )
