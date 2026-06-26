# src/owlroost/workspace/tree.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Generic tree utilities.

Notes
-----
Supports the generic hierarchical tree
grammar used throughout ROOST.

Tree nodes follow the form:

    {
        "kind": "...",
        "label": "...",
        "field": "...",        # optional
        "value": ...,          # optional
        "meta": {...},         # optional
        "children": [...],     # optional
    }

These helpers intentionally know
nothing about studies, workspaces,
or display fields.
"""

from __future__ import annotations

# =========================================================
# Tree lookup
# =========================================================


def lookup_tree_node(
    root,
    field_name,
):
    """
    Return the first node whose
    ``field`` matches ``field_name``.

    Parameters
    ----------
    root
        Root tree node or list.

    field_name
        Display field name to locate.

    Returns
    -------
    dict | None
    """

    if root is None:
        return None

    #
    # List
    #
    if isinstance(
        root,
        list,
    ):
        for child in root:
            found = lookup_tree_node(
                child,
                field_name,
            )

            if found is not None:
                return found

        return None

    #
    # Ignore non-tree objects.
    #
    if not isinstance(
        root,
        dict,
    ):
        return None

    #
    # Match current node.
    #
    if (
        root.get(
            "field",
        )
        == field_name
    ):
        return root

    #
    # Search children.
    #
    for child in root.get(
        "children",
        [],
    ):
        found = lookup_tree_node(
            child,
            field_name,
        )

        if found is not None:
            return found

    return None


# =========================================================
# Convenience lookup
# =========================================================


def lookup_tree_value(
    root,
    field_name,
    default=None,
):
    """
    Return the materialized value for a
    field stored in a tree.

    Parameters
    ----------
    root
        Tree root.

    field_name
        Display field.

    default
        Value returned if the field
        is not present.

    Returns
    -------
    object
    """

    node = lookup_tree_node(
        root,
        field_name,
    )

    if node is None:
        return default

    return node.get(
        "value",
        default,
    )


# =========================================================
# Existence helper
# =========================================================


def tree_contains_field(
    root,
    field_name,
):
    """
    Return True if the tree contains
    a node for ``field_name``.
    """

    return (
        lookup_tree_node(
            root,
            field_name,
        )
        is not None
    )
