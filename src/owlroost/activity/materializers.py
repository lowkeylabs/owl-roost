# src/owlroost/activity/materializers.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning activity materialization.

Notes
-----
Materializes planning activity
evaluation onto operational rows.

Activity materialization intentionally
produces two representations.

    _activity_eval

        Rich evaluation object used by
        explanation, coverage analysis,
        and future planning-cycle
        reasoning.

    _activity

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


def _build_activity_namespace(
    evaluation,
):
    """
    Convert an ActivityEvaluation into
    the semantic activity namespace.

    The namespace contains both the
    semantic values consumed by display
    fields and the semantic objects used
    for dynamic property resolution.

    Objects include:

        ActivitySpec
        ActivityResult
        RequirementResult
    """

    activity = {
        "summary": {
            #
            # Overall activity counts.
            #
            "activity_count": len(
                evaluation.all_activities,
            ),
            "applicable_count": len(
                evaluation.applicable_activities,
            ),
            "rejected_count": len(
                evaluation.rejected_activities,
            ),
            #
            # Applicable activity summary.
            #
            "top_activity": (
                evaluation.applicable_activities[0].activity.title
                if evaluation.applicable_activities
                else None
            ),
            "has_activities": bool(
                evaluation.applicable_activities,
            ),
            #
            # Variable coverage.
            #
            "required_variable_count": len(
                evaluation.required_variables,
            ),
            "observed_variable_count": len(
                evaluation.observed_variables,
            ),
            "unused_variable_count": len(
                evaluation.unused_variables,
            ),
            "variables": sorted(
                evaluation.required_variables,
            ),
        },  #
        # Semantic object registry.
        #
        "_objects": {},
    }

    #
    # Materialize every evaluated activity.
    #
    for activity_result in evaluation.all_activities:
        activity_spec = activity_result.activity

        #
        # -------------------------------------------------
        # ActivitySpec
        # -------------------------------------------------
        #
        activity["_objects"][activity_spec.name] = activity_spec

        #
        # -------------------------------------------------
        # ActivityResult
        # -------------------------------------------------
        #
        activity["_objects"][f"{activity_spec.name}.result"] = activity_result

        #
        # -------------------------------------------------
        # RequirementResult objects
        # -------------------------------------------------
        #
        for i, requirement_result in enumerate(
            activity_result.requirement_results,
        ):
            activity["_objects"][f"{activity_spec.name}.requirement.{i}"] = requirement_result

        #
        # -------------------------------------------------
        # Semantic value
        #
        # Only applicable activities are
        # materialized into the semantic
        # namespace.
        # -------------------------------------------------
        #
        if activity_result.applicable:
            current = activity

            parts = activity_spec.name.split(
                ".",
            )

            for part in parts[:-1]:
                current = current.setdefault(
                    part,
                    {},
                )

            current[parts[-1]] = activity_spec.suggested_commands

    return activity


# =========================================================
# Activity Materialization
# =========================================================


def materialize_activity(
    row,
    registry,
):
    """
    Attach activity evaluation and the
    semantic activity namespace to a
    planning row.
    """

    evaluation = registry.evaluate(
        row=row,
    )

    #
    # Rich internal evaluation.
    #
    row["_activity_eval"] = evaluation

    #
    # Semantic namespace.
    #
    row["_activity"] = _build_activity_namespace(
        evaluation,
    )

    return row


# =========================================================
# Guide Tree Materialization
# =========================================================


def materialize_activity_suggestion_tree(
    row,
):
    """
    Materialize applicable planning
    activities into a semantic tree.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Suggested Activities",
        "children": [],
    }

    if evaluation is not None:
        for result in evaluation.applicable_activities:
            activity = result.activity

            tree["children"].append(
                {
                    "kind": "section",
                    "label": activity.title,
                    "field": (f"activity.{activity.name}"),
                    "children": [],
                }
            )

    row["_activity_suggestions"] = tree

    return row


def materialize_activity_detail_tree(
    row,
):
    """
    Materialize detailed information for
    applicable planning activities.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Details",
        "children": [],
    }

    if evaluation is not None:
        for result in evaluation.applicable_activities:
            activity = result.activity

            tree["children"].append(
                {
                    "kind": "section",
                    "label": activity.title,
                    "children": [
                        {
                            "kind": "section",
                            "label": "Description",
                            "field": (f"activity.{activity.name}.description"),
                            "children": [],
                        },
                        {
                            "kind": "section",
                            "label": "Suggested Commands",
                            "field": (f"activity.{activity.name}.suggested_commands"),
                            "children": [],
                        },
                    ],
                }
            )

    row["_activity_details"] = tree

    return row


def materialize_activity_status_tree(
    row,
):
    """
    Materialize planning activity
    availability.

    Applicable activities resolve to
    their semantic activity values.

    Rejected activities remain
    structural since they are
    intentionally not materialized into
    the activity semantic namespace.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Status",
        "children": [],
    }

    if evaluation is not None:
        applicable = {
            "kind": "section",
            "label": "Applicable",
            "children": [],
        }

        rejected = {
            "kind": "section",
            "label": "Not Applicable",
            "children": [],
        }

        #
        # Applicable activities.
        #
        for result in evaluation.applicable_activities:
            activity = result.activity

            applicable["children"].append(
                {
                    "kind": "section",
                    "label": activity.title,
                    "field": (f"activity.{activity.name}"),
                    "children": [],
                }
            )

        #
        # Rejected activities.
        #
        # These are intentionally not
        # materialized into the activity
        # namespace, so they remain
        # structural.
        #
        for result in evaluation.rejected_activities:
            rejected["children"].append(
                {
                    "kind": "section",
                    "label": result.activity.title,
                    "children": [],
                }
            )

        tree["children"].extend(
            [
                applicable,
                rejected,
            ]
        )

    row["_activity_status"] = tree

    return row


def materialize_activity_reasoning_tree(
    row,
):
    """
    Materialize activity applicability
    reasoning.

    Each RequirementResult is exposed
    through the semantic activity object
    namespace. The requirement node is
    structural; its children resolve the
    RequirementResult properties.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Reasoning",
        "children": [],
    }

    if evaluation is not None:
        for result in evaluation.all_activities:
            activity = result.activity

            activity_node = {
                "kind": "section",
                "label": activity.title,
                "children": [],
            }

            for i, requirement in enumerate(
                result.requirement_results,
            ):
                prefix = f"activity.{activity.name}.requirement.{i}"

                activity_node["children"].append(
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
                activity_node,
            )

    row["_activity_reasoning"] = tree

    return row


def materialize_activity_variable_tree(
    row,
):
    """
    Materialize the semantic variables
    consumed during activity
    evaluation.
    """

    variables = (
        row.get(
            "_activity",
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
        "label": "Activity Variables",
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

    row["_activity_variables"] = tree

    return row


def materialize_activity_diagnostic_tree(
    row,
):
    """
    Materialize activity diagnostics.

    Diagnostic values are resolved from
    the semantic activity namespace.
    """

    tree = {
        "kind": "section",
        "label": "Activity Diagnostics",
        "children": [
            {
                "kind": "section",
                "label": "Applicable",
                "field": ("activity.summary.applicable_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Rejected",
                "field": ("activity.summary.rejected_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Variables",
                "field": ("activity.summary.required_variable_count"),
                "children": [],
            },
        ],
    }

    row["_activity_diagnostics"] = tree

    return row


def materialize_activity_trees(
    row,
):
    """
    Materialize every activity tree.
    """

    row = materialize_activity_suggestion_tree(
        row,
    )

    row = materialize_activity_detail_tree(
        row,
    )

    row = materialize_activity_status_tree(
        row,
    )

    row = materialize_activity_reasoning_tree(
        row,
    )

    row = materialize_activity_variable_tree(
        row,
    )

    row = materialize_activity_diagnostic_tree(
        row,
    )

    return row
