# src/owlroost/activity/engine.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning activity evaluation engine.

Notes
-----
Evaluates every registered planning
activity against the current planning
context.

Produces an ActivityEvaluation
describing activity readiness together
with evaluation coverage.

Current Implementation
----------------------
Activities currently transition between
READY and BLOCKED based solely upon
their semantic requirements.

Future implementations will also
consider prerequisite activities,
planning cadence, completion history,
and evidence freshness to produce
additional readiness states.
"""

from __future__ import annotations

from owlroost.display.operations.resolution import (
    resolve_field_value,
)

from .specs import (
    ActivityEvaluation,
    ActivityRecommendationState,
    ActivityResult,
    ActivityState,
    RequirementResult,
)

# =========================================================
# Operators
# =========================================================

OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "in": lambda a, b: a in b,
    "not in": lambda a, b: a not in b,
}

# =========================================================
# Evaluation
# =========================================================


def evaluate(
    *,
    row,
    registry,
):
    """
    Evaluate every registered planning
    activity.

    The evaluation proceeds in three
    phases:

        1. Determine readiness state.
        2. Determine recommendations.
        3. Compute evaluation coverage.
    """

    # =====================================================
    # Activity collections
    # =====================================================

    all_activities = []

    ready_activities = []

    waiting_activities = []

    blocked_activities = []

    needs_review_activities = []

    complete_activities = []

    not_applicable_activities = []

    next_activities = []

    upcoming_activities = []

    deferred_activities = []

    hidden_activities = []

    referenced_variables = set()

    # =====================================================
    # Phase 1
    #
    # Determine readiness.
    # =====================================================

    for activity in registry.activities():
        state = ActivityState.READY

        requirement_results = []

        for requirement in activity.requirements:
            referenced_variables.add(
                requirement.variable,
            )

            actual = resolve_field_value(
                row,
                requirement.variable,
            )

            op = OPS.get(
                requirement.operator,
            )

            if op is None:
                raise ValueError(f"Unknown activity operator: {requirement.operator!r}")

            satisfied = op(
                actual,
                requirement.value,
            )

            if not satisfied:
                state = ActivityState.BLOCKED

            requirement_results.append(
                RequirementResult(
                    requirement=requirement,
                    actual=actual,
                    satisfied=satisfied,
                )
            )

        #
        # Placeholder for future readiness
        # refinement.
        #
        # state = determine_readiness(...)
        #

        result = ActivityResult(
            activity=activity,
            state=state,
            requirement_results=requirement_results,
        )

        all_activities.append(
            result,
        )

        match state:
            case ActivityState.READY:
                ready_activities.append(
                    result,
                )

            case ActivityState.WAITING:
                waiting_activities.append(
                    result,
                )

            case ActivityState.BLOCKED:
                blocked_activities.append(
                    result,
                )

            case ActivityState.NEEDS_REVIEW:
                needs_review_activities.append(
                    result,
                )

            case ActivityState.COMPLETE:
                complete_activities.append(
                    result,
                )

            case ActivityState.NOT_APPLICABLE:
                not_applicable_activities.append(
                    result,
                )

    # =====================================================
    # Phase 2
    #
    # Determine recommendations.
    # =====================================================

    if ready_activities:
        first = ready_activities[0]

        first.recommendation = ActivityRecommendationState.NEXT

        next_activities.append(
            first,
        )

        for result in ready_activities[1:]:
            result.recommendation = ActivityRecommendationState.UPCOMING

            upcoming_activities.append(
                result,
            )

    #
    # Everything else is currently hidden.
    #
    # Future implementations may classify
    # activities as DEFERRED.
    #

    for result in (
        waiting_activities
        + blocked_activities
        + needs_review_activities
        + complete_activities
        + not_applicable_activities
    ):
        hidden_activities.append(
            result,
        )

    # =====================================================
    # Presentation order
    # =====================================================

    def sort_key(
        result,
    ):
        return (
            result.activity.display_order,
            result.activity.title.lower(),
        )

    for collection in (
        all_activities,
        ready_activities,
        waiting_activities,
        blocked_activities,
        needs_review_activities,
        complete_activities,
        not_applicable_activities,
        next_activities,
        upcoming_activities,
        deferred_activities,
        hidden_activities,
    ):
        collection.sort(
            key=sort_key,
        )

    # =====================================================
    # Coverage
    # =====================================================

    observed_variables = {key for key in row if not key.startswith("_")}

    unused_variables = observed_variables - referenced_variables

    # =====================================================
    # Sanity checks
    # =====================================================

    assert len(all_activities) == (
        len(ready_activities)
        + len(waiting_activities)
        + len(blocked_activities)
        + len(needs_review_activities)
        + len(complete_activities)
        + len(not_applicable_activities)
    )

    assert len(all_activities) == (
        len(next_activities)
        + len(upcoming_activities)
        + len(deferred_activities)
        + len(hidden_activities)
    )

    # =====================================================
    # Result
    # =====================================================

    return ActivityEvaluation(
        all_activities=all_activities,
        ready_activities=ready_activities,
        waiting_activities=waiting_activities,
        blocked_activities=blocked_activities,
        needs_review_activities=needs_review_activities,
        complete_activities=complete_activities,
        not_applicable_activities=not_applicable_activities,
        next_activities=next_activities,
        upcoming_activities=upcoming_activities,
        deferred_activities=deferred_activities,
        hidden_activities=hidden_activities,
        observed_variables=observed_variables,
        required_variables=referenced_variables,
        unused_variables=unused_variables,
    )
