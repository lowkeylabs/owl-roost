# src/owlroost/workspace/operations.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace operations.

Notes
-----
Owns filesystem operations
performed on workspaces.

A workspace is currently defined
as a directory containing:

    workspace.toml

Workspace capability queries
belong in workspace.checks.

This module should perform
mutations only.

"""

from __future__ import annotations

import os
import re
import shutil
import tomllib
from pathlib import Path

import yaml

from owlroost.core.settings import (
    get_workspace_template_dir,
)
from owlroost.display.discovery import (
    find_cases,
    find_first_trial,
    find_runs,
    find_sessions,
)
from owlroost.exceptions import (
    RoostError,
)
from owlroost.workspace.default_toml import (
    render_workspace_toml,
)
from owlroost.workspace.levers.context import workspace_initialized

# These files should exist and be stored in ./src/owlroost/templates/workspace
# The user can create "makefile.mk" to hold local commands
# The Makefile will autoload ./templates/workspace/default-makefile.mk

WORKSPACE_TEMPLATE_FILES = [
    "index.qmd",
    "Makefile",
    "_quarto.yml",
    "_variables.yml",
]


def rename_workspace(
    workspace_dir,
    new_name,
):
    """
    Rename a workspace directory.
    """

    workspace_dir = Path(
        workspace_dir,
    )

    if not workspace_dir.exists():
        raise RoostError(f"Workspace not found: {workspace_dir}")

    target = workspace_dir.parent / new_name

    if target.exists():
        raise RoostError(f"Target already exists: {target}")

    workspace_dir.rename(
        target,
    )

    return target


def install_workspace_templates(
    workspace_dir: Path,
    *,
    force: bool = False,
) -> None:
    """Install standard workspace template files."""

    template_dir = get_workspace_template_dir() / "workspace"

    for filename in WORKSPACE_TEMPLATE_FILES:
        src = template_dir / filename
        dst = workspace_dir / filename

        if not src.exists():
            raise RoostError(f"Missing workspace template: {src}")

        if force or not dst.exists():
            shutil.copy2(src, dst)


def init_workspace(
    workspace_dir=".",
    *,
    parent="",
    force=False,
):
    """
    Initialize an existing directory
    as a workspace.

    Missing files are created.

    Existing files are preserved
    unless force=True.
    """

    parent = Path(parent)

    workspace_dir = Path(
        parent / workspace_dir,
    ).resolve()

    if not workspace_dir.exists():
        raise RoostError(f"Directory does not exist: {workspace_dir}")

    if not workspace_dir.is_dir():
        raise RoostError(f"Not a directory: {workspace_dir}")

    workspace_exists = workspace_initialized(
        workspace_dir,
    )

    workspace_toml = workspace_dir / "workspace.toml"

    # -----------------------------------------
    # workspace.toml
    # -----------------------------------------

    if force or not workspace_exists:
        workspace_toml.write_text(
            render_workspace_toml(
                workspace_dir,
            )
        )

    install_workspace_templates(
        workspace_dir,
        force=force,
    )

    return workspace_dir


def sync_results_catalog(
    workspace_dir=".",
    *,
    force=False,
):
    """
    Synchronize generated catalog files
    throughout the results tree.

    ROOST owns:

        index.qmd
        _metadata.yml

    beneath the results tree.

    If force=False:

        * create missing files
        * refresh include paths
        * refresh metadata

    If force=True:

        * overwrite index.qmd from template
        * refresh include paths
        * refresh metadata
    """

    workspace_dir = Path(
        workspace_dir,
    ).resolve()

    if not workspace_initialized(
        workspace_dir,
    ):
        raise RoostError(f"Missing workspace.toml: {workspace_dir / 'workspace.toml'}")

    workspace_file = workspace_dir / "workspace.toml"

    if not workspace_file.exists():
        raise RoostError(f"Missing workspace.toml: {workspace_file}")

    with open(
        workspace_file,
        "rb",
    ) as fh:
        workspace = tomllib.load(
            fh,
        )

    # =====================================================
    # Results directory
    # =====================================================

    results_dir = Path(
        workspace.get(
            "results_dir",
            "results",
        )
    )

    if not results_dir.is_absolute():
        results_dir = workspace_dir / results_dir

    results_dir = results_dir.resolve()

    if not results_dir.exists():
        return

    # =====================================================
    # Template directory
    # =====================================================

    template_root = workspace.get(
        "results_template_dir",
    )

    if template_root:
        template_root = Path(
            template_root,
        ).resolve()

    else:
        template_root = (get_workspace_template_dir() / "results").resolve()

    # =====================================================
    # Helpers
    # =====================================================

    include_re = re.compile(r"(\{\{<\s*include\s+)(.+?)(\s*>\}\})")

    def write_metadata(
        *,
        target_dir,
        level,
        level_template_dir,
    ):
        metadata = {
            "level": level,
            "paths": {
                "workspace_dir": str(
                    workspace_dir,
                ),
                "results_dir": str(
                    results_dir,
                ),
                "template_root": str(
                    template_root,
                ),
                "level_template_dir": str(
                    level_template_dir,
                ),
                "current_dir": str(
                    target_dir.resolve(),
                ),
                "relative_template_dir": os.path.relpath(
                    level_template_dir,
                    start=target_dir,
                ),
            },
        }

        with open(
            target_dir / "_metadata.yml",
            "w",
            encoding="utf-8",
        ) as fh:
            yaml.safe_dump(
                metadata,
                fh,
                sort_keys=False,
            )

    def sync_qmd(
        *,
        qmd_file,
        template_file,
        level,
    ):
        qmd_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -----------------------------------------
        # Materialize template
        # -----------------------------------------

        if force or not qmd_file.exists():
            if not template_file.exists():
                raise RoostError(f"Missing template: {template_file}")

            shutil.copy2(
                template_file,
                qmd_file,
            )

        text = qmd_file.read_text(
            encoding="utf-8",
        )

        match = include_re.search(
            text,
        )

        if match:
            include_target = match.group(2).strip()

            # -------------------------------------
            # Preserve payload filename
            # -------------------------------------

            if not force and "__PAYLOAD_DIR__" not in include_target:
                filename = Path(include_target).name

            else:
                filename = Path(
                    include_target.replace(
                        "__PAYLOAD_DIR__/",
                        "",
                    )
                ).name

            payload_file = (template_file.parent / filename).resolve()

            refreshed = os.path.relpath(
                payload_file,
                start=qmd_file.parent,
            )

            replacement = match.group(1) + refreshed + match.group(3)

            text = include_re.sub(
                replacement,
                text,
                count=1,
            )

            qmd_file.write_text(
                text,
                encoding="utf-8",
            )

        # -----------------------------------------
        # Metadata
        # -----------------------------------------

        write_metadata(
            target_dir=qmd_file.parent,
            level=level,
            level_template_dir=(template_file.parent),
        )

    # =====================================================
    # Results root
    # =====================================================

    sync_qmd(
        qmd_file=(results_dir / "index.qmd"),
        template_file=(template_root / "results" / "_index.qmd"),
        level="results",
    )

    # =====================================================
    # Cases
    # =====================================================

    for case_dir in find_cases(
        results_dir,
    ):
        sync_qmd(
            qmd_file=(case_dir / "index.qmd"),
            template_file=(template_root / "case" / "_index.qmd"),
            level="case",
        )

    # =====================================================
    # Sessions
    # =====================================================

    for session_dir in find_sessions(
        results_dir,
    ):
        sync_qmd(
            qmd_file=(session_dir / "index.qmd"),
            template_file=(template_root / "session" / "_index.qmd"),
            level="session",
        )

    # =====================================================
    # Runs / Trials
    # =====================================================

    for session_dir in find_sessions(
        results_dir,
    ):
        for run_dir in find_runs(
            session_dir,
        ):
            sync_qmd(
                qmd_file=(run_dir / "index.qmd"),
                template_file=(template_root / "run" / "_index.qmd"),
                level="run",
            )

            trial_dir = find_first_trial(
                run_dir,
            )

            if trial_dir:
                sync_qmd(
                    qmd_file=(trial_dir / "index.qmd"),
                    template_file=(template_root / "trial" / "_index.qmd"),
                    level="trial",
                )
