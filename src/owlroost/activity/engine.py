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
    Evaluate every registered activity.
    """

    all_activities = []

    ready_activities = []

    waiting_activities = []

    blocked_activities = []

    needs_review_activities = []

    complete_activities = []

    not_applicable_activities = []

    referenced_variables = set()

    # -----------------------------------------------------
    # Evaluate every registered activity.
    # -----------------------------------------------------

    for activity in registry.all():
        #
        # Determine the current readiness
        # state for this activity.
        #
        # The current implementation uses
        # only semantic requirements.
        #
        # Future implementations will also
        # consider:
        #
        #     * prerequisite activities
        #     * planning cadence
        #     * completion history
        #     * evidence freshness
        #
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
        # Future readiness refinement.
        #
        # state = determine_readiness(
        #     activity,
        #     state,
        #     row,
        #     requirement_results,
        # )
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

    # -----------------------------------------------------
    # Presentation order.
    # -----------------------------------------------------

    all_activities.sort(
        key=lambda r: (
            r.activity.display_order,
            r.activity.title.lower(),
        ),
    )

    for collection in (
        ready_activities,
        waiting_activities,
        blocked_activities,
        needs_review_activities,
        complete_activities,
        not_applicable_activities,
    ):
        collection.sort(
            key=lambda r: (
                r.activity.display_order,
                r.activity.title.lower(),
            ),
        )

    # -----------------------------------------------------
    # Coverage
    # -----------------------------------------------------
    #
    # Currently every non-private row
    # field is treated as an observed
    # semantic variable.
    #
    # Future implementations should
    # derive semantic coverage directly
    # from the catalog.
    #

    observed_variables = {key for key in row if not key.startswith("_")}

    unused_variables = observed_variables - referenced_variables

    return ActivityEvaluation(
        all_activities=all_activities,
        ready_activities=ready_activities,
        waiting_activities=waiting_activities,
        blocked_activities=blocked_activities,
        needs_review_activities=needs_review_activities,
        complete_activities=complete_activities,
        not_applicable_activities=not_applicable_activities,
        observed_variables=observed_variables,
        required_variables=referenced_variables,
        unused_variables=unused_variables,
    )
