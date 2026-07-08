# src/owlroost/cli/cmd_household.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household CLI.

Notes
-----
Owns discovery, selection,
query, and display of
registered Household Projects.

Architectural Invariants
------------------------

Household CLI owns:

    * argument parsing
    * row selection
    * display orchestration

Household subsystem owns:

    * discovery
    * registry construction
    * manifest loading
    * filesystem inspection
"""

from __future__ import annotations

from pathlib import Path

import click

from owlroost.catalog.context import (
    build_catalog_context,
)
from owlroost.cli.utils import (
    render_available_views,
    render_table,
    resolve_renderer,
    select_rows_by_id,
)
from owlroost.display.explain import (
    parse_explain_request,
)
from owlroost.display.materializers.materialize import (
    materialize_view,
)
from owlroost.display.operations.filtering import (
    apply_filters,
)
from owlroost.display.operations.row_ops import (
    apply_top,
    attach_row_ids,
)
from owlroost.display.operations.sorting import (
    apply_canonical_sort,
    apply_sort,
)
from owlroost.display.operations.table_ops import (
    inject_id_column,
)
from owlroost.household.bootstrap import (
    build_household_registry,
)
from owlroost.household.loaders import (
    load_household_rows,
)
from owlroost.household.operations import (
    export_case,
)

DEFAULT_LEVEL = "household"

DEFAULT_VIEW = "household"


@click.command("household")
@click.argument(
    "selectors",
    nargs=-1,
)
@click.option(
    "--view",
    default=DEFAULT_VIEW,
    show_default=True,
)
@click.option(
    "--markdown",
    is_flag=True,
)
@click.option(
    "--latex",
    is_flag=True,
)
@click.option(
    "--filter",
    "filters",
    multiple=True,
    help="Filter rows.",
)
@click.option(
    "--sort",
    type=str,
    help="Sort by field.",
)
@click.option(
    "--top",
    type=int,
    help="Limit number of rows.",
)
@click.option(
    "--pivot",
    is_flag=True,
    help="Display selected rows as a pivot table.",
)
@click.option(
    "--explain",
    type=str,
    help="Explanation facets.",
)
@click.option(
    "--export",
    is_flag=True,
    help=("Export selected households into the current workspace."),
)
def cmd_household(
    selectors,
    view,
    markdown,
    latex,
    filters,
    sort,
    top,
    pivot,
    explain,
    export,
):
    """
    Browse registered Household Projects.

    Examples
    --------

    List households

        roost household

    Inspect one household

        roost household 0

    Filter households

        roost household --filter tags=tutorial

    Pivot display

        roost household 0 --pivot
    """

    explain_facets, explain_errors = parse_explain_request(
        explain,
    )

    if explain_errors:
        raise click.BadParameter(
            "\n".join(
                explain_errors,
            )
        )

    if explain_facets and not pivot:
        raise click.BadParameter("--explain requires --pivot")

    # =====================================================
    # Context
    # =====================================================

    catalog = build_catalog_context()

    household_registry = build_household_registry()

    # =====================================================
    # Validate view
    # =====================================================

    if not catalog.display_registry.has_view_for_level(
        DEFAULT_LEVEL,
        view,
    ):
        click.echo(f"Display view not found: {DEFAULT_LEVEL}/{view}")

        render_available_views(
            catalog.display_registry,
            level=DEFAULT_LEVEL,
        )

        return

    # =====================================================
    # Load rows
    # =====================================================

    rows = load_household_rows(
        household_registry,
    )

    # =====================================================
    # Row pipeline
    # =====================================================

    rows = apply_canonical_sort(
        rows,
    )

    rows = apply_filters(
        rows,
        filters,
    )

    rows = apply_sort(
        rows,
        sort,
    )

    rows = apply_top(
        rows,
        top,
    )

    rows = attach_row_ids(
        rows,
    )

    if not rows:
        click.echo("No households found.")
        return

    # =====================================================
    # Selection
    # =====================================================

    if selectors:
        rows = select_rows_by_id(
            rows,
            selectors,
        )

        if not rows:
            raise click.ClickException("No matching household selections.")

    if export:
        destination = Path(".")

        failures = []

        for row in rows:
            household = household_registry.get_household(
                row["household.global_id"],
            )

            try:
                export_case(
                    household,
                    destination,
                )

                click.echo(f"Exported {household.global_id}")

            except FileExistsError:
                failures.append(
                    (
                        household.global_id,
                        "already exists",
                    )
                )

            except Exception as exc:
                failures.append(
                    (
                        household.global_id,
                        str(exc),
                    )
                )

        if failures:
            click.echo()

            click.echo("Some households could not be exported:")

            for household_id, message in failures:
                click.echo(f"  {household_id}: {message}")

        return

    # =====================================================
    # Renderer
    # =====================================================

    renderer = resolve_renderer(
        markdown,
        latex,
    )

    # =====================================================
    # Display
    # =====================================================

    table = materialize_view(
        rows=rows,
        registry=catalog.display_registry,
        catalog_index={},
        level=DEFAULT_LEVEL,
        view_name=view,
        mode="pivot" if pivot else "table",
        explain_facets=explain_facets,
    )

    if not pivot:
        table = inject_id_column(
            table,
            rows,
        )

    output = render_table(
        table,
        renderer,
    )

    if output:
        click.echo(
            output,
        )
