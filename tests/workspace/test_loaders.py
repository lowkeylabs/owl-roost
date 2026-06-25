# tests/workspace/test_loaders.py


from owlroost.workspace.loaders import (
    find_workspaces,
    load_workspace_rows,
)


def test_find_workspaces_empty(
    tmp_path,
):
    """
    No workspace.toml files produces
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
    workspace.toml are workspaces.
    """

    ws = tmp_path / "example"

    ws.mkdir()

    (ws / "workspace.toml").write_text('name = "example"\n')

    workspaces = find_workspaces(
        tmp_path,
    )

    assert workspaces == [ws]


def test_find_workspaces_ignores_non_workspace_dirs(
    tmp_path,
):
    """
    Directories without workspace.toml
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

        (ws / "workspace.toml").write_text(f'name = "{name}"\n')

    rows = load_workspace_rows(
        tmp_path,
    )

    ids = [row["_meta"]["workspace_id"] for row in rows]

    assert ids == [0, 1]


def test_load_workspace_rows_basic(
    sample_workspace,
):
    """
    Workspace metadata loads
    into workspace rows.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    row = rows[0]

    workspace = row["_workspace"]

    assert workspace["name"] == "example"

    assert workspace["title"] == "Example Study"

    assert workspace["description"] == "Example description."


def test_load_workspace_rows_detects_cases(
    sample_workspace,
):
    """
    cases directory presence
    is detected.
    """

    (sample_workspace / "cases").mkdir()

    _row = load_workspace_rows(
        sample_workspace.parent,
    )[0]


def test_load_workspace_rows_detects_results(
    sample_workspace,
):
    """
    results directory presence
    is detected.
    """

    (sample_workspace / "results").mkdir()

    _row = load_workspace_rows(
        sample_workspace.parent,
    )[0]
