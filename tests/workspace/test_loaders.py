# tests/workspace/test_loaders.py


from owlroost.workspace.loaders import (
    find_workspaces,
    load_workspace_rows,
)


def test_find_workspaces_empty(
    tmp_path,
):
    """
    No study.toml files produces
    no discovered workspaces.
    """

    assert (
        find_workspaces(
            tmp_path,
        )
        == []
    )


def test_find_workspaces_discovers_workspace(
    tmp_path,
):
    """
    Directories containing
    study.toml are workspaces.
    """

    ws = tmp_path / "example"

    ws.mkdir()

    (ws / "study.toml").write_text('name = "example"\n')

    workspaces = find_workspaces(
        tmp_path,
    )

    assert workspaces == [ws]


def test_find_workspaces_ignores_non_workspace_dirs(
    tmp_path,
):
    """
    Directories without study.toml
    are ignored.
    """

    (tmp_path / "foo").mkdir()

    workspaces = find_workspaces(
        tmp_path,
    )

    assert workspaces == []


def test_load_workspace_rows_empty(
    tmp_path,
):
    """
    Empty source directory
    produces no rows.
    """

    rows = load_workspace_rows(
        tmp_path,
    )

    assert rows == []


def test_load_workspace_rows_basic(
    sample_workspace,
):
    """
    Workspace metadata loads
    into display rows.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    row = rows[0]

    assert row["workspace_name"] == "example"

    assert row["workspace_title"] == "Example Study"

    assert row["workspace_description"] == "Example description."

    assert row["has_cases"] is False

    assert row["has_results"] is False


def test_load_workspace_rows_detects_cases(
    sample_workspace,
):
    """
    cases directory presence
    is detected.
    """

    (sample_workspace / "cases").mkdir()

    row = load_workspace_rows(
        sample_workspace.parent,
    )[0]

    assert row["has_cases"] is True


def test_load_workspace_rows_detects_results(
    sample_workspace,
):
    """
    results directory presence
    is detected.
    """

    (sample_workspace / "results").mkdir()

    row = load_workspace_rows(
        sample_workspace.parent,
    )[0]

    assert row["has_results"] is True


def test_load_workspace_rows_assigns_ids(
    tmp_path,
):
    """
    Workspace ids are assigned.
    """

    for name in [
        "alpha",
        "beta",
    ]:
        ws = tmp_path / name

        ws.mkdir()

        (ws / "study.toml").write_text(f'name = "{name}"\n')

    rows = load_workspace_rows(
        tmp_path,
    )

    ids = [row["_meta"]["workspace_id"] for row in rows]

    assert ids == [0, 1]
