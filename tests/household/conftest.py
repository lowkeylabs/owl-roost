# tests/household/conftest.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household test fixtures.

## Notes

Provides reusable fixtures for the
Household subsystem test suite.

Tests exercising Household bootstrap
operate within an explicit temporary
workspace context.

The temporary workspace uses the
canonical packaged workspace.toml
template so tests exercise the same
Household Library configuration used
by production code.

## Architectural Invariants

Tests should construct Household
Registries through the public
bootstrap interface whenever
practical.

Bootstrap tests must provide an
explicit workspace context rather
than depend on the pytest process
working directory.

Temporary Household Libraries should
be used for filesystem mutation tests.

The canonical workspace.toml template
defines Household Library search
policy.
"""

from __future__ import annotations

import shutil

import pytest

from owlroost.core.settings import (
    get_workspace_template_dir,
)
from owlroost.household.bootstrap import (
    build_household_registry,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
    HouseholdSpec,
)

# =========================================================
# Workspace Context
# =========================================================


@pytest.fixture
def workspace_root(
    tmp_path,
):
    """
    Temporary workspace root.

    The workspace definition is copied
    from the canonical packaged
    workspace.toml template.
    """

    root = tmp_path / "workspace"

    root.mkdir()

    template_file = get_workspace_template_dir() / "workspace" / "workspace.toml"

    shutil.copyfile(
        template_file,
        root / "workspace.toml",
    )

    return root


# =========================================================
# Registry
# =========================================================


@pytest.fixture
def registry(
    workspace_root,
):
    """
    Return the Household Registry
    visible to the temporary workspace
    context.
    """

    return build_household_registry(
        root=workspace_root,
    )


# =========================================================
# Household Libraries
# =========================================================


@pytest.fixture
def writable_library(
    tmp_path,
):
    """
    Temporary writable Household
    Library.
    """

    root = tmp_path / "households"

    root.mkdir()

    return HouseholdLibrarySpec(
        name="test",
        root=root,
        read_only=False,
    )


@pytest.fixture
def readonly_library(
    tmp_path,
):
    """
    Temporary read-only Household
    Library.
    """

    root = tmp_path / "builtin"

    root.mkdir()

    return HouseholdLibrarySpec(
        name="builtin",
        root=root,
        read_only=True,
    )


# =========================================================
# Household Projects
# =========================================================


@pytest.fixture
def household(
    writable_library,
):
    """
    Temporary Household Project.
    """

    root = writable_library.root / "smith"

    root.mkdir()

    return HouseholdSpec(
        title="Smith Household",
        library=writable_library,
        root=root,
    )
