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

Guide materialization evaluates the
registered workflow suggestions for
the current row and attaches both the
semantic evaluation and lightweight
summary structures.

Rendering is intentionally owned by
the display subsystem.
"""

from __future__ import annotations

from owlroost.guide.specs import (
    GuideStats,
)

# =========================================================
# Guide Materialization
# =========================================================


def materialize_guide(
    row,
    registry,
):
    """
    Attach guide evaluation and summary
    to a row.
    """

    evaluation = registry.evaluate(
        row=row,
    )

    row["_guide"] = evaluation

    row["_guide_stats"] = GuideStats(
        suggestion_count=len(
            evaluation.applicable_suggestions,
        ),
        top_suggestion=(
            evaluation.applicable_suggestions[0].suggestion.title
            if evaluation.applicable_suggestions
            else None
        ),
        has_suggestions=bool(
            evaluation.applicable_suggestions,
        ),
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
    Materialize applicable guide
    suggestions into a semantic tree.

    Explanation, requirement evaluation,
    and coverage remain attached to the
    guide evaluation object and are
    rendered later by the display
    subsystem.
    """

    evaluation = row.get(
        "_guide",
    )

    tree = {
        "kind": "section",
        "label": "Suggested Next Steps",
        "children": [],
    }

    if evaluation is None:
        row["_guide_tree"] = tree
        return row

    for result in evaluation.applicable_suggestions:
        suggestion = result.suggestion

        tree["children"].append(
            {
                "kind": "section",
                "label": suggestion.title,
                "field": f"guide.{suggestion.name}",
                "value": suggestion.command,
                "children": [],
            }
        )

    row["_guide_tree"] = tree

    return row
