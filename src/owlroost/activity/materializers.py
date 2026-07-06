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
    """

    activity = {
        "summary": {
            "activity_count": evaluation.activity_count,
            "actionable_count": evaluation.ready_count,
            "ready_count": evaluation.ready_count,
            "blocked_count": evaluation.blocked_count,
            "needs_review_count": len(
                evaluation.needs_review_activities,
            ),
            "not_applicable_count": len(
                evaluation.not_applicable_activities,
            ),
            "top_activity": (
                evaluation.actionable_activities[0].activity.title
                if evaluation.actionable_activities
                else None
            ),
            "has_actionable": bool(
                evaluation.actionable_activities,
            ),
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
        },
        "_objects": {},
    }

    for activity_result in evaluation.all_activities:
        activity_spec = activity_result.activity

        activity["_objects"][activity_spec.name] = activity_spec

        activity["_objects"][f"{activity_spec.name}.result"] = activity_result

        for i, requirement_result in enumerate(
            activity_result.requirement_results,
        ):
            activity["_objects"][f"{activity_spec.name}.requirement.{i}"] = requirement_result

        #
        # Only actionable activities are
        # materialized into the semantic
        # namespace.
        #
        if activity_result.is_ready:
            current = activity

            for part in activity_spec.name.split(".")[:-1]:
                current = current.setdefault(
                    part,
                    {},
                )

            current[activity_spec.name.split(".")[-1]] = activity_spec.suggested_commands

    return activity


# =========================================================
# Activity Materialization
# =========================================================


def materialize_activity(
    row,
    registry,
):
    """
    Attach activity evaluation and
    semantic activity namespace.
    """

    evaluation = registry.evaluate(
        row=row,
    )

    row["_activity_eval"] = evaluation

    row["_activity"] = _build_activity_namespace(
        evaluation,
    )

    return row


# =========================================================
# Guide Tree Materialization
# =========================================================


def materialize_activity_next_tree(
    row,
):
    """
    Materialize actionable planning
    activities.
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
        for result in evaluation.actionable_activities:
            activity = result.activity

            tree["children"].append(
                {
                    "kind": "section",
                    "label": activity.title,
                    "field": (f"activity.{activity.name}"),
                    "children": [],
                }
            )

    row["_activity_next"] = tree

    return row


def materialize_activity_detail_tree(
    row,
):
    """
    Materialize detailed information
    for actionable activities.
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
        for result in evaluation.actionable_activities:
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
    Materialize activity readiness.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Readiness",
        "children": [],
    }

    if evaluation is not None:
        sections = [
            (
                "Ready",
                evaluation.ready_activities,
            ),
            (
                "Blocked",
                evaluation.blocked_activities,
            ),
            (
                "Needs Review",
                evaluation.needs_review_activities,
            ),
            (
                "Not Applicable",
                evaluation.not_applicable_activities,
            ),
        ]

        for label, results in sections:
            node = {
                "kind": "section",
                "label": label,
                "children": [],
            }

            for result in results:
                node["children"].append(
                    {
                        "kind": "section",
                        "label": result.activity.title,
                        "children": [],
                    }
                )

            tree["children"].append(
                node,
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
                                "label": "State",
                                "field": (f"activity.{activity.name}.result.state"),
                                "children": [],
                            },
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
    """

    tree = {
        "kind": "section",
        "label": "Activity Diagnostics",
        "children": [
            {
                "kind": "section",
                "label": "Activities",
                "field": ("activity.summary.activity_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Actionable",
                "field": ("activity.summary.actionable_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Ready",
                "field": ("activity.summary.ready_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Blocked",
                "field": ("activity.summary.blocked_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Needs Review",
                "field": ("activity.summary.needs_review_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Not Applicable",
                "field": ("activity.summary.not_applicable_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Required Variables",
                "field": ("activity.summary.required_variable_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Observed Variables",
                "field": ("activity.summary.observed_variable_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Unused Variables",
                "field": ("activity.summary.unused_variable_count"),
                "children": [],
            },
        ],
    }

    row["_activity_diagnostics"] = tree

    return row


def materialize_activity_workflow_tree(
    row,
):
    """
    Materialize the retirement
    planning workflow.

    Activities are organized by
    category and ordered according
    to their display order.

    The workflow shows each activity's
    readiness rather than only those
    that are currently actionable.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Planning Workflow",
        "children": [],
    }

    if evaluation is None:
        row["_activity_workflow"] = tree
        return row

    #
    # Build quick lookup.
    #
    results = {result.activity.name: result for result in evaluation.all_activities}

    #
    # Categories appear in workflow order.
    #
    categories = [
        ("Workspace", "WORKSPACE"),
        ("Households", "HOUSEHOLD"),
        ("Annual Review", "REVIEW"),
        ("Planning Decisions", "DECISION"),
        ("Reporting", "REPORTING"),
        ("General", "GENERAL"),
    ]

    for label, enum_name in categories:
        category_node = {
            "kind": "section",
            "label": label,
            "children": [],
        }

        for result in sorted(
            (r for r in results.values() if r.activity.category.name == enum_name),
            key=lambda r: (
                r.activity.display_order,
                r.activity.title.lower(),
            ),
        ):
            #
            # Readiness label.
            #

            if result.is_ready:
                state = "▶"

            elif result.needs_review:
                state = "↺"

            elif result.is_blocked:
                state = "○"

            elif result.is_complete:
                state = "✓"

            else:
                state = "—"

            category_node["children"].append(
                {
                    "kind": "section",
                    "label": (f"{state} {result.activity.title}"),
                    "field": (f"activity.{result.activity.name}" if result.is_ready else None),
                    "children": [],
                }
            )

        if category_node["children"]:
            tree["children"].append(
                category_node,
            )

    row["_activity_workflow"] = tree

    return row


def materialize_activity_trees(
    row,
):
    """
    Materialize every activity tree.
    """

    row = materialize_activity_next_tree(
        row,
    )

    row = materialize_activity_detail_tree(
        row,
    )

    row = materialize_activity_status_tree(
        row,
    )

    row = materialize_activity_workflow_tree(
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
