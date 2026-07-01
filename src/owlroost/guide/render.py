# src/owlroost/guide/render.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide rendering.

Notes
-----
Provides lightweight rendering of
workflow guidance.

Rendering consumes EvaluationResult
objects produced by the guide engine.
"""

from __future__ import annotations

from owlroost.guide.specs import (
    EvaluationResult,
)

# =========================================================
# Welcome Screen
# =========================================================


def render_welcome(
    registry,
):
    """
    Render the ROOST welcome screen.
    """

    lines = []

    lines.append("")
    lines.append("ROOST")
    lines.append("")
    lines.append("Retirement Options and Outcomes Studies Tool.")
    lines.append("")
    lines.append("Common starting points:")
    lines.append("")

    for suggestion in registry.suggestions():
        if suggestion.command is None:
            continue

        lines.append(f"  {suggestion.command:<24}{suggestion.description}")

    lines.append("")

    return "\n".join(lines)


# =========================================================
# Context Rendering
# =========================================================


def render_context(
    evaluation: EvaluationResult,
    *,
    explain_suggestions=False,
    explain_coverage=False,
):
    """
    Render context-sensitive guidance.
    """

    lines = []

    #
    # -----------------------------------------------------
    # Suggested next steps
    # -----------------------------------------------------
    #

    lines.append("Suggested next steps")
    lines.append("--------------------")
    lines.append("")

    shown = False

    for result in evaluation.suggestions:
        if not result.applicable:
            continue

        suggestion = result.suggestion

        if suggestion.command is None:
            continue

        shown = True

        lines.append(f"  {suggestion.command:<28}{suggestion.description}")

    if not shown:
        lines.append("  No suggestions available.")

    #
    # -----------------------------------------------------
    # Suggestion explanations
    # -----------------------------------------------------
    #

    if explain_suggestions:
        lines.append("")
        lines.append("")
        lines.append("Suggestion Evaluation")
        lines.append("---------------------")
        lines.append("")

        for result in evaluation.suggestions:
            status = "✓" if result.applicable else "✗"

            suggestion = result.suggestion

            lines.append(f"{status} {suggestion.title}")

            if suggestion.command:
                lines.append(f"    Command: {suggestion.command}")

            if suggestion.description:
                lines.append(f"    {suggestion.description}")

            if result.requirement_results:
                lines.append("")
                lines.append("    Requirements:")

                for req in result.requirement_results:
                    r = req.requirement

                    mark = "✓" if req.satisfied else "✗"

                    lines.append(f"      {mark} {r.variable} {r.operator} {r.value!r}")

                    lines.append(f"           actual = {req.actual_value!r}")

            lines.append("")

    #
    # -----------------------------------------------------
    # Coverage
    # -----------------------------------------------------
    #

    if explain_coverage:
        lines.append("")
        lines.append("")
        lines.append("Guide Coverage")
        lines.append("--------------")
        lines.append("")

        lines.append(f"Observed variables:   {len(evaluation.observed_variables)}")

        lines.append(f"Referenced variables: {len(evaluation.referenced_variables)}")

        lines.append(f"Unused variables:     {len(evaluation.unused_variables)}")

        if evaluation.unused_variables:
            lines.append("")
            lines.append("Variables with no guide coverage:")

            for variable in sorted(evaluation.unused_variables):
                lines.append(f"    {variable}")

    return "\n".join(lines)
