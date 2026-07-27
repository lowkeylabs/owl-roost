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

from ..version import __version__
from .cmd_build import cmd_build
from .cmd_context import cmd_context
from .cmd_household import cmd_household
from .cmd_reports import cmd_reports
from .cmd_results import cmd_results
from .cmd_run import cmd_run
from .cmd_vals import cmd_vals
from .cmd_vars import cmd_vars
from .cmd_workspace import cmd_workspace


def render_welcome(guide):
    print("welcome")


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
    #
    # No subcommand?
    #
    if ctx.invoked_subcommand is None:
        print("welcome.  Adjust in _main")


# ================================================
# Add commands
# ================================================

cli.add_command(cmd_build, name="cases")
cli.add_command(cmd_build, name="build")

cli.add_command(cmd_run)
cli.add_command(cmd_reports)
cli.add_command(cmd_results)

cli.add_command(cmd_vars, name="vars")
cli.add_command(cmd_vals, name="vals")
cli.add_command(cmd_vals, name="settings")

cli.add_command(cmd_workspace, name="workspace")
cli.add_command(cmd_workspace, name=".")

cli.add_command(cmd_context, name="context")
cli.add_command(cmd_context, name="publish")

cli.add_command(cmd_household, name="library")
