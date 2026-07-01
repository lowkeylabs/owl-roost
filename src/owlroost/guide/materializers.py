# src/owlroost/guide/materializers.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide materialization.

Notes
-----
Materializes workflow guidance onto
operational rows.

Guide materialization intentionally
produces two representations.

    _guide_eval

        Rich evaluation object used by
        explanation, coverage analysis,
        and future guide reasoning.

    _guide

        Semantic namespace consumed by
        the display subsystem exactly
        like _context, _workspace, and
        _study.

Rendering is owned entirely by the
display subsystem.
"""

from __future__ import annotations

# =========================================================
# Helpers
# =========================================================


def _build_guide_namespace(
    evaluation,
):
    """
    Convert a GuideEvaluation into the
    semantic guide namespace.
    """

    guide = {
        "summary": {
            "guide_count": len(
                evaluation.applicable_guides,
            ),
            "top_guide": (
                evaluation.applicable_guides[0].guide.title
                if evaluation.applicable_guides
                else None
            ),
            "has_guides": bool(
                evaluation.applicable_guides,
            ),
        },
    }

    #
    # Materialize applicable guides into
    # nested semantic namespaces.
    #
    # Example
    #
    #     workspace.initialize
    #
    # becomes
    #
    #     guide.workspace.initialize
    #

    for result in evaluation.applicable_guides:
        guide_spec = result.guide

        current = guide

        parts = guide_spec.name.split(".")

        for part in parts[:-1]:
            current = current.setdefault(
                part,
                {},
            )

        current[parts[-1]] = guide_spec.command

    return guide


# =========================================================
# Guide Materialization
# =========================================================


def materialize_guide(
    row,
    registry,
):
    """
    Attach guide evaluation and semantic
    guide namespace to a row.
    """

    evaluation = registry.evaluate(
        row=row,
    )

    #
    # Rich internal evaluation.
    #
    row["_guide_eval"] = evaluation

    #
    # Semantic namespace.
    #
    row["_guide"] = _build_guide_namespace(
        evaluation,
    )

    return row


# =========================================================
# Guide Tree Materialization
# =========================================================


def materialize_guide_tree(
    row,
    registry=None,
):
    """
    Materialize applicable guides into a
    semantic tree.

    The tree is intentionally structural.

    Values are resolved later by the
    display subsystem using the guide
    semantic namespace.
    """

    evaluation = row.get(
        "_guide_eval",
    )

    tree = {
        "kind": "section",
        "label": "Suggested Next Steps",
        "children": [],
    }

    if evaluation is None:
        row["_guide_tree"] = tree
        return row

    for result in evaluation.applicable_guides:
        guide = result.guide

        tree["children"].append(
            {
                "kind": "section",
                "label": guide.title,
                "field": f"guide.{guide.name}",
                "children": [],
            }
        )

    row["_guide_tree"] = tree

    return row
