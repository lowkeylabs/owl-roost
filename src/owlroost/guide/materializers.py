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

#    _guide_eval
#
#        Rich evaluation object used by
#        explanation, coverage analysis,
#        and future guide reasoning.
#
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

    The namespace contains both the
    semantic values consumed by display
    fields and the semantic objects used
    for dynamic property resolution.

    Objects include:

        GuideSpec
        GuideResult
        RequirementResult
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
            "variables": sorted(
                evaluation.required_variables,
            ),
        },
        #
        # Semantic object registry.
        #
        "_objects": {},
    }

    #
    # Materialize every evaluated guide.
    #
    for guide_result in evaluation.all_guides:
        guide_spec = guide_result.guide

        #
        # -------------------------------------------------
        # GuideSpec
        # -------------------------------------------------
        #
        guide["_objects"][guide_spec.name] = guide_spec

        #
        # -------------------------------------------------
        # GuideResult
        # -------------------------------------------------
        #
        guide["_objects"][f"{guide_spec.name}.result"] = guide_result

        #
        # -------------------------------------------------
        # RequirementResult objects
        # -------------------------------------------------
        #
        for i, requirement_result in enumerate(
            guide_result.requirement_results,
        ):
            guide["_objects"][(f"{guide_spec.name}.requirement.{i}")] = requirement_result

        #
        # -------------------------------------------------
        # Semantic value
        #
        # Only applicable guides receive a
        # command value in the namespace.
        # -------------------------------------------------
        #
        if guide_result.applicable:
            current = guide

            parts = guide_spec.name.split(
                ".",
            )

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


def materialize_guide_suggestion_tree(
    row,
):
    """
    Materialize applicable guides into a
    semantic tree.
    """

    evaluation = row.get(
        "_guide_eval",
    )

    tree = {
        "kind": "section",
        "label": "Suggested Next Steps",
        "children": [],
    }

    if evaluation is not None:
        for result in evaluation.applicable_guides:
            guide = result.guide

            tree["children"].append(
                {
                    "kind": "section",
                    "label": guide.title,
                    "field": (f"guide.{guide.name}"),
                    "children": [],
                }
            )

    row["_guide_suggestions"] = tree

    return row


def materialize_guide_detail_tree(
    row,
):
    """
    Materialize detailed information for
    applicable guides.
    """

    evaluation = row.get(
        "_guide_eval",
    )

    tree = {
        "kind": "section",
        "label": "Guide Details",
        "children": [],
    }

    if evaluation is not None:
        for result in evaluation.applicable_guides:
            guide = result.guide

            tree["children"].append(
                {
                    "kind": "section",
                    "label": guide.title,
                    "children": [
                        {
                            "kind": "section",
                            "label": "Description",
                            "field": (f"guide.{guide.name}.description"),
                            "children": [],
                        },
                        {
                            "kind": "section",
                            "label": "Command",
                            "field": (f"guide.{guide.name}.command"),
                            "children": [],
                        },
                    ],
                }
            )

    row["_guide_details"] = tree

    return row


def materialize_guide_workflow_tree(
    row,
):
    """
    Materialize workflow availability.

    Available guides resolve to their
    semantic command values.

    Unavailable guides remain structural
    since they are intentionally not
    materialized into the guide semantic
    namespace.
    """

    evaluation = row.get(
        "_guide_eval",
    )

    tree = {
        "kind": "section",
        "label": "Workflow",
        "children": [],
    }

    if evaluation is not None:
        available = {
            "kind": "section",
            "label": "Available",
            "children": [],
        }

        unavailable = {
            "kind": "section",
            "label": "Unavailable",
            "children": [],
        }

        #
        # Applicable transforms.
        #
        for result in evaluation.applicable_guides:
            guide = result.guide

            available["children"].append(
                {
                    "kind": "section",
                    "label": guide.title,
                    "field": (f"guide.{guide.name}"),
                    "children": [],
                }
            )

        #
        # Rejected transforms.
        #
        # These are not materialized into
        # _guide, so they remain structural.
        #
        for result in evaluation.rejected_guides:
            unavailable["children"].append(
                {
                    "kind": "section",
                    "label": result.guide.title,
                    "children": [],
                }
            )

        tree["children"].extend(
            [
                available,
                unavailable,
            ]
        )

    row["_guide_workflows"] = tree

    return row


def materialize_guide_reasoning_tree(
    row,
):
    """
    Materialize guide applicability
    reasoning.

    Each RequirementResult is exposed
    through the semantic guide object
    namespace. The requirement node is
    structural; its children resolve the
    RequirementResult properties.
    """

    evaluation = row.get(
        "_guide_eval",
    )

    tree = {
        "kind": "section",
        "label": "Guide Reasoning",
        "children": [],
    }

    if evaluation is not None:
        for result in evaluation.all_guides:
            guide = result.guide

            guide_node = {
                "kind": "section",
                "label": guide.title,
                "children": [],
            }

            for i, requirement in enumerate(
                result.requirement_results,
            ):
                prefix = f"guide.{guide.name}.requirement.{i}"

                guide_node["children"].append(
                    {
                        "kind": "section",
                        "label": (requirement.requirement.variable),
                        #
                        # Structural node only.
                        #
                        "children": [
                            {
                                "kind": "section",
                                "label": "Operator",
                                "field": (f"{prefix}.requirement.operator"),
                                "children": [],
                            },
                            {
                                "kind": "section",
                                "label": "Expected",
                                "field": (f"{prefix}.requirement.value"),
                                "children": [],
                            },
                            {
                                "kind": "section",
                                "label": "Actual",
                                "field": (f"{prefix}.actual"),
                                "children": [],
                            },
                            {
                                "kind": "section",
                                "label": "Satisfied",
                                "field": (f"{prefix}.satisfied"),
                                "children": [],
                            },
                        ],
                    }
                )

            tree["children"].append(
                guide_node,
            )

    row["_guide_reasoning"] = tree

    return row


def materialize_guide_variable_tree(
    row,
):
    """
    Materialize the semantic variables
    consumed during guide evaluation.
    """

    variables = (
        row.get(
            "_guide",
            {},
        )
        .get(
            "summary",
            {},
        )
        .get(
            "variables",
            [],
        )
    )

    tree = {
        "kind": "section",
        "label": "Guide Variables",
        "children": [],
    }

    for variable in variables:
        tree["children"].append(
            {
                "kind": "section",
                "label": variable,
                "children": [],
            }
        )

    row["_guide_variables"] = tree

    return row


def materialize_guide_diagnostic_tree(
    row,
):
    """
    Materialize guide diagnostics.

    Diagnostic values are resolved from
    the semantic guide namespace.
    """

    tree = {
        "kind": "section",
        "label": "Guide Diagnostics",
        "children": [
            {
                "kind": "section",
                "label": "Applicable",
                "field": ("guide.summary.applicable_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Rejected",
                "field": ("guide.summary.rejected_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Variables",
                "field": ("guide.summary.required_variable_count"),
                "children": [],
            },
        ],
    }

    row["_guide_diagnostics"] = tree

    return row


def materialize_guide_trees(
    row,
):
    """
    Materialize every guide tree.
    """

    row = materialize_guide_suggestion_tree(row)
    row = materialize_guide_detail_tree(row)
    row = materialize_guide_workflow_tree(row)
    row = materialize_guide_reasoning_tree(row)
    row = materialize_guide_variable_tree(row)
    row = materialize_guide_diagnostic_tree(row)

    return row
