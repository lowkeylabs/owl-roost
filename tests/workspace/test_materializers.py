# tests/workspace/test_materializers.py

from owlroost.catalog.context import (
    build_catalog_context,
)
from owlroost.workspace.loaders import (
    load_workspace_rows,
)
from owlroost.workspace.materializers import (
    materialize_context,
    materialize_workspace,
)


def test_materialize_workspace_name(
    sample_workspace,
):
    """
    Workspace identity is materialized
    from semantic planning-context state.

    The workspace name is the workspace
    directory name rather than a
    configuration default.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    row = rows[0]

    catalog = build_catalog_context()

    #
    # Context observations must be
    # materialized first because workspace
    # observations may depend upon them.
    #

    materialize_context(
        row,
        catalog.workspace_registry,
    )

    materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    assert row["_workspace"]["name"] == sample_workspace.name


def test_materialize_workspace_overrides(
    sample_workspace,
):
    """
    Workspace overrides are materialized
    from the effective workspace
    configuration.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    row = rows[0]

    catalog = build_catalog_context()

    materialize_context(
        row,
        catalog.workspace_registry,
    )

    materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    workspace = row["_workspace"]

    definition = workspace["definition"]

    assert "workspace" in definition

    assert "overrides" in definition["workspace"]

    assert isinstance(
        workspace["overrides"],
        list,
    )


def test_materialize_workspace_preserves_definition(
    sample_workspace,
):
    """
    Semantic workspace materialization
    does not mutate or replace the
    effective workspace definition.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    row = rows[0]

    definition = row["_workspace"]["definition"]

    expected_title = definition["title"]

    expected_description = definition["description"]

    catalog = build_catalog_context()

    materialize_context(
        row,
        catalog.workspace_registry,
    )

    materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    assert row["_workspace"]["definition"]["title"] == expected_title

    assert row["_workspace"]["definition"]["description"] == expected_description
