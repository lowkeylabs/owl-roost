# tests/household/test_minimum.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for the built-in Minimum Household
Project.

Notes
-----
The Minimum Household establishes the
smallest executable Household Project
supported by ROOST.

It serves as the architectural reference
for future household projects.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_household_module(
    household_file: Path,
):
    """
    Import a household.py module from a
    Household Project.
    """

    spec = importlib.util.spec_from_file_location(
        "minimum_household",
        household_file,
    )

    assert spec is not None

    assert spec.loader is not None

    module = importlib.util.module_from_spec(
        spec,
    )

    spec.loader.exec_module(
        module,
    )

    return module


def test_minimum_household_project_exists(
    registry,
):
    """
    The built-in minimum Household Project
    is discoverable.
    """

    spec = registry.get_household(
        "minimum",
    )

    assert spec.exists


def test_minimum_household_contains_manifest(
    registry,
):
    """
    Every Household Project contains a
    manifest.
    """

    spec = registry.get_household(
        "minimum",
    )

    assert spec.manifest_file.is_file()


def test_minimum_household_contains_household_py(
    registry,
):
    """
    Every executable Household Project
    contains household.py.
    """

    spec = registry.get_household(
        "minimum",
    )

    assert spec.household_file.is_file()


def test_minimum_household_imports(
    registry,
):
    """
    household.py imports successfully.
    """

    spec = registry.get_household(
        "minimum",
    )

    module = load_household_module(
        spec.household_file,
    )

    assert module is not None


def test_minimum_household_exports_required_functions(
    registry,
):
    """
    Executable specifications export the
    expected public interface.
    """

    spec = registry.get_household(
        "minimum",
    )

    module = load_household_module(
        spec.household_file,
    )

    assert hasattr(
        module,
        "create_plan",
    )

    assert hasattr(
        module,
        "write_household",
    )

    assert hasattr(
        module,
        "main",
    )


def test_minimum_create_plan(
    registry,
):
    """
    create_plan() is callable.

    Future revisions may return an OWL
    Plan.
    """

    spec = registry.get_household(
        "minimum",
    )

    module = load_household_module(
        spec.household_file,
    )

    plan = module.create_plan()

    #
    # Placeholder implementation.
    #
    assert plan is None


def test_minimum_write_household_not_implemented(
    registry,
):
    """
    Placeholder implementation raises.
    """

    spec = registry.get_household(
        "minimum",
    )

    module = load_household_module(
        spec.household_file,
    )

    with pytest.raises(
        RuntimeError,
    ):
        module.write_household(
            None,
        )


def test_minimum_household_artifacts(
    registry,
):
    """
    The Minimum Household contains the
    expected project artifacts.
    """

    spec = registry.get_household(
        "minimum",
    )

    assert spec.artifact_names == (
        "household.py",
        "manifest.toml",
    )
