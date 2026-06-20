# tests/workspace/conftest.py


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
    Single valid workspace.
    """

    ws = workspace_root / "example"

    ws.mkdir()

    (ws / "study.toml").write_text(
        """
name = "example"

title = "Example Study"

description = "Example description."
"""
    )

    (ws / "Makefile").write_text("-include $(shell roost paths --makefile)\n")

    return ws
