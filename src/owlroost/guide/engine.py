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
suggestion against the current planning
context.

Produces a complete EvaluationResult
describing both applicable and rejected
suggestions together with evaluation
coverage.
"""

from __future__ import annotations

from owlroost.display.operations.resolution import (
    resolve_field_value,
)
from owlroost.guide.specs import (
    EvaluationResult,
    RequirementResult,
    SuggestionResult,
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
    Evaluate every registered guide suggestion.
    """

    all_results = []

    applicable_results = []

    rejected_results = []

    required_variables = set()

    #
    # Evaluate every suggestion.
    #
    for suggestion in registry.suggestions():
        applicable = True

        requirement_results = []

        for requirement in suggestion.requirements:
            required_variables.add(
                requirement.variable,
            )

            actual = resolve_field_value(
                row,
                requirement.variable,
            )

            satisfied = OPS[requirement.operator](
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

        result = SuggestionResult(
            suggestion=suggestion,
            applicable=applicable,
            requirement_results=requirement_results,
        )

        all_results.append(
            result,
        )

        if applicable:
            applicable_results.append(
                result,
            )
        else:
            rejected_results.append(
                result,
            )

    #
    # Highest priority first.
    #
    applicable_results.sort(
        key=lambda r: (
            r.suggestion.priority,
            r.suggestion.title,
        )
    )

    rejected_results.sort(
        key=lambda r: (
            r.suggestion.priority,
            r.suggestion.title,
        )
    )

    #
    # Coverage.
    #
    # We currently treat every row field as
    # "observed". Future versions will use
    # catalog metadata to distinguish
    # semantic variables from implementation
    # fields.
    #
    observed_variables = {k for k in row if not k.startswith("_")}

    unused_variables = observed_variables - required_variables

    return EvaluationResult(
        all_suggestions=all_results,
        applicable_suggestions=applicable_results,
        rejected_suggestions=rejected_results,
        observed_variables=observed_variables,
        required_variables=required_variables,
        unused_variables=unused_variables,
    )
