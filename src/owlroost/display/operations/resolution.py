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


def extract_object_path(
    obj,
    path,
):
    """
    Extract a dotted attribute path from
    nested Python objects.
    """

    cur = obj

    for part in path.split("."):
        if cur is None:
            return None

        cur = getattr(
            cur,
            part,
            None,
        )

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
    5. expanded history context
    6. semantic namespaces
    7. semantic object registries
    8. _inputs
    9. top-level row
    """

    # =====================================================
    # Display-derived value
    # =====================================================

    if display_field is not None and display_field.display_fn is not None:
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
    # Parse semantic field
    # =====================================================

    head, sep, tail = field_name.partition(
        ".",
    )

    semantic_root = None

    if sep:
        semantic_root = row.get(
            f"_{head}",
        )

    # =====================================================
    # Expanded History Context
    #
    # history.<collection>.<field>
    #
    # resolves against:
    #
    #     row["_history_context"]["record"]
    # =====================================================

    if head == "history" and sep:
        ctx = row.get(
            "_history_context",
        )

        if ctx is not None:
            collection = ctx.get(
                "collection",
            )

            record = ctx.get(
                "record",
            )

            parts = tail.split(
                ".",
            )

            if len(parts) >= 2 and parts[0] == collection:
                value = extract_object_path(
                    record,
                    ".".join(parts[1:]),
                )

                if value is not None:
                    return value

    # =====================================================
    # Semantic namespaces
    # =====================================================

    if sep:
        if semantic_root is not None:
            value = extract_path(
                semantic_root,
                tail,
            )

            if value is not None:
                return value

    # =====================================================
    # Semantic object lookup
    # =====================================================

    if sep:
        if semantic_root is not None:
            obj, property_path = resolve_field_object(
                row,
                field_name,
            )

            if obj is not None:
                if not property_path:
                    return obj

                value = extract_object_path(
                    obj,
                    property_path,
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


# =========================================================
# Runtime DisplayField Resolution
# =========================================================


def resolve_display_field(
    registry,
    entry,
):
    """
    Resolve the DisplayField associated
    with one materialized view entry.

    Returns
    -------
    DisplayField | None

        None indicates that the field is
        resolved dynamically rather than
        through the DisplayRegistry.
    """

    try:
        return registry.get_display_field(
            entry["field"],
        )

    except KeyError:
        return None


def resolve_field_object(
    row,
    field_name,
):
    """
    Resolve the semantic object and
    remaining property path associated
    with a field.

    Example
    -------

        guide.workspace.initialize.command

    returns

        (
            GuideSpec(...),
            "command",
        )
    """

    head, sep, tail = field_name.partition(".")

    if not sep:
        return (
            None,
            None,
        )

    semantic_root = row.get(
        f"_{head}",
    )

    if semantic_root is None:
        return (
            None,
            None,
        )

    objects = semantic_root.get(
        "_objects",
        {},
    )

    parts = tail.split(".")

    for i in range(
        len(parts),
        0,
        -1,
    ):
        object_name = ".".join(
            parts[:i],
        )

        obj = objects.get(
            object_name,
        )

        if obj is None:
            continue

        property_path = ".".join(
            parts[i:],
        )

        return (
            obj,
            property_path,
        )

    return (
        None,
        None,
    )


def resolve_field_description(
    row,
    field_name,
):
    """
    Resolve documentation associated with
    a semantic field.
    """

    obj, property_path = resolve_field_object(
        row,
        field_name,
    )

    if obj is None:
        return ""

    #
    # Referring to the object itself
    # means "describe the object".
    #
    if not property_path:
        property_path = "description"

    describe = getattr(
        obj,
        "describe_property",
        None,
    )

    if describe is None:
        return ""

    return (
        describe(
            property_path,
        )
        or ""
    )
