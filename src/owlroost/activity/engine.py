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
describing both applicable and
rejected activities together with
evaluation coverage.
"""

from __future__ import annotations

from owlroost.display.operations.resolution import (
    resolve_field_value,
)

from .specs import (
    ActivityEvaluation,
    ActivityResult,
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
    #
    # Membership
    #
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
    Evaluate every registered activity
    """

    all_activities = []

    applicable_activities = []

    rejected_activities = []

    required_variables = set()

    # -----------------------------------------------------
    # Evaluate every registered activity.
    # -----------------------------------------------------

    for activity in registry.all():
        #
        # Activity applicability currently
        # reflects only semantic
        # requirements.
        #
        # Future implementations will also
        # consider prerequisite activities,
        # required scenario families, and
        # planning-cycle state.
        #
        #
        applicable = True

        requirement_results = []

        for requirement in activity.requirements:
            required_variables.add(
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
                applicable = False

            requirement_results.append(
                RequirementResult(
                    requirement=requirement,
                    actual=actual,
                    satisfied=satisfied,
                )
            )

        result = ActivityResult(
            activity=activity,
            applicable=applicable,
            requirement_results=requirement_results,
        )

        all_activities.append(
            result,
        )

        if applicable:
            applicable_activities.append(
                result,
            )
        else:
            rejected_activities.append(
                result,
            )

    # -----------------------------------------------------
    # Highest-priority guides first.
    # -----------------------------------------------------

    applicable_activities.sort(
        key=lambda r: (
            r.activity.display_order,
            r.activity.title.lower(),
        ),
    )

    rejected_activities.sort(
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
    # field is considered observed.
    # Future implementations should
    # derive observed semantic variables
    # from the catalog.
    #

    observed_variables = {key for key in row if not key.startswith("_")}

    unused_variables = observed_variables - required_variables

    return ActivityEvaluation(
        all_activities=all_activities,
        applicable_activities=applicable_activities,
        rejected_activities=rejected_activities,
        observed_variables=observed_variables,
        required_variables=required_variables,
        unused_variables=unused_variables,
    )
