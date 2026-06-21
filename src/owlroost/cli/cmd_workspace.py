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
from owlroost.workspace.loaders import (
    load_workspace_row,
    load_workspace_rows,
)
from owlroost.workspace.operations import (
    create_workspace,
    init_workspace,
    rename_workspace,
    sync_results_catalog,
)

DEFAULT_LEVEL = "workspace"
DEFAULT_VIEW = "workspace"


@click.command("workspace")
@click.argument(
    "selectors",
    nargs=-1,
)
@click.option(
    "--view",
    default=None,
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
    type=str,
    help="Limit rows.",
)
@click.option(
    "--create",
    type=str,
    help="Create new workspace.",
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
    help="Initialize current directory as a workspace.",
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
def cmd_workspace(
    selectors,
    view,
    markdown,
    latex,
    filters,
    sort,
    top,
    create,
    rename,
    root,
    pivot,
    explain,
    init,
    sync_results_catalog_flag,
    force,
):
    """
    List and manage workspaces.

    Examples
    --------

    List workspaces:

        roost workspace

    Show workspace:

        roost workspace 0

    Create workspace:

        roost workspace --create foo

    Rename workspace:

        roost workspace 0 --rename bar
    """

    if view is None:
        view = DEFAULT_VIEW

    explain_facets, explain_errors = parse_explain_request(
        explain,
    )

    # =====================================================
    # Immediate operations
    # =====================================================

    if create:
        workspace_dir = create_workspace(
            create,
            parent=root,
        )

        click.echo(f"Created workspace: {workspace_dir}")

        return

    if init:
        workspace_dir = init_workspace(
            root,
            force=force,
        )

        click.echo(f"Initialized workspace: {workspace_dir}")

        return

    if sync_results_catalog_flag:
        sync_results_catalog(
            workspace_dir=root,
            force=force,
        )

        click.echo("Results catalog synchronized.")

        return

    # =====================================================
    # Context
    # =====================================================

    (
        schema_registry,
        metrics_registry,
        display_registry,
        catalog_rows,
        catalog_index,
    ) = build_catalog_context()

    # =====================================================
    # Validate view
    # =====================================================

    level = DEFAULT_LEVEL

    if not display_registry.has_view_for_level(
        level,
        view,
    ):
        click.echo(f"Display view not found: {level}/{view}")

        render_available_views(
            display_registry,
            level=level,
        )

        return

    # =====================================================
    # Load rows
    # =====================================================

    rows = load_workspace_rows(
        root,
    )

    if not rows:
        rows = [load_workspace_row(".")]

        if not rows:
            print("No workspaces found in subfolders or this folder")
            return

    rows = apply_canonical_sort(
        rows,
    )

    print(rows)

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
        click.echo("No workspaces found.")

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
        if len(selected_rows) != 1:
            raise click.ClickException("--rename requires exactly one workspace.")

        workspace_path = selected_rows[0]["_path"]

        renamed = rename_workspace(
            workspace_path,
            rename,
        )

        click.echo(f"Renamed workspace to: {renamed.name}")

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
        rows=selected_rows,
        registry=display_registry,
        catalog_index=catalog_index,
        level=level,
        mode="pivot" if pivot else "table",
        view_name=view,
        explain_facets=explain_facets,
    )

    if not pivot:
        table = inject_id_column(
            table,
            selected_rows,
        )

    output = render_table(
        table,
        renderer,
    )

    if output:
        click.echo(
            output,
        )
