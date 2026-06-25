# tests/workspace/conftest.py

from __future__ import annotations

import pytest


@pytest.fixture
def workspace_root(
    tmp_path,
):
    """
    Temporary workspace root.
    """

    return tmp_path


@pytest.fixture
def sample_workspace(
    workspace_root,
):
    """
    Single initialized workspace.
    """

    ws = workspace_root / "example"

    ws.mkdir()

    (ws / "workspace.toml").write_text(
        """
name = "example"

title = "Example Workspace"

description = "Example description."
"""
    )

    (ws / "Makefile").write_text("-include $(shell roost info --path=makefile)\n")

    return ws


# =====================================================
# Household Fixtures
# =====================================================


@pytest.fixture
def workspace_with_household(
    sample_workspace,
):
    """
    Workspace containing a single
    household TOML.
    """

    (sample_workspace / "case.toml").write_text(
        """
name = "Example Household"
"""
    )

    return sample_workspace


@pytest.fixture
def workspace_with_hfp(
    workspace_with_household,
):
    """
    Workspace containing a
    household and HFP workbook.
    """

    (workspace_with_household / "case.xlsx").write_text(
        "",
    )

    return workspace_with_household


@pytest.fixture
def workspace_with_multiple_households(
    sample_workspace,
):
    """
    Workspace containing multiple
    household TOMLs.
    """

    (sample_workspace / "case1.toml").write_text(
        "",
    )

    (sample_workspace / "case2.toml").write_text(
        "",
    )

    return sample_workspace


# =====================================================
# Inventory Fixtures
# =====================================================


@pytest.fixture
def workspace_with_cases(
    sample_workspace,
):
    """
    Workspace containing a
    cases directory.
    """

    (sample_workspace / "cases").mkdir()

    return sample_workspace


@pytest.fixture
def workspace_with_results(
    sample_workspace,
):
    """
    Workspace containing a
    results directory.
    """

    (sample_workspace / "results").mkdir()

    return sample_workspace


@pytest.fixture
def workspace_with_reports(
    sample_workspace,
):
    """
    Workspace containing a
    reports directory.
    """

    (sample_workspace / "reports").mkdir()

    return sample_workspace
