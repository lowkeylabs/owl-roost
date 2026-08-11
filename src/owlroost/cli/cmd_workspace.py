# src/owlroost/cli/cmd_workspace.py
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

Workspace configuration is loaded and
composed by the workspace subsystem.

The CLI does not load, merge, validate,
or interpret workspace.toml directly.
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
    select_workspace_rows,
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
from owlroost.operations.resolve import (
    build_resolver,
)
from owlroost.workspace.levers.context import (
    workspace_initialized,
)
from owlroost.workspace.loaders import (
    load_workspace_row,
    load_workspace_rows,
)
from owlroost.workspace.materializers import (
    materialize_planning_context,
)
from owlroost.workspace.operations import (
    init_workspace,
    rename_workspace,
    sync_results_catalog,
)


@click.command("workspace")
@click.pass_context
@click.argument(
    "selectors",
    nargs=-1,
)
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
    "--rename",
    type=str,
    help="Rename selected workspace.",
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
    help="Display selected rows as a pivot table.",
)
@click.option(
    "--explain",
    type=str,
    help=("Explanation facets. Use '.' for list."),
)
@click.option(
    "--init",
    is_flag=True,
    help=("Initialize current directory as a workspace."),
)
@click.option(
    "--sync-results-catalog",
    "sync_results_catalog_flag",
    is_flag=True,
    help=("Refresh generated catalog files throughout the results tree."),
)
@click.option(
    "--force",
    is_flag=True,
)
@click.option(
    "--ignore",
    is_flag=True,
    help="Ignore workspace suitability checks.",
)
@click.option(
    "--publish",
    is_flag=True,
    help="Publish the current evidence package.",
)
@click.option(
    "--assist",
    flag_value="",
    help="Append guidance to display.",
)
@click.option(
    "--discover",
    is_flag=True,
    help="Append guidance to display.",
)
def cmd_workspace(
    ctx,
    selectors,
    view,
    filters,
    sort,
    top,
    rename,
    root,
    pivot,
    explain,
    init,
    sync_results_catalog_flag,
    force,
    ignore,
    assist,
    discover,
    publish,
):
    """
    List and manage workspaces.
    """

    # =====================================================
    # Invocation
    # =====================================================

    level = "context" if ctx.info_name == "." else "workspace"

    view = view or level

    explain_facets, explain_errors = parse_explain_request(
        explain,
    )

    # =====================================================
    # Immediate initialization
    # =====================================================
    #
    # Initialization is a filesystem operation.
    #
    # It intentionally occurs before catalog construction
    # and planning-context materialization.
    #

    if init:
        if (
            workspace_initialized(
                root,
            )
            and not force
        ):
            raise click.ClickException(
                "Current directory is already a workspace. Use --force to reinitialize."
            )

        workspace_dir = init_workspace(
            root,
            force=force,
        )

        click.echo(f"Initialized workspace: {workspace_dir}")

        return

    # =====================================================
    # Catalog
    # =====================================================

    catalog = build_catalog_context()

    # =====================================================
    # Current planning context
    # =====================================================

    planning_row = materialize_planning_context(
        load_workspace_row(
            root,
        ),
        catalog,
    )

    resolve = build_resolver(
        catalog,
        planning_row,
    )

    # =====================================================
    # Immediate workspace operations
    # =====================================================

    if publish:
        raise click.ClickException(
            "Workspace publishing requires "
            "materialized run rows and has "
            "not yet been connected to the "
            "canonical results-loading pipeline."
        )

    if sync_results_catalog_flag:
        sync_results_catalog(
            workspace_dir=root,
            force=force,
        )

        click.echo("Results catalog synchronized.")

        return

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
    # Build row set
    # =====================================================

    if resolve(
        "context.workspace.initialized",
    ):
        rows = load_workspace_rows(
            root,
        )

        if not rows:
            rows = [
                load_workspace_row(
                    root,
                )
            ]

    else:
        rows = [
            planning_row,
        ]

    rows = [
        materialize_planning_context(
            row,
            catalog,
        )
        for row in rows
    ]

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

    rows = attach_row_ids(
        rows,
    )

    if not rows:
        click.echo("No matching rows.")

        return

    # =====================================================
    # Selection
    # =====================================================

    selected_rows = select_workspace_rows(
        rows,
        selectors,
    )

    if not selected_rows:
        raise click.ClickException("No matching workspace selections.")

    # =====================================================
    # Rename
    # =====================================================

    if rename:
        if (
            len(
                selected_rows,
            )
            != 1
        ):
            raise click.ClickException("--rename requires exactly one workspace.")

        renamed = rename_workspace(
            selected_rows[0]["_path"],
            rename,
        )

        click.echo(f"Renamed workspace to: {renamed.name}")

        return

    # =====================================================
    # Display
    # =====================================================

    table = materialize_view(
        rows=selected_rows,
        registry=(catalog.display_registry),
        catalog_index=(catalog.catalog_index),
        level=level,
        mode=("pivot" if pivot else "table"),
        view_name=view,
        explain_facets=explain_facets,
    )

    if not pivot:
        table = inject_id_column(
            table,
        )

    output = render_table(
        table,
        resolve_renderer(
            False,
            False,
        ),
    )

    if output:
        click.echo(
            output,
        )
