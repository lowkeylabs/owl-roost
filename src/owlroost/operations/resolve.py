# src/owlroost/operations/resolve.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Semantic value resolution.

Notes
-----
Provides subsystem-independent resolution
of semantic variables from a materialized
planning row.

Architectural Invariant
-----------------------
Resolution is catalog-driven.

The catalog defines semantic identity.

Materialized planning rows contain the
corresponding realized values.

This module bridges the two.

Unlike the display subsystem, semantic
resolution ignores presentation concepts
such as display functions, formatting,
and alternate display paths.

Typical usage
-------------

    catalog = build_catalog_context()

    row = load_context_row()

    ...

    value = resolve_value(
        catalog,
        row,
        "context.case_count",
    )
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
    Extract a dotted path from nested
    dictionaries.
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
# Semantic Resolution
# =========================================================


def _resolve_semantic_value(
    row,
    field_name,
):
    """
    Resolve a semantic variable from a
    materialized planning row.

    Resolution order
    ----------------

    1. _metrics
    2. _meta
    3. semantic namespace
    4. _inputs
    5. top-level row
    """

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
    # Semantic namespace
    # =====================================================

    head, sep, tail = field_name.partition(".")

    if sep:
        namespace = row.get(
            f"_{head}",
        )

        if namespace is not None:
            value = extract_path(
                namespace,
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
# Public API
# =========================================================


def resolve_value(
    catalog,
    row,
    field_name,
    *,
    default=None,
):
    """
    Resolve a semantic variable.

    Parameters
    ----------
    catalog
        CatalogContext returned by
        build_catalog_context().

    row
        Materialized planning row.

    field_name
        Canonical semantic variable.

    default
        Value returned if the variable
        cannot be resolved.

    Returns
    -------
    object
    """

    # =====================================================
    # Validate
    # =====================================================

    if catalog is None:
        raise ValueError("catalog must not be None.")

    if row is None:
        raise ValueError("row must not be None.")

    if not hasattr(
        catalog,
        "catalog_index",
    ):
        raise ValueError("catalog must provide catalog_index.")

    # =====================================================
    # Catalog lookup
    # =====================================================

    if field_name not in catalog.catalog_index:
        return default

    # =====================================================
    # Resolve
    # =====================================================

    value = _resolve_semantic_value(
        row,
        field_name,
    )

    if value is None:
        return default

    return value


# =========================================================
# Bound Resolver
# =========================================================


def build_resolver(
    catalog,
    row,
):
    """
    Build a semantic resolver bound to a
    specific planning row.

    Parameters
    ----------
    catalog
        CatalogContext.

    row
        Materialized planning row.

    Returns
    -------
    callable
        resolve(field_name, default=None)
    """

    def resolve(
        field_name,
        default=None,
    ):
        return resolve_value(
            catalog=catalog,
            row=row,
            field_name=field_name,
            default=default,
        )

    return resolve
