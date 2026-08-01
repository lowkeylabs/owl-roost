# src/owlroost/cli/cmd_study.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study CLI.

Notes
-----
Owns discovery, selection,
query, and display of
registered Studies and
Experiments.

Architectural Invariants
------------------------

Study CLI owns:

    * argument parsing
    * row selection
    * display orchestration

Study subsystem owns:

    * registry construction
    * study definitions
    * experiment definitions
    * row construction
"""

from __future__ import annotations

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
from owlroost.study.loaders import (
    load_study_rows,
)

DEFAULT_LEVEL = "study"

DEFAULT_VIEW = "study"


@click.command("study")
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
def cmd_study(
    selectors,
    view,
    markdown,
    latex,
    filters,
    sort,
    top,
    pivot,
):
    """
    Browse registered studies and
    experiments.

    Examples
    --------

    List studies

        roost study

    Inspect one study

        roost study 0

    Filter studies

        roost study --filter study.name=market

    Pivot display

        roost study --pivot
    """

    # =====================================================
    # Context
    # =====================================================

    catalog = build_catalog_context()

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

    rows = load_study_rows(
        catalog.study_registry,
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
        click.echo("No studies found.")
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
            raise click.ClickException("No matching study selections.")

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
        catalog_index=catalog.catalog_index,
        level=DEFAULT_LEVEL,
        view_name=view,
        mode="pivot" if pivot else "table",
    )

    if not pivot:
        table = inject_id_column(
            table,
        )

    output = render_table(
        table,
        renderer,
    )

    if output:
        click.echo(
            output,
        )
