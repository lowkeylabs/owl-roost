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

from pprint import pprint

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
from owlroost.operations.resolve import build_resolver
from owlroost.workspace.loaders import (
    load_workspace_row,
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
    "--root",
    default=".",
    show_default=True,
    help="Workspace root folder.",
)
@click.option(
    "--explain",
    type=str,
    default="variables",
    help=("Explanation facets. Use '.' for list."),
)
@click.option(
    "--assist",
    default="status",
    callback=parse_assist,
    help=(
        "Append activity view(s).\n"
        "Examples:\n"
        "  --assist\n"
        "  --assist status\n"
        "  --assist suggestions,status"
    ),
)
def cmd_context(
    ctx,
    view,
    root,
    explain,
    assist,
):
    """
    Display the current planning context.
    """

    # =====================================================
    # Invocation
    # =====================================================

    _invoked_as = ctx.info_name
    is_publish_command = _invoked_as == "publish"

    DEFAULT_VIEW = "cases"
    if view is None:
        view = ctx.info_name or DEFAULT_VIEW

    view = view or "context"
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

    planning_context = materialize_planning_context(
        load_workspace_row(root),
        catalog,
    )
    resolve = build_resolver(
        catalog,
        planning_context,
    )

    if is_publish_command:
        click.echo("publish command selected")

        if not resolve("context.workspace.initialized"):
            click.echo("publish requires an initialized workspace.  Use: roost workspace --init")
            return

        if 1:
            pprint(planning_context.keys())
        if 0:
            pprint(planning_context["_context"])
        if 0:
            pprint(planning_context["_activity"].keys())
        if 1:
            pprint(planning_context["_activity"])

        return

    # =====================================================
    # Display views
    # =====================================================

    if view is not None:
        table = materialize_view(
            rows=[planning_context],
            registry=catalog.display_registry,
            catalog_index=catalog.catalog_index,
            level=level,
            mode="pivot",
            view_name=view,
            explain_facets=explain_facets,
            show_header=True,
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

        return

    # =====================================================
    # Planning activities
    # =====================================================

    # assist is a list of command line keyword views found activity.py

    for activity_view in assist:
        if not catalog.display_registry.has_view_for_level(
            "activity",
            activity_view,
        ):
            click.echo("")
            click.echo(f"View not found: activity/{activity_view}")

            render_available_views(
                catalog.display_registry,
                level="activity",
            )

            continue

        activity_table = materialize_view(
            rows=[planning_context],
            registry=catalog.display_registry,
            catalog_index=catalog.catalog_index,
            level="activity",
            mode="pivot",
            view_name=activity_view,
            explain_facets=explain_facets,
            show_header=False,
        )

        activity_output = render_table(
            activity_table,
            resolve_renderer(
                False,
                False,
            ),
        )

        if activity_output:
            click.echo()
            click.echo(
                activity_output,
            )
