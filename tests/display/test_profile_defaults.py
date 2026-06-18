from __future__ import annotations

from owlroost.cli.utils import render_table
from owlroost.display.materializers.materialize import (
    materialize_view,
)
from owlroost.display.registry import (
    DisplayRegistry,
)
from owlroost.display.specs import (
    DisplayField,
    DisplayProfile,
    DisplayView,
)

# =========================================================
# Helpers
# =========================================================


def build_registry():
    reg = DisplayRegistry()

    reg.register_display_field(
        DisplayField.field(
            "x",
            profiles={
                "table": DisplayProfile(
                    label=None,
                    fmt=None,
                    label_align=None,
                    content_align=None,
                    width=None,
                    min_width=None,
                    max_width=None,
                    wrap=None,
                    visible=None,
                ),
            },
        )
    )

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[
                "x",
            ],
        )
    )

    reg.validate()

    return reg


# =========================================================
# Sentinel Tests
# =========================================================


def test_none_profile_attributes_materialize():
    """
    Sentinel test.

    Documents what happens if DisplayProfile
    eventually migrates to overlay semantics
    where unspecified attributes are None.

    This test intentionally constructs a
    profile that violates current defaults
    and verifies whether materialization
    survives.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[
            {
                "_inputs": {
                    "x": 123,
                },
            }
        ],
        registry=reg,
        level="case",
        view_name="basic",
    )

    assert table.rows == [
        [123],
    ]


def test_none_profile_attributes_column_defaults():
    """
    Sentinel test.

    Reveals whether materialization assumes
    label_align/content_align/wrap are
    always populated.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[
            {
                "_inputs": {
                    "x": 123,
                },
            }
        ],
        registry=reg,
        level="case",
        view_name="basic",
    )

    column = table.columns[0]

    #
    # We intentionally make only weak
    # assertions here.
    #
    # If this test fails during a future
    # migration, the failure tells us
    # exactly where defaulting needs to
    # move.
    #

    assert column is not None


def test_none_profile_attributes_empty_table():
    """
    Sentinel test.

    Empty-row materialization often hits
    slightly different paths.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[],
        registry=reg,
        level="case",
        view_name="basic",
    )

    assert table.rows == []


def test_none_profile_attributes_pivot():
    """
    Sentinel test.

    Verifies pivot materialization survives
    None-valued profile attributes.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[
            {
                "_inputs": {
                    "x": 123,
                },
            }
        ],
        registry=reg,
        level="case",
        view_name="basic",
        mode="pivot",
    )

    assert table is not None

    assert len(table.rows) > 0


def test_none_profile_attributes_explain():
    """
    Sentinel test.

    Verifies explain-mode materialization
    survives None-valued profile attributes.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[
            {
                "_inputs": {
                    "x": 123,
                },
            }
        ],
        registry=reg,
        level="case",
        view_name="basic",
        mode="pivot",
        explain_facets={
            "description",
        },
    )

    assert table is not None

    assert len(table.rows) > 0


def test_none_profile_attributes_are_resolved():
    """
    Sentinel test.

    None-valued profile attributes should
    be materialized into renderer-facing
    defaults during profile resolution.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[
            {
                "_inputs": {
                    "x": 123,
                },
            }
        ],
        registry=reg,
        level="case",
        view_name="basic",
    )

    column = table.columns[0]

    assert column.label == "x"

    assert column.label_align == "left"

    assert column.content_align == "left"

    assert column.wrap is False


def test_none_profile_attributes_render():
    """
    Sentinel test.

    Verify a table containing None-valued
    column attributes can be rendered.
    """

    reg = build_registry()

    table = materialize_view(
        rows=[
            {
                "_inputs": {
                    "x": 123,
                },
            }
        ],
        registry=reg,
        level="case",
        view_name="basic",
    )

    render_table(
        table,
        "html",
    )

    render_table(
        table,
        "markdown",
    )
