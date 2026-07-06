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

    The namespace contains:

        summary

            Aggregate activity
            statistics.

        _objects

            Semantic object registry
            supporting property
            resolution.

        activity hierarchy

            Recommended activities
            exposed through their
            semantic names.
    """

    activity = {
        "summary": {
            "activity_count": evaluation.activity_count,
            "ready_count": evaluation.ready_count,
            "blocked_count": evaluation.blocked_count,
            "next_count": len(
                evaluation.next_activities,
            ),
            "upcoming_count": len(
                evaluation.upcoming_activities,
            ),
            "recommended_count": len(
                evaluation.recommended_activities,
            ),
            "needs_review_count": len(
                evaluation.needs_review_activities,
            ),
            "not_applicable_count": len(
                evaluation.not_applicable_activities,
            ),
            "top_activity": (
                evaluation.next_activity.activity.title if evaluation.next_activity else None
            ),
            "has_next": (evaluation.next_activity is not None),
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

    #
    # Register every semantic object.
    #

    for activity_result in evaluation.all_activities:
        activity_spec = activity_result.activity

        activity["_objects"][activity_spec.name] = activity_spec

        activity["_objects"][f"{activity_spec.name}.result"] = activity_result

        for i, requirement_result in enumerate(
            activity_result.requirement_results,
        ):
            activity["_objects"][f"{activity_spec.name}.requirement.{i}"] = requirement_result

    #
    # Expose recommended activities
    # through the semantic namespace.
    #

    for activity_result in evaluation.recommended_activities:
        activity_spec = activity_result.activity

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
    Materialize planning activity
    information onto a planning
    context.

    Produces two complementary
    representations.

        _activity_eval

            Rich ActivityEvaluation
            consumed by reasoning,
            workflow analysis, and
            future planning logic.

        _activity

            Semantic namespace used by
            the display subsystem.
    """

    #
    # Evaluate every registered
    # planning activity.
    #

    evaluation = registry.evaluate(
        row=row,
    )

    row["_activity_eval"] = evaluation

    #
    # Build the semantic namespace
    # consumed by display and field
    # resolution.
    #

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
    Materialize the next recommended
    planning activities.

    These are the activities currently
    recommended for immediate
    attention.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Suggested Activities",
        "children": [],
    }

    if evaluation is None:
        row["_activity_next"] = tree
        return row

    for result in evaluation.next_activities:
        activity = result.activity

        tree["children"].append(
            {
                "kind": "section",
                "label": activity.title,
                "field": f"activity.{activity.name}",
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
    for recommended planning
    activities.

    Includes both next and upcoming
    activities.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Details",
        "children": [],
    }

    if evaluation is None:
        row["_activity_details"] = tree
        return row

    for result in evaluation.next_activities + evaluation.upcoming_activities:
        activity = result.activity

        children = [
            {
                "kind": "section",
                "label": "Description",
                "field": (f"activity.{activity.name}.description"),
                "children": [],
            },
        ]

        if activity.suggested_commands:
            children.append(
                {
                    "kind": "section",
                    "label": "Suggested Commands",
                    "field": (f"activity.{activity.name}.suggested_commands"),
                    "children": [],
                }
            )

        if activity.prerequisite_activities:
            children.append(
                {
                    "kind": "section",
                    "label": "Prerequisites",
                    "field": (f"activity.{activity.name}.prerequisite_activities"),
                    "children": [],
                }
            )

        if activity.required_scenario_families:
            children.append(
                {
                    "kind": "section",
                    "label": "Scenario Families",
                    "field": (f"activity.{activity.name}.required_scenario_families"),
                    "children": [],
                }
            )

        tree["children"].append(
            {
                "kind": "section",
                "label": activity.title,
                "field": (f"activity.{activity.name}"),
                "children": children,
            }
        )

    row["_activity_details"] = tree

    return row


def materialize_activity_status_tree(
    row,
):
    """
    Materialize current activity
    readiness.

    Every activity appears exactly
    once according to its current
    readiness state.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Readiness",
        "children": [],
    }

    if evaluation is None:
        row["_activity_status"] = tree
        return row

    sections = [
        (
            "Ready",
            evaluation.ready_activities,
        ),
        (
            "Waiting",
            evaluation.waiting_activities,
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
            "Complete",
            evaluation.complete_activities,
        ),
        (
            "Not Applicable",
            evaluation.not_applicable_activities,
        ),
    ]

    for label, results in sections:
        if not results:
            continue

        node = {
            "kind": "section",
            "label": label,
            "children": [],
        }

        for result in results:
            activity = result.activity

            node["children"].append(
                {
                    "kind": "section",
                    "label": activity.title,
                    "field": (f"activity.{activity.name}.state"),
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
    Materialize activity evaluation
    reasoning.

    Shows the readiness state,
    recommendation, and requirement
    evaluation used to determine the
    current planning status.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Reasoning",
        "children": [],
    }

    if evaluation is None:
        row["_activity_reasoning"] = tree
        return row

    for result in evaluation.all_activities:
        activity = result.activity

        activity_node = {
            "kind": "section",
            "label": activity.title,
            "children": [
                {
                    "kind": "section",
                    "label": "State",
                    "field": (f"activity.{activity.name}.result.state"),
                    "children": [],
                },
                {
                    "kind": "section",
                    "label": "Recommendation",
                    "field": (f"activity.{activity.name}.result.recommendation"),
                    "children": [],
                },
            ],
        }

        if result.requirement_results:
            requirements_node = {
                "kind": "section",
                "label": "Requirements",
                "children": [],
            }

            for i, requirement in enumerate(
                result.requirement_results,
            ):
                prefix = f"activity.{activity.name}.requirement.{i}"

                requirements_node["children"].append(
                    {
                        "kind": "section",
                        "label": (requirement.requirement.variable),
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

            activity_node["children"].append(
                requirements_node,
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
    referenced during activity
    evaluation.
    """

    evaluation = row.get(
        "_activity_eval",
    )

    tree = {
        "kind": "section",
        "label": "Activity Variables",
        "children": [],
    }

    if evaluation is None:
        row["_activity_variables"] = tree
        return row

    for variable in sorted(
        evaluation.required_variables,
    ):
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
    Materialize activity evaluation
    diagnostics.
    """

    tree = {
        "kind": "section",
        "label": "Activity Diagnostics",
        "children": [
            #
            # Activity counts
            #
            {
                "kind": "section",
                "label": "Activities",
                "field": ("activity.summary.activity_count"),
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
                "label": "Waiting",
                "field": ("activity.summary.waiting_count"),
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
                "label": "Complete",
                "field": ("activity.summary.complete_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Not Applicable",
                "field": ("activity.summary.not_applicable_count"),
                "children": [],
            },
            #
            # Recommendation counts
            #
            {
                "kind": "section",
                "label": "Next",
                "field": ("activity.summary.next_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Upcoming",
                "field": ("activity.summary.upcoming_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Deferred",
                "field": ("activity.summary.deferred_count"),
                "children": [],
            },
            {
                "kind": "section",
                "label": "Hidden",
                "field": ("activity.summary.hidden_count"),
                "children": [],
            },
            #
            # Coverage
            #
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
    planning category.

    Icons represent recommendation
    status rather than evaluation
    state.

    This answers:

        "What should I do next?"
    """

    from owlroost.activity.specs import (
        ActivityCategory,
    )

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

    categories = [
        (ActivityCategory.WORKSPACE, "Workspace"),
        (ActivityCategory.HOUSEHOLD, "Households"),
        (ActivityCategory.REVIEW, "Annual Review"),
        (ActivityCategory.DECISION, "Planning Decisions"),
        (ActivityCategory.REPORTING, "Reporting"),
        (ActivityCategory.GENERAL, "General"),
    ]

    for category, label in categories:
        results = [
            result for result in evaluation.all_activities if result.activity.category == category
        ]

        if not results:
            continue

        results.sort(
            key=lambda result: (
                result.activity.display_order,
                result.activity.title.lower(),
            ),
        )

        category_node = {
            "kind": "section",
            "label": label,
            "children": [],
        }

        for result in results:
            #
            # Recommendation icon.
            #

            if result.is_next:
                icon = "▶"

            elif result.is_upcoming:
                icon = "•"

            elif result.is_deferred:
                icon = "⏸"

            elif result.is_hidden:
                icon = " "

            else:
                icon = " "

            #
            # Completion badge.
            #

            if result.is_complete:
                badge = "✓ "

            elif result.needs_review:
                badge = "↺ "

            else:
                badge = ""

            category_node["children"].append(
                {
                    "kind": "section",
                    "label": (f"{badge}{icon} {result.activity.title}"),
                    "field": (f"activity.{result.activity.name}"),
                    "children": [],
                }
            )

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
