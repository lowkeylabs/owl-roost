# tests/workspace/test_operations.py


import pytest

from owlroost.exceptions import (
    RoostError,
)
from owlroost.workspace.operations import (
    init_workspace,
    rename_workspace,
)


def test_rename_workspace(
    tmp_path,
):
    """
    Workspace directory can
    be renamed.
    """

    source_dir = tmp_path / "old_name"
    if not source_dir.exists():
        source_dir.mkdir()

    workspace = init_workspace(
        "old_name",
        parent=tmp_path,
    )

    renamed = rename_workspace(
        workspace,
        "new_name",
    )

    assert renamed.exists()

    assert renamed.name == "new_name"

    assert not workspace.exists()


def test_rename_workspace_missing_raises(
    tmp_path,
):
    """
    Missing workspaces
    raise errors.
    """

    with pytest.raises(
        RoostError,
    ):
        rename_workspace(
            tmp_path / "missing",
            "new_name",
        )


def test_rename_workspace_existing_target_raises(
    tmp_path,
):
    """
    Existing target names
    are rejected.
    """

    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"

    source_dir.mkdir()
    target_dir.mkdir()

    source = init_workspace(
        "source",
        parent=tmp_path,
    )

    init_workspace(
        "target",
        parent=tmp_path,
    )

    with pytest.raises(
        RoostError,
    ):
        rename_workspace(
            source,
            "target",
        )
