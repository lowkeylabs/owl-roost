from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

# =========================================================
# Helpers
# =========================================================


def load_toml_file(
    path: Path,
):
    """
    Load TOML into a raw dict.
    """

    with path.open(
        "rb",
    ) as fp:
        return tomllib.load(
            fp,
        )


# =========================================================
# Workspace Override Configuration
# =========================================================


@pytest.fixture
def workspace_with_overrides(
    e2e_workspace: Path,
):
    """
    Configure the shared end-to-end
    workspace with a persistent workspace
    override.

    The ordinary E2E workspace is neutral:

        workspace.overrides = []

    This fixture changes only the workspace
    configuration required by these tests.

    The workspace override intentionally
    conflicts with command-line overrides
    used by the precedence tests.
    """

    workspace_file = e2e_workspace / "workspace.toml"

    assert workspace_file.is_file()

    workspace_file.write_text(
        """
title = "End-to-End Override Test"

description = '''
Workspace used to verify override precedence.
'''

[context.paths]

cases = "."
results = "./results"

[workspace]

overrides = [
    "solver_options.bequest=300",
]
""".lstrip(),
        encoding="utf-8",
    )

    return e2e_workspace


# =========================================================
# Session Builder
# =========================================================


@pytest.fixture
def build_workspace_session(
    build_session,
    workspace_with_overrides: Path,
):
    """
    Build a ROOST session using the shared
    workspace-based end-to-end fixture with
    workspace overrides enabled.

    Notes
    -----
    build_session already owns:

        * execution from the workspace
        * deterministic session naming
        * results cleanup
        * subprocess execution
        * build failure diagnostics

    This fixture exists only to ensure that
    workspace_with_overrides is materialized
    before build_session executes.
    """

    def _build(
        case_name: str,
        *overrides: str,
    ) -> Path:
        return build_session(
            case_name,
            *overrides,
        )

    return _build


# =========================================================
# Workspace Override Propagation
# =========================================================


def test_workspace_overrides_are_applied(
    build_workspace_session,
    load_run_toml,
):
    """
    Workspace overrides participate in
    the generated run configuration.

    The workspace specifies:

        solver_options.bequest=300

    With no conflicting command-line
    override, the generated run must
    therefore contain:

        solver_options.bequest = 300
    """

    session = build_workspace_session(
        "case_alex+jamie.toml",
    )

    run = load_run_toml(
        session,
        run_id=0,
    )

    assert run["solver_options"]["bequest"] == 300


def test_workspace_overrides_are_recorded_in_provenance(
    build_workspace_session,
    load_run_toml,
):
    """
    Workspace overrides are recorded
    separately from command-line/orphan
    overrides in ROOST provenance.

    With no explicit command-line
    overrides, workspace provenance must
    contain the workspace contribution.
    """

    session = build_workspace_session(
        "case_alex+jamie.toml",
    )

    run = load_run_toml(
        session,
        run_id=0,
    )

    settings = run["roost_settings"]

    assert "solver_options.bequest=300" in settings["workspace_overrides"]

    assert "orphan_overrides" in settings


# =========================================================
# Override Precedence
# =========================================================


def test_cli_overrides_replace_workspace_overrides(
    build_workspace_session,
    load_run_toml,
):
    """
    Command-line overrides take precedence
    over persistent workspace overrides.

    Precedence:

        workspace
            <
        command line / orphan

    Experiment override behavior is tested
    independently by the Study subsystem.

    The workspace requests:

        solver_options.bequest=300

    The command line requests:

        solver_options.bequest=200

    Therefore the effective value must be:

        solver_options.bequest=200
    """

    session = build_workspace_session(
        "case_alex+jamie.toml",
        "solver_options.bequest=200",
    )

    run = load_run_toml(
        session,
        run_id=0,
    )

    assert run["solver_options"]["bequest"] == 200


def test_workspace_and_cli_overrides_preserve_provenance(
    build_workspace_session,
    load_run_toml,
):
    """
    Workspace and command-line overrides
    retain separate provenance even when
    they target the same setting.

    Effective precedence is:

        workspace
            <
        command line / orphan

    Provenance nevertheless preserves both
    contributions.
    """

    session = build_workspace_session(
        "case_alex+jamie.toml",
        "solver_options.bequest=200",
    )

    run = load_run_toml(
        session,
        run_id=0,
    )

    # =====================================================
    # Effective Configuration
    # =====================================================

    assert run["solver_options"]["bequest"] == 200

    # =====================================================
    # Configuration Provenance
    # =====================================================

    settings = run["roost_settings"]

    assert "solver_options.bequest=300" in settings["workspace_overrides"]

    assert "solver_options.bequest=200" in settings["orphan_overrides"]
