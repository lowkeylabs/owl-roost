# src/owlroost/cli/cmd_context.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace CLI.

Notes
-----
Owns workspace discovery,
selection, display, and
workspace-level operations.

Architectural Invariant
-----------------------

Workspace CLI owns:

    * Argument parsing
    * Selection
    * Validation
    * Display orchestration

Workspace subsystem owns:

    * Loading
    * Creation
    * Rename operations
    * Filesystem mutation
"""

from __future__ import annotations

import click

from owlroost.catalog.context import (
    build_catalog_context,
)
from owlroost.cli.utils import (
    parse_assist,
    render_available_views,
    render_table,
    resolve_renderer,
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
)
from owlroost.display.operations.sorting import (
    apply_canonical_sort,
    apply_sort,
)
from owlroost.workspace.loaders import (
    load_context_row,
)
from owlroost.workspace.materializers import (
    materialize_planning_context,
)


@click.command("workspace")
@click.pass_context
@click.option(
    "--view",
    default=None,
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
    type=str,
    help="Limit rows.",
)
@click.option(
    "--root",
    default=".",
    show_default=True,
    help="Workspace root folder.",
)
@click.option(
    "--pivot",
    is_flag=True,
    default=True,
    help="Display selected rows as a pivot table.",
)
@click.option(
    "--explain",
    type=str,
    default="variables",
    help=("Explanation facets. Use '.' for list."),
)
@click.option(
    "--assist",
    default="suggestions",
    callback=parse_assist,
    help=(
        "Append guide view(s).\n"
        "Examples:\n"
        "  --assist\n"
        "  --assist workflow\n"
        "  --assist suggestions,workflow"
    ),
)
def cmd_context(
    ctx,
    view,
    filters,
    sort,
    top,
    root,
    pivot,
    explain,
    assist,
):
    """
    Display the current planning context.
    """

    # =====================================================
    # Invocation
    # =====================================================

    level = "context"

    view = view or level

    explain_facets, explain_errors = parse_explain_request(
        explain,
    )

    # =====================================================
    # Catalog
    # =====================================================

    catalog = build_catalog_context()

    # =====================================================
    # Planning context
    # =====================================================

    row = materialize_planning_context(
        load_context_row(root),
        catalog,
    )

    rows = [row]

    # =====================================================
    # View validation
    # =====================================================

    if not catalog.display_registry.has_view_for_level(
        level,
        view,
    ):
        click.echo(f"Display view not found: {level}/{view}")

        render_available_views(
            catalog.display_registry,
            level=level,
        )

        return

    # =====================================================
    # Row operations
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

    if not rows:
        click.echo("No matching rows.")
        return

    # =====================================================
    # Display context
    # =====================================================

    table = materialize_view(
        rows=rows,
        registry=catalog.display_registry,
        catalog_index=catalog.catalog_index,
        level=level,
        mode="pivot" if pivot else "table",
        view_name=view,
        explain_facets=explain_facets,
        show_header=True,
        title="Here are details about your current directory.\n",
    )

    _output = render_table(
        table,
        resolve_renderer(
            False,
            False,
        ),
    )

    # =====================================================
    # Guidance
    # =====================================================

    for guide_view in assist:
        if not catalog.display_registry.has_view_for_level(
            "guide",
            guide_view,
        ):
            click.echo(f"Guide view not found: guide/{guide_view}")

            render_available_views(
                catalog.display_registry,
                level="guide",
            )

            continue

        print("")
        guide_table = materialize_view(
            rows=rows,
            registry=catalog.display_registry,
            catalog_index=catalog.catalog_index,
            level="guide",
            mode="pivot",
            view_name=guide_view,
            explain_facets=explain_facets,
            show_header=False,
        )

        guide_output = render_table(
            guide_table,
            resolve_renderer(
                False,
                False,
            ),
        )

        if guide_output:
            click.echo()
            click.echo(
                guide_output,
            )


#    print(rows)
