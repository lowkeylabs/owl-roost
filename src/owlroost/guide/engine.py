# src/owlroost/guide/engine.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide evaluation engine.

Notes
-----
Evaluates every registered workflow
guide against the current planning
context.

Produces a complete GuideEvaluation
describing both applicable and
rejected guides together with
evaluation coverage.
"""

from __future__ import annotations

from owlroost.display.operations.resolution import (
    resolve_field_value,
)
from owlroost.guide.specs import (
    GuideEvaluation,
    GuideResult,
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
    Evaluate every registered guide.
    """

    all_guides = []

    applicable_guides = []

    rejected_guides = []

    required_variables = set()

    # -----------------------------------------------------
    # Evaluate every registered guide.
    # -----------------------------------------------------

    for guide in registry.all():
        applicable = True

        requirement_results = []

        for requirement in guide.requirements:
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
                raise ValueError(f"Unknown guide operator: {requirement.operator!r}")

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

        result = GuideResult(
            guide=guide,
            applicable=applicable,
            requirement_results=requirement_results,
        )

        all_guides.append(
            result,
        )

        if applicable:
            applicable_guides.append(
                result,
            )
        else:
            rejected_guides.append(
                result,
            )

    # -----------------------------------------------------
    # Highest-priority guides first.
    # -----------------------------------------------------

    applicable_guides.sort(
        key=lambda r: (
            r.guide.priority,
            r.guide.title.lower(),
        ),
    )

    rejected_guides.sort(
        key=lambda r: (
            r.guide.priority,
            r.guide.title.lower(),
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

    return GuideEvaluation(
        all_guides=all_guides,
        applicable_guides=applicable_guides,
        rejected_guides=rejected_guides,
        observed_variables=observed_variables,
        required_variables=required_variables,
        unused_variables=unused_variables,
    )
