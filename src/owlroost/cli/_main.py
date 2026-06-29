# src/owlroost/cli/_main.py
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

import click

from ..core.info import (
    get_installation_info,
)
from ..version import __version__
from .cmd_build import cmd_build
from .cmd_household import cmd_household
from .cmd_reports import cmd_reports
from .cmd_results import cmd_results
from .cmd_run import cmd_run
from .cmd_vars import cmd_vars
from .cmd_workspace import cmd_workspace


@click.group(invoke_without_command=True)
@click.version_option(
    version=__version__,
    prog_name="roost",
)
@click.option(
    "--log-level",
    default="INFO",
    show_default=True,
    help="Log level",
)
@click.pass_context
def cli(
    ctx,
    log_level,
):
    """
    ROOST CLI (in development).

    See main project README.md
    """

    # ----------------------------------------
    # Normalize level
    # ----------------------------------------
    log_level = log_level.upper()

    ctx.ensure_object(dict)


@cli.command()
@click.pass_context
@click.argument(
    "key",
    required=False,
)
def info(ctx, key):
    """Show ROOST installation information."""

    info = get_installation_info()

    if key is None:
        for k, v in info.items():
            click.echo(f"{k}: {v}")
    else:
        click.echo(info[key])


#    solver = get_owl_solver_info()
#    click.echo(f"OWL-Planner version: {solver.version}")
#    if solver.commit:
#        click.echo(f"OWL-Planner commit:  {solver.commit}")
#    click.echo(f"{solver}")


cli.add_command(cmd_build, name="cases")
cli.add_command(cmd_build, name="build")

cli.add_command(cmd_run)
cli.add_command(cmd_reports)
cli.add_command(cmd_results)

cli.add_command(cmd_vars, name="vars")
cli.add_command(cmd_workspace)
cli.add_command(cmd_household)
