# tests/operations/test_resolve.py

from types import SimpleNamespace

from owlroost.activity.materializers import (
    materialize_activity,
    materialize_activity_trees,
)
from owlroost.catalog.context import (
    build_catalog_context,
)
from owlroost.display.operations.resolution import (
    resolve_field_description,
    resolve_field_object,
    resolve_field_value,
)
from owlroost.workspace.loaders import (
    load_workspace_row,
)
from owlroost.workspace.materializers import (
    materialize_context,
    materialize_context_tree,
    materialize_study,
    materialize_study_tree,
    materialize_workspace,
    materialize_workspace_tree,
)

# =========================================================
# Unit-test helpers
# =========================================================


class DummyDisplayRegistry:
    def get(
        self,
        field_name,
    ):
        return None


def make_fake_catalog():
    return SimpleNamespace(
        catalog_index={
            "context.workspace.case_count": {},
            "workspace.identity.name": {},
            "activity.workspace.initialize": {},
        },
        display_registry=DummyDisplayRegistry(),
    )


def make_fake_row():
    return {
        "_context": {
            "case_count": 5,
        },
        "_workspace": {
            "identity": {
                "name": "Example",
            },
        },
        "_activity": {
            "workspace": {
                "initialize": "roost workspace --init",
            },
        },
    }


# =========================================================
# Integration helper
# =========================================================


def make_context():
    """
    Build a fully materialized planning
    context.
    """

    catalog = build_catalog_context()

    row = load_workspace_row(".")

    row = materialize_context(
        row,
        catalog.workspace_registry,
    )
    row = materialize_context_tree(
        row,
        catalog.workspace_registry,
    )

    row = materialize_workspace(
        row,
        catalog.workspace_registry,
    )
    row = materialize_workspace_tree(
        row,
        catalog.workspace_registry,
    )

    row = materialize_study(
        row,
        catalog.study_registry,
    )
    row = materialize_study_tree(
        row,
        catalog.study_registry,
    )

    row = materialize_activity(
        row,
        catalog.activity_registry,
    )

    row = materialize_activity_trees(
        row,
    )

    return catalog, row


# =========================================================
# Unit tests
# =========================================================


def test_resolve_field_value_context():
    row = make_fake_row()

    assert (
        resolve_field_value(
            row,
            "context.case_count",
        )
        == 5
    )


def test_resolve_field_value_workspace():
    row = make_fake_row()

    assert (
        resolve_field_value(
            row,
            "workspace.identity.name",
        )
        == "Example"
    )


def test_resolve_field_value_missing():
    row = make_fake_row()

    assert (
        resolve_field_value(
            row,
            "missing.variable",
        )
        is None
    )


def test_resolve_field_object_missing():
    row = make_fake_row()

    obj, property_path = resolve_field_object(
        row,
        "missing.variable",
    )

    assert obj is None
    assert property_path is None


def test_resolve_field_description_missing():
    row = make_fake_row()

    assert (
        resolve_field_description(
            row,
            "missing.variable",
        )
        == ""
    )


def test_resolve_field_value_requires_row():
    try:
        resolve_field_value(
            None,
            "context.case_count",
        )
    except AttributeError:
        #
        # Resolver expects a materialized row.
        #
        pass
    else:
        raise AssertionError("resolve_field_value() should require a row")


# =========================================================
# Integration test
# =========================================================


def test_resolution_integration():
    """
    Ensure semantic field resolution works
    against a fully materialized planning
    context.
    """

    catalog, row = make_context()

    assert isinstance(
        resolve_field_value(
            row,
            "context.workspace.case_count",
        ),
        int,
    )

    assert (
        resolve_field_value(
            row,
            "activity.workspace.initialize",
        )
        is not None
    )

    assert (
        resolve_field_description(
            row,
            "activity.workspace.initialize",
        )
        != ""
    )
