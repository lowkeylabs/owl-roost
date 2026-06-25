# tests/workspace/test_operations.py


import pytest

from owlroost.exceptions import (
    RoostError,
)
from owlroost.workspace.operations import (
    create_workspace,
    rename_workspace,
    validate_workspace,
)


def test_create_workspace(
    tmp_path,
):
    """
    Workspace creation writes
    required files.
    """

    workspace = create_workspace(
        "example",
        parent=tmp_path,
    )

    assert workspace.exists()

    assert (workspace / "workspace.toml").exists()

    assert (workspace / "Makefile").exists()


def test_create_workspace_existing_raises(
    tmp_path,
):
    """
    Existing workspace names
    are rejected.
    """

    (tmp_path / "example").mkdir()

    with pytest.raises(
        RoostError,
    ):
        create_workspace(
            "example",
            parent=tmp_path,
        )


def test_create_workspace_study_toml_contains_name(
    tmp_path,
):
    """
    Name is materialized into
    workspace.toml.
    """

    workspace = create_workspace(
        "example",
        parent=tmp_path,
    )

    contents = (workspace / "workspace.toml").read_text()

    assert 'name = "example"' in contents


def test_rename_workspace(
    tmp_path,
):
    """
    Workspace directory can
    be renamed.
    """

    workspace = create_workspace(
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

    source = create_workspace(
        "source",
        parent=tmp_path,
    )

    create_workspace(
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


def test_validate_workspace_valid(
    tmp_path,
):
    """
    Freshly created workspace
    validates successfully.
    """

    workspace = create_workspace(
        "example",
        parent=tmp_path,
    )

    errors = validate_workspace(
        workspace,
    )

    assert errors == []


def test_validate_workspace_missing_study_toml(
    tmp_path,
):
    """
    Missing workspace.toml is
    reported.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    (workspace / "Makefile").write_text("")

    errors = validate_workspace(
        workspace,
    )

    assert "missing workspace.toml" in errors


def test_validate_workspace_missing_makefile(
    tmp_path,
):
    """
    Missing Makefile is
    reported.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    (workspace / "workspace.toml").write_text("")

    errors = validate_workspace(
        workspace,
    )

    assert "missing Makefile" in errors
