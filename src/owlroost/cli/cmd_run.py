# src/owlroost/cli/cmd_run.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

import os
from pathlib import Path

import click

from owlroost.catalog.context import build_catalog_context
from owlroost.cli.help import (
    process_help_requests,
)
from owlroost.cli.utils import (
    render_available_views,
    render_table,
    resolve_renderer,
)
from owlroost.core.run_owl_executor import execute_runs
from owlroost.display.loaders import load_run_rows
from owlroost.display.materializers.materialize import materialize_view
from owlroost.display.operations.filtering import apply_filters
from owlroost.display.operations.row_ops import apply_top, attach_row_ids
from owlroost.display.operations.sorting import apply_canonical_sort, apply_sort

# =========================================================
# CLI
# =========================================================


@click.command("run")
@click.argument(
    "selectors",
    nargs=-1,
)
@click.option(
    "--root",
    default="results",
    type=click.Path(exists=True),
)
@click.option(
    "--view",
    default="run",
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
    "--pivot",
    is_flag=True,
)
@click.option(
    "--filter",
    "filters",
    multiple=True,
    help=("Filter rows. Examples: case_id=0 trial.pending>0"),
)
@click.option(
    "--sort",
    type=str,
    help="Sort by field. Prefix '-' for descending.",
)
@click.option(
    "--top",
    type=int,
    help="Limit number of rows.",
)
@click.option(
    "--progress",
    default="rich",
    show_default=True,
    help="Progress renderer: rich, dot, dot2, none",
)
@click.option(
    "--rerun",
    is_flag=True,
    default=False,
    help="Rerun completed trials.",
)
@click.option(
    "--list-only",
    is_flag=True,
    default=False,
    help="Display matching runs but do not execute.",
)
def cmd_run(
    selectors,
    root,
    view,
    markdown,
    latex,
    pivot,
    filters,
    sort,
    top,
    progress,
    rerun,
    list_only,
):
    """
    Display and execute runs.

    Default behavior:

    - discover runs
    - filter to runs with pending trials
    - display matching runs
    - execute pending trials

    Execution uses hybrid scheduling:

    - single-trial runs are bundled
    - multi-trial runs execute independently
    """

    root = Path(root).resolve()

    # =====================================================
    # Build Registries
    # =====================================================

    (
        schema_registry,
        metrics_registry,
        workspace_registry,
        display_registry,
        catalog_rows,
        catalog_index,
    ) = build_catalog_context()

    # =====================================================
    # Check requested view
    # =====================================================

    level = "run"

    if 0:
        if not view or not display_registry.has_view_for_level(
            level,
            view,
        ):
            if view:
                click.echo(f"Display view not found: {level}/{view}")

            render_available_views(
                display_registry,
                level=level,
            )

            return

    # =====================================================
    # Discover + Load Runs
    # =====================================================

    rows = load_run_rows(
        metrics_registry=metrics_registry,
        results_root=str(root),
    )

    if process_help_requests(
        selectors=selectors,
        overrides=None,
        help_requests=None,
        view=view,
        explain=None,
        filters=filters,
        sort=sort,
        top=top,
        rows=rows,
        display_registry=display_registry,
        schema_registry=schema_registry,
        level=level,
    ):
        return

    if not rows:
        click.echo("No runs found.")
        return

    # =====================================================
    # Default Pending Filter
    # =====================================================

    filter_list = list(filters)

    if not rerun:
        filter_list.append("trial.pending>0")

    rows = apply_canonical_sort(
        rows,
    )

    rows = apply_filters(
        rows,
        filter_list,
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

    # =====================================================
    # No Matching Runs
    # =====================================================

    if not rows:
        if rerun:
            click.echo("No matching runs found.")

        else:
            click.echo("No pending runs found.")

        return

    # =====================================================
    # Resolve Renderer
    # =====================================================

    renderer = resolve_renderer(
        markdown,
        latex,
    )

    # =====================================================
    # Materialize View
    # =====================================================

    table = materialize_view(
        rows=rows,
        registry=display_registry,
        level="run",
        view_name=view,
        mode="pivot" if pivot else "table",
    )

    # =====================================================
    # Render Table
    # =====================================================

    if 0:
        _output = render_table(
            table,
            renderer,
        )

    # =====================================================
    # List-only Exit
    # =====================================================

    if list_only:
        return

    # =====================================================
    # Resolve Selected Runs
    # =====================================================

    selected_runs = []

    for row in rows:
        run_dir = row.get("_path")

        if run_dir:
            selected_runs.append(Path(run_dir))

    # =====================================================
    # No Executable Runs
    # =====================================================

    if not selected_runs:
        click.echo("No runs available for execution.")

        return

    # =====================================================
    # Progress Label Width
    # =====================================================

    labels = []

    for run_dir in selected_runs:
        try:
            run_name = f"{run_dir.parent.parent.parent.name}/{run_dir.name}"

            labels.append(run_name)

        except Exception:
            labels.append(run_dir.name)

    if labels:
        max_label_width = max(len(x) for x in labels)

        os.environ["OWLROOST_PROGRESS_LABEL_WIDTH"] = str(max_label_width)

    # =====================================================
    # Execute
    # =====================================================

    click.echo(f"Scheduling {len(selected_runs)} runs.")

    execute_runs(
        selected_runs,
        progress=progress,
        rerun=rerun,
    )


if __name__ == "__main__":
    cmd_run()
