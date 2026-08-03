# src/owlroost/cli/cmd_build.py
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
import subprocess
import sys
from pathlib import Path

import click

from owlroost.catalog.context import build_catalog_context
from owlroost.cli.help import (
    process_help_requests,
)
from owlroost.cli.utils import (
    parse_override_request,
    render_available_views,
    render_table,
    resolve_renderer,
    select_case_rows,
    split_build_args,
)
from owlroost.core.run_owl_executor import execute_runs
from owlroost.display.discovery import find_runs
from owlroost.display.explain import (
    parse_explain_request,
)
from owlroost.display.loaders import load_case_rows
from owlroost.display.materializers.compare import materialize_compare_table
from owlroost.display.materializers.materialize import materialize_view
from owlroost.display.operations.filtering import apply_filters
from owlroost.display.operations.row_ops import apply_top, attach_row_ids
from owlroost.display.operations.sorting import apply_canonical_sort, apply_sort
from owlroost.display.operations.table_ops import inject_id_column
from owlroost.operations.resolve import build_resolver
from owlroost.schema.sweeps import expand_cli_overrides
from owlroost.workspace.loaders import (
    load_workspace_row,
)
from owlroost.workspace.materializers import (
    materialize_planning_context,
)

DEFAULT_LEVEL = "case"
DEFAULT_VIEW = "build"


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def build_hydra_command(
    case_path: Path,
    overrides: list[str],
    *,
    study_name: str | None = None,
    experiment_name: str | None = None,
    orphan_overrides: list[str] | None = None,
    workspace_overrides: list[str] | None = None,
):
    """
    Construct Hydra multirun command.
    """

    package_root = Path(__file__).parents[1]

    conf_dir = package_root / "conf"

    overrides = expand_cli_overrides(overrides)

    if workspace_overrides is None:
        workspace_overrides = []

    cmd = [
        sys.executable,
        "-m",
        "owlroost.executive.generate_trials",
        "--multirun",
        (f"--config-path={str(conf_dir.resolve())}"),
        "--config-name=config",
        (f"case.file={str(case_path.resolve())}"),
        (f"case.name={case_path.stem}"),
        *overrides,
        *workspace_overrides,
    ]

    if study_name is not None:
        cmd.append(f"roost_settings.study_name={study_name}")
    if experiment_name is not None:
        cmd.append(f"roost_settings.experiment_name={experiment_name}")
    if orphan_overrides is not None:
        cmd.append(f"roost_settings.orphan_overrides='{','.join(orphan_overrides)}'")
    if workspace_overrides is not None:
        cmd.append(f"roost_settings.workspace_overrides='{','.join(workspace_overrides)}'")

    # print(cmd)
    return cmd


def discover_latest_session(
    results_root: Path,
    case_name: str,
):
    """
    Return newest session directory
    for case.
    """

    case_root = results_root / case_name

    if not case_root.exists():
        return None

    candidates = []

    for date_dir in case_root.iterdir():
        if not date_dir.is_dir():
            continue

        for exp_dir in date_dir.iterdir():
            if not exp_dir.is_dir():
                continue

            if (exp_dir / "multirun.yaml").exists():
                candidates.append(exp_dir)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def run_direct_case_build(
    case_paths,
    overrides,
    *,
    progress,
    run,
):
    generated_runs = []

    for case_path in case_paths:
        runs = run_hydra_build(
            case_path,
            list(overrides),
        )

        generated_runs.extend(
            runs,
        )

    if not run:
        click.echo(f"Generated {len(generated_runs)} sessions.")

        click.echo("session generation complete.")

        return

    if not generated_runs:
        click.echo("No runs available for execution.")

        return

    execute_runs(
        generated_runs,
        progress=progress,
    )


def resolve_direct_case_paths(
    selectors,
) -> list[Path]:
    """
    Resolve selectors that reference
    explicit TOML files.

    Examples
    --------
    roost build case.toml

    roost build examples/foo/case.toml
    """

    paths = []

    for selector in selectors:
        path = Path(selector)

        if path.suffix == ".toml" and path.exists():
            paths.append(
                path.resolve(),
            )

    return paths


# ---------------------------------------------------------
# Hydra execution
# ---------------------------------------------------------
def run_hydra_build(
    case_path: Path,
    overrides: list[str],
    *,
    study_name: str | None = None,
    experiment_name: str | None = None,
    orphan_overrides: list[str] | None = None,
    workspace_overrides: list[str] | None = None,
):
    """
    Execute Hydra generator in multirun mode.

    Returns:
        list[Path] of generated run directories
    """
    cmd = build_hydra_command(
        case_path,
        overrides,
        study_name=study_name,
        experiment_name=experiment_name,
        orphan_overrides=orphan_overrides,
        workspace_overrides=workspace_overrides,
    )

    #    click.echo("Running Hydra:")
    #    logger.debug(f"Hydra CLI: {(" ".join(cmd))}")
    #    click.echo()

    try:
        subprocess.run(
            cmd,
            check=True,
        )

        exp_dir = discover_latest_session(
            Path("results"),
            case_path.stem,
        )

        if exp_dir is None:
            raise click.ClickException("Unable to locate generated session.")

        runs = find_runs(exp_dir)
        if not runs:
            raise click.ClickException(f"No runs discovered in {exp_dir}")
        return runs

    except subprocess.CalledProcessError as exc:
        raise click.ClickException(f"Hydra run failed ({exc.returncode})") from exc


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------
@click.command("build")
@click.pass_context
@click.argument(
    "args",
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
    "--pivot",
    is_flag=True,
    help="Render transposed pivot layout.",
)
@click.option(
    "--compare",
    is_flag=True,
    help="Structural side-by-side comparison.",
)
@click.option(
    "--diff",
    is_flag=True,
    help="Show only differing structural fields.",
)
@click.option(
    "--explain",
    type=str,
    help=("Explanation facets. Use '.' for list."),
)
@click.option(
    "--filter",
    "filters",
    multiple=True,
    help=(
        "Filter rows. "
        "Examples: "
        "display.total_savings>1000000 "
        "optimization_parameters.objective=maxBequest"
    ),
)
@click.option(
    "--sort",
    type=str,
    help="Sort by field. Prefix '-' for descending.",
)
@click.option(
    "--top",
    type=str,
    help="Limit number of rows.",
)
@click.option(
    "--progress",
    default="rich",
    show_default=True,
    help=("Progress renderer: rich, dot, dot2, none"),
)
@click.option(
    "--run",
    is_flag=True,
    help="Generate sessions only; do not execute runs.",
)
@click.option(
    "--case-folder",
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        path_type=Path,
    ),
    help=("Folder containing case*.toml and HFP_*.xlsx files."),
)
@click.option(
    "--import-to",
    default=None,
    metavar="LIBRARY",
    help=(
        "Import selected cases into the named household library (workspace, user, builtin, ...)."
    ),
)
@click.option(
    "--experiment",
    type=str,
    help=("Comma-separated list of experiment names."),
)
@click.option(
    "--study",
    type=str,
    help=("Comma-separated list of study names."),
)
def cmd_build(
    ctx,
    args,
    view,
    markdown,
    latex,
    pivot,
    compare,
    diff,
    explain,
    filters,
    sort,
    top,
    progress,
    run,
    case_folder,
    import_to,
    experiment,
    study,
):
    """
    Display available cases and build sessions.

    Examples:
      roost build
      roost build 0
      roost build case.toml
      roost build 0 solver_options.maxSpending=145
    """

    # was this function invoked as "cases" or "build"

    _invoked_as = ctx.info_name
    # set default view to "build" or "cases"
    # will automatically load as "case" view
    if view is None:
        view = ctx.info_name or DEFAULT_VIEW

    selectors, overrides, help_requests = split_build_args(args)

    is_cases_command = _invoked_as == "cases"

    #    if overrides_request_trials(overrides):
    #        if run:
    #            click.echo("INFO: trials_per_run > 0 detected; " "enabling --build-only automatically.")
    #
    #        build_only = True

    catalog = build_catalog_context()

    # =====================================================
    # Parse experiment, direct case paths and overrices
    # (these are all used later, AFTER rows are loaded.)
    # =====================================================

    experiment_names = []
    if experiment:
        experiment_names = [x.strip() for x in experiment.split(",") if x.strip()]

    experiments = []
    for name in experiment_names:
        spec = catalog.study_registry.get_experiment(name)

        if spec is None:
            raise click.ClickException(f"Unknown experiment: {name}")

        experiments.append(spec)

    study_names = []
    if study:
        study_names = [x.strip() for x in study.split(",") if x.strip()]

    studies = []
    for name in study_names:
        spec = catalog.study_registry.get_study(name)

        if spec is None:
            raise click.ClickException(f"Unknown study: {name}")

        studies.append(spec)

    direct_case_paths = resolve_direct_case_paths(
        selectors,
    )

    overrides, override_errors = parse_override_request(
        overrides,
        catalog.schema_registry,
    )

    if 0 and override_errors:
        raise click.BadParameter(
            "\n".join(
                override_errors,
            )
        )

    # This code is used by the tests only.
    # See bottom of file for CLI processing.

    if direct_case_paths:
        if experiments:
            for experiment in experiments:
                experiment_overrides = [
                    *overrides,
                    *experiment.hydra_overrides(),
                ]

                run_direct_case_build(
                    direct_case_paths,
                    experiment_overrides,
                    progress=progress,
                    run=run,
                )

        else:
            run_direct_case_build(
                direct_case_paths,
                overrides,
                progress=progress,
                run=run,
            )

        return

    # =====================================================
    # Parse explain request
    # =====================================================

    explain_facets, explain_errors = parse_explain_request(
        explain,
    )

    if 0 and explain_errors:
        raise click.BadParameter(
            "\n".join(
                explain_errors,
            )
        )

    # =====================================================
    # Check requested view
    # =====================================================

    level = DEFAULT_LEVEL

    if not view or not catalog.display_registry.has_view_for_level(
        level,
        view,
    ):
        if view:
            click.echo(f"Display view not found: {level}/{view}")

        render_available_views(
            catalog.display_registry,
            level=level,
        )

        return

    # =====================================================
    # Context-sensitive CLI help
    # =====================================================

    rows = load_case_rows(
        case_folder,
        schema_registry=catalog.schema_registry,
        metrics_registry=catalog.metrics_registry,
    )
    # if no cases and we're in ".", look in ./cases
    if not rows:
        case_folder = "./cases"
        rows = load_case_rows(
            case_folder,
            schema_registry=catalog.schema_registry,
            metrics_registry=catalog.metrics_registry,
        )
    rows = attach_row_ids(rows)

    if process_help_requests(
        selectors=selectors,
        overrides=overrides,
        help_requests=help_requests,
        view=view,
        explain=explain,
        filters=filters,
        sort=sort,
        top=top,
        rows=rows,
        display_registry=catalog.display_registry,
        schema_registry=catalog.schema_registry,
        level=level,
    ):
        return

    # ----------------------------------------
    # Discover + load case dataset
    # ----------------------------------------
    rows = apply_canonical_sort(
        rows,
    )

    #    if filters:
    #        print(filters)

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
        click.echo("No case TOML files found.")
        return

    if selectors:
        rows = select_case_rows(
            rows,
            selectors,
        )

    selected_rows = rows

    if not selected_rows:
        raise click.ClickException("No matching case selections.")

    # ----------------------------------------
    # Process any imports
    # ----------------------------------------

    if is_cases_command and import_to is not None:
        from owlroost.household.bootstrap import (
            household_library,
        )
        from owlroost.household.operations import (
            import_case,
        )

        library = household_library(
            import_to,
            root=case_folder,
        )

        for row in selected_rows:
            import_case(
                case_file=Path(
                    row["_path"],
                ),
                library=library,
            )

        return

    # ----------------------------------------
    # Resolve renderer
    # ----------------------------------------
    renderer = resolve_renderer(
        markdown,
        latex,
    )

    # =====================================================
    # Structural compare/diff mode
    #
    # Also automatically enabled when:
    #   roost cases <single-id>
    #
    # because user intent is usually:
    #   "show me full case contents"
    # =====================================================

    auto_compare = (
        is_cases_command
        and len(rows) == 1
        and not compare
        and not diff
        and not pivot
        and view == "basic"
    )

    if compare or diff or auto_compare:
        table = materialize_compare_table(
            rows,
            registry=catalog.display_registry,
            catalog_index=catalog.catalog_index,
            diff_only=diff,
            explain_facets=explain_facets,
        )

        output = render_table(
            table,
            renderer,
        )

        if output:
            click.echo(output)

        return

    # ----------------------------------------
    # List available cases
    # ----------------------------------------
    if is_cases_command or (not selectors and not overrides):
        table = materialize_view(
            rows=rows,
            registry=catalog.display_registry,
            catalog_index=catalog.catalog_index,
            level=DEFAULT_LEVEL,
            view_name=view,
            mode="pivot" if pivot else "table",
            explain_facets=explain_facets,
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
            click.echo(output)

        return

    # ----------------------------------------
    # Process load workspace
    # ----------------------------------------
    workspace_row = load_workspace_row(case_folder)
    planning_context = materialize_planning_context(
        workspace_row,
        catalog,
    )
    resolve = build_resolver(
        catalog,
        planning_context,
    )
    # print(resolve("workspace.overrides"))

    # ----------------------------------------
    # Process selected rows
    # ----------------------------------------

    labels = []

    for row in selected_rows:
        case_path = Path(row["_path"]).resolve()

        labels.append(f"{case_path.stem}/run_0")

    max_label_width = max(len(x) for x in labels)

    os.environ["OWLROOST_PROGRESS_LABEL_WIDTH"] = str(max_label_width)

    generated_runs = []

    for row in selected_rows:
        case_path = Path(row["_path"]).resolve()

        if 0:
            print(f"Path: {case_path}")
            print(f"Overrides: {overrides}")
            print(f"Experiments: {experiments}")

        experiment_overrides = overrides

        if studies:
            for study in studies:
                for experiment_name in study.experiment_names:
                    print(f"{study.name} -> {experiment_name}")

                    experiment = catalog.study_registry.get_experiment(experiment_name)

                    experiment_overrides = [
                        *overrides,
                        *experiment.hydra_overrides(),
                    ]

                    runs = run_hydra_build(
                        case_path,
                        list(experiment_overrides),
                        study_name=study.name,
                        experiment_name=experiment.name,
                        orphan_overrides=overrides,
                        workspace_overrides=resolve("workspace.overrides"),
                    )

                    generated_runs.extend(runs)

        elif experiments:
            for experiment in experiments:
                experiment_overrides = [
                    *overrides,
                    *experiment.hydra_overrides(),
                ]

                runs = run_hydra_build(
                    case_path,
                    list(experiment_overrides),
                    study_name=None,
                    experiment_name=experiment.name,
                    orphan_overrides=overrides,
                    workspace_overrides=resolve("workspace.overrides"),
                )

                generated_runs.extend(runs)

        else:
            runs = run_hydra_build(
                case_path,
                list(experiment_overrides),
                study_name=None,
                experiment_name=None,
                orphan_overrides=overrides,
                workspace_overrides=resolve("workspace.overrides"),
            )

            generated_runs.extend(runs)

    # ----------------------------------------
    # Build-only exit
    # ----------------------------------------

    if not run:
        click.echo(f"Generated {len(generated_runs)} sessions.")

        click.echo("session generation complete.")

        return

    # ----------------------------------------
    # Execute all runs
    # ----------------------------------------

    if not generated_runs:
        click.echo("No runs available for execution.")

        return

    execute_runs(
        generated_runs,
        progress=progress,
    )
