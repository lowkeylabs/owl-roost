# src/owlroost/cli/help.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
CLI discovery and help workflow.

Notes
-----
Provides a common discovery model
shared across CLI commands.

Architectural Invariant
-----------------------

A single period (".") requests
context-sensitive discovery for the
current argument position.

Examples
--------

    roost cases .
    roost cases --view .
    roost cases --filter .
    roost cases --sort .
"""

from __future__ import annotations

import click

from owlroost.cli.utils import (
    render_available_views,
)
from owlroost.display.operations.help import (
    render_field_help,
    render_override_help,
)

# =========================================================
# Discovery Detection
# =========================================================


def wants_help(
    value,
) -> bool:
    """
    Return True when help/discovery
    was requested.
    """

    if value is None:
        return False

    if value in (
        ".",
        "help",
    ):
        return True

    if isinstance(
        value,
        (list, tuple, set),
    ):
        return "." in value or "help" in value

    return False


# =========================================================
# Simple Renderers
# =========================================================


def render_selector_help():
    """
    Render selector syntax help.
    """

    click.echo()
    click.echo("Case Selectors")
    click.echo()

    click.echo("Selectors reference the ID column shown by the default case listing.")

    click.echo()

    click.echo("Examples:")
    click.echo()

    click.echo("  roost cases 0")
    click.echo("  roost cases 0,5,7")
    click.echo("  roost cases 0-10")
    click.echo("  roost cases 0,2,5-8")

    click.echo()


def render_top_help():
    """
    Render top syntax help.
    """

    click.echo()
    click.echo("Top Syntax")
    click.echo()

    click.echo("Limit displayed rows.")

    click.echo()

    click.echo("Examples:")
    click.echo()

    click.echo("  --top 5")
    click.echo("  --top 10")
    click.echo("  --top 25")

    click.echo()


def render_explain_help():
    """
    Render explain facet help.
    """

    click.echo()
    click.echo("Available explain facets:")
    click.echo()

    for facet in [
        "variables",
        "values",
        "sources",
        "display",
        "ontology",
        "provenance",
        "debug",
        "all",
    ]:
        click.echo(f"  {facet}")

    click.echo()


# =========================================================
# Dispatcher
# =========================================================


def process_help_requests(
    *,
    selectors,
    overrides,
    help_requests,
    view,
    explain,
    filters,
    sort,
    top,
    rows,
    display_registry,
    schema_registry,
    level,
):
    """
    Process contextual help requests.

    Returns
    -------
    bool

        True
            Help rendered.

        False
            Continue command execution.
    """

    # =====================================================
    # Positional CLI help
    #
    # Examples:
    #
    #   roost build .
    #       -> selector help
    #
    #   roost build 0 .
    #       -> override help
    #
    #   roost build 0,5,7 .
    #       -> override help
    # =====================================================

    if help_requests:
        if selectors:
            render_override_help(overrides, help_requests, schema_registry)
        else:
            render_selector_help()

        return True

    # =====================================================
    # View help
    # =====================================================

    if wants_help(
        view,
    ):
        render_available_views(
            display_registry,
            level=level,
        )

        return True

    # =====================================================
    # Explain help
    # =====================================================

    if wants_help(
        explain,
    ):
        render_explain_help()

        return True

    # =====================================================
    # Filter help
    # =====================================================

    if wants_help(
        filters,
    ):
        render_field_help(
            rows=rows,
            registry=display_registry,
            level=level,
            view_name=view,
            mode="view",
            title="Available filter fields",
            examples=[
                "--filter id=in:1,2,3",
                "--filter display.total_savings>2000000",
                "--filter optimization_parameters.objective=maxBequest",
                "--filter rates_selection.method=user",
            ],
        )

        return True

    # =====================================================
    # Sort help
    # =====================================================

    if wants_help(
        sort,
    ):
        render_field_help(
            rows=rows,
            registry=display_registry,
            level=level,
            view_name=view,
            mode="view",
            title="Available sort fields",
            examples=[
                "--sort display.total_savings",
                "--sort -display.total_savings",
                "--sort display.fixed_income",
            ],
        )

        return True

    # =====================================================
    # Top help
    # =====================================================

    if wants_help(
        top,
    ):
        render_top_help()

        return True

    return False
