# src/owlroost/cli/cmd_vals.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Display canonical catalog semantics.

Architecture
------------
Schema Registry
    -> Metrics Registry
    -> Display Registry
    -> Catalog Rows
    -> Materialized View
    -> RoostTable
    -> Renderer
"""

from __future__ import annotations

import click

from owlroost.catalog.context import build_catalog_context
from owlroost.operations.resolve import build_resolver
from owlroost.workspace.loaders import load_context_row
from owlroost.workspace.materializers import materialize_planning_context

from ..core.settings import get_settings

# =========================================================
# CLI
# =========================================================


@click.command("vars")
@click.pass_context
@click.argument(
    "args",
    nargs=-1,
)
def cmd_vals(
    ctx,
    args,
):
    """
    Display ROOST ontology and variable catalog.
    """

    _invoked_as = ctx.info_name
    # set default view to "build" or "cases"
    # will automatically load as "case" view

    info = get_settings()

    if args is None or len(args) == 0:
        for k, v in info.items():
            click.echo(f"{k}: {v}")
        return

    for key in args:
        if key in info.keys():
            click.echo(info[key])
            return

    catalog = build_catalog_context()
    planning_context = materialize_planning_context(
        load_context_row("."),
        catalog,
    )
    resolve = build_resolver(
        catalog,
        planning_context,
    )
    for key in args:
        try:
            value = resolve(key)
            print(value)
        except Exception as e:
            print(str(e))
