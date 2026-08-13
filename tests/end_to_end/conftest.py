from __future__ import annotations

import re
import shutil
import subprocess
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from owlplanner.config import (
    config_to_plan,
    load_toml,
)

# =========================================================
# Test Cases
# =========================================================

CASE_ROOT = Path(__file__).parent / "cases"


# =========================================================
# Helpers
# =========================================================


def _safe_name(
    name: str,
) -> str:
    """
    Convert pytest node names into
    filesystem-safe session names.
    """

    return re.sub(
        r"[^A-Za-z0-9_.-]",
        "_",
        name,
    )


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


def load_plan_from_toml(
    toml_file: Path,
):
    """
    Load TOML into a real OWL Plan.
    """

    diconf, dirname, _ = load_toml(
        str(toml_file),
    )

    logstreams = [
        StringIO(),
        StringIO(),
    ]

    return config_to_plan(
        diconf,
        dirname,
        verbose=False,
        loadHFP=False,
        logstreams=logstreams,
    )


# =========================================================
# End-to-End Workspace
# =========================================================


@pytest.fixture
def e2e_workspace(
    tmp_path: Path,
):
    """
    Construct a neutral initialized
    workspace for end-to-end BUILD tests.

    Architectural invariant
    -----------------------
    ROOST BUILD operates within a planning
    workspace.

    End-to-end tests must therefore execute
    from a directory containing a valid
    workspace.toml.

    This workspace intentionally contributes
    no workspace overrides. Individual tests
    provide their own command-line overrides.
    """

    root = tmp_path / "workspace"

    root.mkdir()

    #
    # Minimal local workspace definition.
    #
    # Configuration not specified here is
    # inherited from the packaged workspace
    # template.
    #

    (root / "workspace.toml").write_text(
        """
title = "End-to-End Test Workspace"

description = '''
Neutral workspace used by ROOST end-to-end tests.
'''

[context.paths]

cases = "."
results = "./results"

[workspace]

overrides = []
""".lstrip(),
        encoding="utf-8",
    )

    #
    # Copy all case fixtures into the
    # temporary workspace.
    #
    # This includes case TOML files and
    # case-local artifacts such as HFP
    # spreadsheets.
    #

    assert CASE_ROOT.is_dir(), f"End-to-end case directory does not exist:\n{CASE_ROOT}"

    for source in CASE_ROOT.iterdir():
        if not source.is_file():
            continue

        shutil.copy2(
            source,
            root / source.name,
        )

    return root


# =========================================================
# Session Builder
# =========================================================


@pytest.fixture
def build_session(
    request,
    e2e_workspace: Path,
):
    """
    Build a deterministic ROOST session.

    BUILD is executed from a temporary
    initialized workspace so that workspace
    discovery and planning-context
    materialization participate in the
    end-to-end pipeline.

    Example
    -------

    session = build_session(
        "case_alex+jamie.toml",
        "roost_sweeps.ss_age_pair=69-69",
    )
    """

    def _build(
        case_name: str,
        *overrides: str,
    ) -> Path:
        case_path = e2e_workspace / case_name

        assert case_path.is_file(), f"Case file not found: {case_path}"

        session_date = "test"

        session_time = _safe_name(
            request.node.name,
        )

        session_root = e2e_workspace / "results" / case_path.stem / session_date / session_time

        if session_root.exists():
            shutil.rmtree(
                session_root,
            )

        #
        # Use the case path relative to the
        # workspace because ROOST itself is
        # executed with the workspace as cwd.
        #

        cmd = [
            "uv",
            "run",
            "roost",
            "build",
            case_path.name,
            *overrides,
            (f"session.date={session_date}"),
            (f"session.time={session_time}"),
        ]

        result = subprocess.run(
            cmd,
            cwd=e2e_workspace,
            text=True,
            capture_output=True,
        )

        if result.returncode != 0:
            print("\nSTDOUT")
            print(result.stdout)

            print("\nSTDERR")
            print(result.stderr)

            print("\nRESULTS TREE")

            results_root = e2e_workspace / "results" / case_path.stem

            if results_root.exists():
                for path in sorted(results_root.rglob("*")):
                    print(path.relative_to(e2e_workspace))
            else:
                print("No results directory")

        assert result.returncode == 0, (
            "\n"
            "ROOST build failed."
            "\n\n"
            "COMMAND:\n"
            f"{' '.join(cmd)}"
            "\n\n"
            "WORKSPACE:\n"
            f"{e2e_workspace}"
            "\n\n"
            "STDOUT:\n"
            f"{result.stdout}"
            "\n\n"
            "STDERR:\n"
            f"{result.stderr}"
        )

        assert session_root.is_dir(), f"Expected session directory was not created:\n{session_root}"

        return session_root

    return _build


# =========================================================
# Raw TOML Fixtures
# =========================================================


@pytest.fixture
def load_session_toml():
    """
    Load session.toml as a dict.
    """

    def _load(
        session_dir: Path,
    ):
        session_file = session_dir / "session.toml"

        assert session_file.is_file()

        return load_toml_file(
            session_file,
        )

    return _load


@pytest.fixture
def load_run_toml():
    """
    Load run_N/run.toml as a dict.
    """

    def _load(
        session_dir: Path,
        run_id: int = 0,
    ):
        run_file = session_dir / f"run_{run_id}" / "run.toml"

        assert run_file.is_file()

        return load_toml_file(
            run_file,
        )

    return _load


@pytest.fixture
def load_trial_toml():
    """
    Load trial_NNNN/trial.toml as a dict.
    """

    def _load(
        session_dir: Path,
        run_id: int = 0,
        trial_id: int = 0,
    ):
        trial_file = session_dir / f"run_{run_id}" / "trials" / f"{trial_id:04d}" / "trial.toml"

        assert trial_file.is_file()

        return load_toml_file(
            trial_file,
        )

    return _load


# =========================================================
# OWL Plan Fixtures
# =========================================================


@pytest.fixture
def load_run_plan():
    """
    Load run_N/run.toml into
    a real OWL Plan object.
    """

    def _load(
        session_dir: Path,
        run_id: int = 0,
    ):
        run_file = session_dir / f"run_{run_id}" / "run.toml"

        assert run_file.is_file()

        return load_plan_from_toml(
            run_file,
        )

    return _load


@pytest.fixture
def load_trial_plan():
    """
    Load trial_NNNN/trial.toml into
    a real OWL Plan object.
    """

    def _load(
        session_dir: Path,
        run_id: int = 0,
        trial_id: int = 0,
    ):
        trial_file = session_dir / f"run_{run_id}" / "trials" / f"{trial_id:04d}" / "trial.toml"

        assert trial_file.is_file()

        return load_plan_from_toml(
            trial_file,
        )

    return _load
