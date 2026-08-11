# src/owlroost/workspace/loaders.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace loaders.

Notes
-----
Owns discovery and loading of
planning contexts and workspace
definitions.

A planning context always exists.

A workspace is an optional planning
artifact represented by:

    workspace.toml

The packaged workspace.toml template
defines:

    * recognized workspace configuration
    * default workspace configuration

A local workspace.toml selectively
overrides those defaults.

Configuration Composition
-------------------------
Workspace configuration is composed
recursively.

TOML tables are merged recursively.
Values within a local table replace the
corresponding values from the canonical
template while unspecified sibling values
remain unchanged.

Scalar values and arrays replace their
canonical values as complete values.

This includes arrays of tables such as:

    [[context.households]]

The canonical template also defines the
configuration schema. A local key that does
not exist at the corresponding location in
the template generates a warning and is
ignored.

Responsibilities
----------------
* Discover workspaces
* Load planning contexts
* Load workspace configuration defaults
* Load local workspace configuration
* Validate local configuration keys
* Compose effective workspace definitions

Does NOT
--------
* Render output
* Materialize tables
* Populate inventory
* Perform workspace operations
"""

from __future__ import annotations

import copy
import tomllib
import warnings
from pathlib import Path
from typing import Any

from owlroost.core.settings import (
    get_workspace_template_dir,
)

# =========================================================
# Constants
# =========================================================


WORKSPACE_TOML = "workspace.toml"


# =========================================================
# TOML Loading
# =========================================================


def _load_workspace_toml(
    path: Path,
):
    """
    Load a workspace TOML file.

    Parameters
    ----------
    path
        TOML file to load.

    Returns
    -------
    dict
        Parsed TOML document.
    """

    with path.open(
        "rb",
    ) as fh:
        return tomllib.load(
            fh,
        )


def _workspace_template_file():
    """
    Return the canonical workspace
    configuration template.
    """

    return get_workspace_template_dir() / "workspace" / WORKSPACE_TOML


def _load_workspace_defaults():
    """
    Load canonical workspace
    configuration defaults.

    The packaged workspace.toml template
    is the authoritative definition of
    both:

        * recognized configuration
        * default configuration
    """

    return _load_workspace_toml(
        _workspace_template_file(),
    )


# =========================================================
# Configuration Composition
# =========================================================


def _configuration_path(
    path: tuple[str, ...],
):
    """
    Render a configuration path.

    Examples
    --------
    ("title",)
        -> "title"

    ("context", "paths", "results")
        -> "context.paths.results"
    """

    return ".".join(
        path,
    )


def _warn_unknown_workspace_key(
    path: tuple[str, ...],
):
    """
    Warn about an unknown workspace
    configuration key.
    """

    warnings.warn(
        (f"Unknown workspace configuration key: {_configuration_path(path)!r}"),
        UserWarning,
        stacklevel=4,
    )


def _merge_workspace_definition(
    defaults: dict[str, Any],
    overrides: dict[str, Any],
    *,
    path: tuple[str, ...] = (),
):
    """
    Compose an effective workspace
    definition.

    Local configuration recursively
    overrides canonical defaults.

    The canonical workspace.toml template
    defines the recognized configuration
    schema.

    Unknown local configuration keys
    generate warnings and are ignored.

    TOML tables are recursively merged.

    Scalar values and arrays replace their
    corresponding canonical values.

    Parameters
    ----------
    defaults
        Canonical configuration at the
        current table level.

    overrides
        Local configuration at the
        current table level.

    path
        Configuration path represented by
        the current table.

    Returns
    -------
    dict
        Effective configuration for the
        current table.
    """

    #
    # Start with an independent copy of
    # the canonical configuration.
    #
    # deepcopy is intentional here because
    # TOML values may contain nested tables,
    # arrays, and arrays of tables.
    #

    definition = copy.deepcopy(
        defaults,
    )

    for key, override_value in overrides.items():
        key_path = (
            *path,
            key,
        )

        #
        # The template defines the schema.
        #

        if key not in defaults:
            _warn_unknown_workspace_key(
                key_path,
            )

            continue

        default_value = defaults[key]

        #
        # TOML tables are composed
        # recursively.
        #

        if isinstance(
            default_value,
            dict,
        ) and isinstance(
            override_value,
            dict,
        ):
            definition[key] = _merge_workspace_definition(
                default_value,
                override_value,
                path=key_path,
            )

            continue

        #
        # If the canonical value is a
        # table, a local non-table value is
        # structurally incompatible.
        #
        # Treat this like an invalid local
        # configuration value rather than
        # destroying the canonical table.
        #

        if isinstance(
            default_value,
            dict,
        ):
            warnings.warn(
                (
                    "Invalid workspace "
                    "configuration value for "
                    f"{_configuration_path(key_path)!r}: "
                    "expected a table."
                ),
                UserWarning,
                stacklevel=3,
            )

            continue

        #
        # Scalars and arrays replace the
        # canonical value as complete
        # values.
        #
        # In particular, arrays of tables
        # such as context.households are
        # intentionally not merged
        # element-by-element.
        #

        definition[key] = copy.deepcopy(
            override_value,
        )

    return definition


def _compose_workspace_definition(
    workspace_file: Path,
):
    """
    Compose the effective workspace
    definition for a local workspace file.

    This is the common implementation used
    by both row loading and the public
    definition loader.
    """

    defaults = _load_workspace_defaults()

    overrides = _load_workspace_toml(
        workspace_file,
    )

    return _merge_workspace_definition(
        defaults,
        overrides,
    )


# =========================================================
# Row Builders
# =========================================================


def _build_context_row(
    root: Path,
):
    """
    Build the canonical planning context.

    Every directory has a planning
    context regardless of whether an
    initialized workspace exists.
    """

    return {
        "_path": root.resolve(),
        "_meta": {
            "level": "workspace",
        },
        "_context": {
            "root": str(
                root.resolve(),
            ),
        },
    }


def _load_workspace_definition(
    row,
    workspace_dir: Path,
):
    """
    Attach effective workspace
    configuration to an existing
    planning context.

    Canonical defaults are loaded from
    the packaged workspace.toml template.

    Local workspace.toml values
    recursively override those defaults.
    """

    workspace_file = workspace_dir / WORKSPACE_TOML

    definition = _compose_workspace_definition(
        workspace_file,
    )

    row["_workspace"] = {
        "definition": definition,
        "definition_file": str(
            workspace_file.resolve(),
        ),
        "definition_note": ("workspace.toml defaults with local overrides"),
    }

    return row


# =========================================================
# Discovery
# =========================================================


def find_workspaces(
    source=".",
):
    """
    Discover initialized workspaces.

    A workspace is any immediate
    subdirectory containing
    workspace.toml.
    """

    source = Path(
        source,
    )

    if not source.exists():
        return []

    workspaces = []

    for child in sorted(
        source.iterdir(),
        key=lambda p: p.name.lower(),
    ):
        if child.is_dir() and (child / WORKSPACE_TOML).exists():
            workspaces.append(
                child,
            )

    return workspaces


# =========================================================
# Public Loaders
# =========================================================


def load_workspace_definition(
    workspace_dir=".",
):
    """
    Load the effective workspace
    definition.

    Canonical defaults are loaded from
    the packaged workspace.toml template.

    Local workspace.toml values
    recursively override those defaults.

    Unknown configuration keys generate
    warnings and are ignored.

    Parameters
    ----------
    workspace_dir
        Initialized workspace directory.

    Returns
    -------
    dict
        Effective workspace configuration.

    Raises
    ------
    FileNotFoundError
        If workspace.toml does not exist.
    """

    workspace_dir = Path(
        workspace_dir,
    ).resolve()

    workspace_file = workspace_dir / WORKSPACE_TOML

    if not workspace_file.exists():
        raise FileNotFoundError(f"Workspace definition not found: {workspace_file}")

    return _compose_workspace_definition(
        workspace_file,
    )


def load_workspace_row(
    workspace_dir=".",
):
    """
    Load a single planning context.

    If the directory is an initialized
    workspace, attach its effective
    workspace definition.
    """

    workspace_dir = Path(
        workspace_dir,
    ).resolve()

    row = _build_context_row(
        workspace_dir,
    )

    workspace_file = workspace_dir / WORKSPACE_TOML

    if workspace_file.exists():
        row = _load_workspace_definition(
            row,
            workspace_dir,
        )

    return row


def load_workspace_rows(
    source=".",
):
    """
    Load discovered workspaces.

    Each discovered workspace receives a
    sequential workspace identifier in
    discovery order.
    """

    rows = []

    for idx, workspace_dir in enumerate(
        find_workspaces(
            source,
        ),
    ):
        row = load_workspace_row(
            workspace_dir,
        )

        row["_meta"]["workspace_id"] = idx

        rows.append(
            row,
        )

    return rows
