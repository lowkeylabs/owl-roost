# src/owlroost/cli/cmd_review.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Review retirement planning workflow.

Notes
-----
Provides the primary user-facing
workflow interface for ROOST.

Architectural Invariant
-----------------------

This command intentionally remains
thin.

Business logic belongs in:

    owlroost.review

Presentation belongs here.

Future versions will progressively
guide users through retirement
planning workflows while continuing
to use the same underlying Python
services available to notebooks,
Quarto, and other interfaces.
"""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from owlroost.review.service import (
    review,
)

console = Console()


@click.command(
    name="review",
    help=("Guide a retirement planning review."),
)
@click.argument(
    "path",
    required=False,
    default=".",
)
def cmd_review(
    path: str,
):
    """
    Review the current household
    and recommend next steps.
    """

    observations = review(
        Path(path),
    )

    console.print()

    console.print("[bold]ROOST Review[/bold]")

    console.print(f"Folder : {observations['root']}")

    console.print(f"Household : {'✓' if observations['household_found'] else '✗'}")

    console.print(f"Workspace : {'✓' if observations['workspace_found'] else '✗'}")

    console.print()

    console.print("[bold]Next Step[/bold]")

    console.print(
        observations["next_step"],
    )

    console.print()
