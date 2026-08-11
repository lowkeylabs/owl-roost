# tests/workspace/test_loaders.py

from __future__ import annotations

import pytest

from owlroost.workspace.loaders import (
    find_workspaces,
    load_workspace_definition,
    load_workspace_row,
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

    Discovery depends only on the
    presence of workspace.toml.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    (workspace / "workspace.toml").write_text(
        "",
        encoding="utf-8",
    )

    workspaces = find_workspaces(
        tmp_path,
    )

    assert workspaces == [
        workspace,
    ]


def test_find_workspaces_ignores_non_workspace_dirs(
    tmp_path,
):
    """
    Directories without workspace.toml
    are not workspaces.
    """

    (tmp_path / "example").mkdir()

    assert (
        find_workspaces(
            tmp_path,
        )
        == []
    )


def test_load_workspace_row_context(
    tmp_path,
):
    """
    Every directory produces a planning
    context even when it is not an
    initialized workspace.
    """

    row = load_workspace_row(
        tmp_path,
    )

    assert row["_path"] == (tmp_path.resolve())

    assert row["_meta"]["level"] == "workspace"

    assert row["_context"]["root"] == str(tmp_path.resolve())

    assert "_workspace" not in row


def test_load_workspace_rows_assigns_ids(
    sample_workspace,
):
    """
    Discovered workspaces receive
    sequential workspace identifiers.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    assert rows[0]["_meta"]["workspace_id"] == 0


def test_load_workspace_definition_applies_local_overrides(
    sample_workspace,
):
    """
    Local workspace configuration
    overrides canonical template
    defaults.
    """

    definition = load_workspace_definition(
        sample_workspace,
    )

    #
    # These values are supplied by the
    # local sample workspace.
    #

    assert definition["title"] == "Workspace"


def test_load_workspace_rows_basic(
    sample_workspace,
):
    """
    Effective workspace configuration
    is attached to workspace rows.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    workspace = rows[0]["_workspace"]

    assert "definition" in workspace

    definition = workspace["definition"]

    assert definition["title"] == "Workspace"


def test_load_workspace_definition_supplies_template_defaults(
    tmp_path,
):
    """
    Values omitted from local
    workspace.toml are supplied by the
    canonical workspace template.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    #
    # An empty local definition should
    # inherit the complete canonical
    # template.
    #

    (workspace / "workspace.toml").write_text(
        "",
        encoding="utf-8",
    )

    definition = load_workspace_definition(
        workspace,
    )

    assert "title" in definition
    assert "description" in definition

    assert "workspace" in definition
    assert "overrides" in (definition["workspace"])

    assert "context" in definition

    assert "households" in (definition["context"])

    assert "paths" in (definition["context"])

    assert "cases" in (definition["context"]["paths"])

    assert "results" in (definition["context"]["paths"])


def test_load_workspace_definition_applies_nested_overrides(
    tmp_path,
):
    """
    Local nested configuration values
    override corresponding canonical
    template values without removing
    sibling defaults.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    (workspace / "workspace.toml").write_text(
        "\n".join(
            [
                "[context.paths]",
                'results = "./custom-results"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    definition = load_workspace_definition(
        workspace,
    )

    assert definition["context"]["paths"]["results"] == "./custom-results"

    #
    # The sibling template default must
    # survive the nested merge.
    #

    assert "cases" in (definition["context"]["paths"])


def test_load_workspace_definition_warns_unknown_keys(
    tmp_path,
):
    """
    Unknown local workspace configuration
    keys generate a warning and are not
    added to the effective definition.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    (workspace / "workspace.toml").write_text(
        "\n".join(
            [
                'unknown_setting = "value"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.warns(
        UserWarning,
        match=("Unknown workspace configuration key"),
    ):
        definition = load_workspace_definition(
            workspace,
        )

    assert "unknown_setting" not in definition


def test_load_workspace_definition_warns_unknown_nested_keys(
    tmp_path,
):
    """
    Unknown nested configuration keys
    also generate warnings and are not
    added to the effective definition.
    """

    workspace = tmp_path / "example"

    workspace.mkdir()

    (workspace / "workspace.toml").write_text(
        "\n".join(
            [
                "[context.paths]",
                'unknown_path = "./somewhere"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.warns(
        UserWarning,
        match=("Unknown workspace configuration key"),
    ):
        definition = load_workspace_definition(
            workspace,
        )

    assert "unknown_path" not in definition["context"]["paths"]


def test_load_workspace_rows_preserves_workspace_path(
    sample_workspace,
):
    """
    Loaded workspace rows retain the
    canonical workspace filesystem path.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    assert rows[0]["_path"] == sample_workspace.resolve()


def test_load_workspace_rows_contains_results_configuration(
    sample_workspace,
):
    """
    Effective workspace configuration
    contains the configured results path.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    definition = rows[0]["_workspace"]["definition"]

    assert "results" in (definition["context"]["paths"])
