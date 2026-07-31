# tests/workspace/test_materializers.py

from owlroost.catalog.context import (
    build_catalog_context,
)
from owlroost.workspace.loaders import (
    load_workspace_rows,
)
from owlroost.workspace.materializers import (
    materialize_workspace,
)


def test_materialize_workspace_inventory(
    sample_workspace,
):
    """
    Workspace inventory is
    materialized from defaults
    and workspace.toml.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    assert len(rows) == 1

    row = rows[0]

    catalog = build_catalog_context()

    materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    workspace = row["_workspace"]

    #
    # Overridden by workspace.toml.
    #
    assert workspace["name"] == "example"

    #
    # Defaulted by inventory.
    #
    assert workspace["test_field"] == ("default from ./workspace/inventory/workspace.py")


def test_materialize_workspace_defaults(
    sample_workspace,
):
    """
    Missing workspace.toml values
    fall back to inventory defaults.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    row = rows[0]

    #
    # Simulate an omitted value.
    #
    del row["_workspace"]["definition"]["name"]

    catalog = build_catalog_context()

    materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    workspace = row["_workspace"]

    #
    # Default comes from the inventory
    # compute function.
    #
    assert workspace["name"] == sample_workspace.name


def test_materialize_workspace_replaces_default(
    sample_workspace,
):
    """
    Workspace configuration
    replaces computed defaults.
    """

    rows = load_workspace_rows(
        sample_workspace.parent,
    )

    row = rows[0]

    catalog = build_catalog_context()

    materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    assert row["_workspace"]["name"] == row["_workspace"]["definition"]["name"]
