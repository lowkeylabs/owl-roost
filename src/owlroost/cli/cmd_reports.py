# src/owlroost/cli/cmd_reports.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Reporting CLI.

Notes
-----
Synchronizes report entrypoints into
ROOST-generated results trees.

Templates are user-owned.

Results are ROOST-owned.

The reporting layer binds user-owned
templates onto the results provenance
tree through generated:

    index.qmd
    _metadata.yml

artifacts.
"""

from __future__ import annotations

from pathlib import Path

import click

from owlroost.reports.reports import (
    sync_reports,
)


@click.command("reports")
@click.option(
    "--sync",
    is_flag=True,
    help=("Synchronize report entrypoints into the results tree."),
)
@click.option(
    "--results-dir",
    type=click.Path(
        path_type=Path,
    ),
    default=Path("./results"),
    show_default=True,
)
@click.option(
    "--results-template-dir",
    type=click.Path(
        path_type=Path,
    ),
    help=("Override results_template_dir defined in study.toml."),
)
def cmd_reports(
    sync: bool,
    results_dir: Path,
    results_template_dir: Path | None,
):
    """
    Manage provenance reporting.

    Examples
    --------

        roost reports --sync

        roost reports \
            --sync \
            --results-template-dir \
            ./templates/results
    """

    results_dir = results_dir.resolve()

    if results_template_dir is not None:
        results_template_dir = results_template_dir.resolve()

    if not sync:
        raise click.ClickException("Specify --sync.")

    print(f"results_dir: {results_dir}")
    print(f"results_template_dir: {results_template_dir}")
    try:
        sync_reports(
            results_dir=results_dir,
            results_template_dir=results_template_dir,
        )

    except Exception as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo("Report sync complete.")
