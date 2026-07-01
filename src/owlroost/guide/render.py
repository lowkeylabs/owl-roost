# src/owlroost/guide/render.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide rendering.

Notes
-----
Provides simple rendering helpers for
guide suggestions.

Presentation is intentionally lightweight.
Future versions may delegate rendering
to the display subsystem.
"""

from __future__ import annotations


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

    return "\n".join(
        lines,
    )
