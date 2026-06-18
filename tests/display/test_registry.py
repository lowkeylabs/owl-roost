# tests/display/test_registry.py

from __future__ import annotations

import pytest

from owlroost.core.utils import normalize_module_path
from owlroost.display.registry import (
    DisplayRegistry,
)
from owlroost.display.specs import (
    DisplayField,
    DisplayGroup,
    DisplayProfile,
    DisplayView,
)
from owlroost.exceptions import (
    RoostError,
)

# =========================================================
# Helpers
# =========================================================


def make_field(
    name: str,
    **kwargs,
):
    return DisplayField.field(
        name,
        **kwargs,
    )


# =========================================================
# Display Fields
# =========================================================


def test_register_display_field():
    reg = DisplayRegistry()

    field = make_field(
        "runtime.trial_jobs",
    )

    reg.register_display_field(field)

    loaded = reg.get_display_field(
        "runtime.trial_jobs",
    )

    assert loaded is field


def test_display_field_override():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field("x"),
    )

    reg.register_display_field(
        make_field(
            "x",
            description="override",
        )
    )

    field = reg.get_display_field(
        "x",
    )

    assert field.description == "override"


def test_missing_display_field_raises():
    reg = DisplayRegistry()

    with pytest.raises(KeyError):
        reg.get_display_field(
            "missing.field",
        )


def test_has_display_field():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field(
            "runtime.trial_jobs",
        )
    )

    assert reg.has_display_field(
        "runtime.trial_jobs",
    )

    assert not reg.has_display_field(
        "missing.field",
    )


def test_all_display_fields():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field("a"),
    )

    reg.register_display_field(
        make_field("b"),
    )

    fields = reg.all_display_fields()

    names = {field.field_name for field in fields}

    assert names == {
        "a",
        "b",
    }


def test_all_alias():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field("a"),
    )

    fields = reg.all()

    assert len(fields) == 1

    assert fields[0].field_name == "a"


# =========================================================
# Groups
# =========================================================


def test_register_group():
    reg = DisplayRegistry()

    group = DisplayGroup(
        key="runtime",
        entries=[
            "runtime.trial_jobs",
        ],
    )

    reg.register_group(group)

    loaded = reg.get_group(
        "runtime",
    )

    assert loaded is group


def test_duplicate_group_raises():
    reg = DisplayRegistry()

    reg.register_group(
        DisplayGroup(
            key="runtime",
            entries=[],
        )
    )

    with pytest.raises(ValueError):
        reg.register_group(
            DisplayGroup(
                key="runtime",
                entries=[],
            )
        )


def test_missing_group_raises():
    reg = DisplayRegistry()

    with pytest.raises(KeyError):
        reg.get_group(
            "missing",
        )


def test_has_group():
    reg = DisplayRegistry()

    reg.register_group(
        DisplayGroup(
            key="runtime",
            entries=[],
        )
    )

    assert reg.has_group(
        "runtime",
    )

    assert not reg.has_group(
        "missing",
    )


# =========================================================
# Views
# =========================================================


def test_register_view():
    reg = DisplayRegistry()

    view = DisplayView(
        level="case",
        name="basic",
        entries=[],
    )

    reg.register_view(view)

    loaded = reg.get_view(
        "case",
        "basic",
    )

    assert loaded is view


def test_duplicate_view_raises():
    reg = DisplayRegistry()

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[],
        )
    )

    with pytest.raises(ValueError):
        reg.register_view(
            DisplayView(
                level="case",
                name="basic",
                entries=[],
            )
        )


def test_row_view_fallback():
    reg = DisplayRegistry()

    view = DisplayView(
        level="row",
        name="balance_sheet",
        entries=[],
    )

    reg.register_view(view)

    loaded = reg.get_view(
        "case",
        "balance_sheet",
    )

    assert loaded is view


def test_missing_view_raises():
    reg = DisplayRegistry()

    with pytest.raises(
        RoostError,
        match="DisplayView not found",
    ):
        reg.get_view(
            "case",
            "missing",
        )


def test_has_view():
    reg = DisplayRegistry()

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[],
        )
    )

    assert reg.has_view(
        "case",
        "basic",
    )

    assert not reg.has_view(
        "case",
        "missing",
    )


# =========================================================
# Summary
# =========================================================


def test_registry_summary_counts():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field(
            "runtime.trial_jobs",
        )
    )

    reg.register_group(
        DisplayGroup(
            key="runtime",
            entries=[],
        )
    )

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[],
        )
    )

    summary = reg.summary()

    assert summary == {
        "display_fields": 1,
        "groups": 1,
        "views": 1,
        "dashboards": 0,
    }


# =========================================================
# Validation
# =========================================================


def test_validate_group_field_reference():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field(
            "runtime.trial_jobs",
        )
    )

    reg.register_group(
        DisplayGroup(
            key="runtime",
            entries=[
                "runtime.trial_jobs",
            ],
        )
    )

    reg.validate()


def test_validate_missing_group_field_raises():
    reg = DisplayRegistry()

    reg.register_group(
        DisplayGroup(
            key="runtime",
            entries=[
                "missing.field",
            ],
        )
    )

    with pytest.raises(ValueError):
        reg.validate()


def test_validate_view_group_reference():
    reg = DisplayRegistry()

    reg.register_group(
        DisplayGroup(
            key="runtime",
            entries=[],
        )
    )

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[
                ("group", "runtime"),
            ],
        )
    )

    reg.validate()


def test_validate_missing_view_group_raises():
    reg = DisplayRegistry()

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[
                ("group", "missing_group"),
            ],
        )
    )

    with pytest.raises(ValueError):
        reg.validate()


def test_validate_view_field_reference():
    reg = DisplayRegistry()

    reg.register_display_field(
        make_field(
            "runtime.trial_jobs",
        )
    )

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[
                ("field", "runtime.trial_jobs"),
            ],
        )
    )

    reg.validate()


def test_validate_missing_view_field_raises():
    reg = DisplayRegistry()

    reg.register_view(
        DisplayView(
            level="case",
            name="basic",
            entries=[
                ("field", "missing.field"),
            ],
        )
    )

    with pytest.raises(ValueError):
        reg.validate()


# =========================================================
# Catalog Declarations
# =========================================================


def test_catalog_declaration_defaults_none():
    """
    Presentation-only display fields should
    not require catalog declarations.
    """

    field = DisplayField.field(
        "runtime.trial_jobs",
    )

    assert field.catalog_declaration is None


def test_synthetic_field_creates_catalog_declaration():
    """
    Ontology declarations should produce a
    catalog declaration.
    """

    field = DisplayField.field(
        "example.synthetic",
        owner="ROOST",
        semantic_domain="execution",
        value_origin="roost-computed",
        projection_kind="synthetic",
        defined_in=normalize_module_path(__file__),
    )

    assert field.catalog_declaration is not None

    assert field.catalog_declaration.owner == "ROOST"


def test_lineage_requires_ontology():
    """
    Lineage metadata represents semantic
    lineage and therefore requires
    ontology metadata.
    """

    with pytest.raises(
        ValueError,
        match=("lineage metadata requires ontology metadata"),
    ):
        DisplayField.field(
            "example.overlay",
            derived_from=[
                "solver_options.bequest",
            ],
        )


def test_lineage_with_ontology_creates_catalog_declaration():
    """
    Semantic declarations carrying lineage
    should synthesize a CatalogSpec.
    """

    field = DisplayField.field(
        "example.overlay",
        owner="ROOST",
        semantic_domain="execution",
        value_origin="roost-computed",
        projection_kind="synthetic",
        derived_from=[
            "solver_options.bequest",
        ],
        defined_in=normalize_module_path(__file__),
    )

    declaration = field.catalog_declaration

    assert declaration is not None

    assert declaration.derived_from == [
        "solver_options.bequest",
    ]


# =========================================================
# Profiles
# =========================================================


def test_display_field_profiles():
    field = DisplayField.field(
        "runtime.trial_jobs",
        profiles={
            "table": DisplayProfile(
                label="Jobs",
            ),
            "pivot": DisplayProfile(
                label=("Parallel Trial Workers"),
            ),
        },
    )

    assert field.profiles["table"].label == "Jobs"

    assert field.profiles["pivot"].label == "Parallel Trial Workers"


def test_display_field_registration_merges_field_metadata():
    """
    Re-registering a DisplayField overlays
    field metadata.

    Unspecified attributes are preserved
    from the previously registered field.
    """

    reg = DisplayRegistry()

    reg.register_display_field(
        DisplayField.field(
            "x",
            description="Original description",
            notes="Original notes",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "x",
            defined_in="overlay.py",
        )
    )

    field = reg.get_display_field(
        "x",
    )

    assert field.description == "Original description"

    assert field.notes == "Original notes"

    assert field.defined_in == "overlay.py"


def test_display_field_registration_replaces_profile():
    """
    Profiles are treated as atomic display
    declarations.

    Re-registering a profile with the same
    name replaces the entire profile rather
    than merging profile attributes.
    """

    reg = DisplayRegistry()

    reg.register_display_field(
        DisplayField.field(
            "x",
            profiles={
                "table": DisplayProfile(
                    label="Original",
                    content_align="center",
                    label_align="center",
                ),
            },
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "x",
            profiles={
                "table": DisplayProfile(
                    width=25,
                ),
            },
        )
    )

    field = reg.get_display_field(
        "x",
    )

    profile = field.profiles["table"]

    assert profile.label is None

    assert profile.content_align == "left"

    assert profile.label_align == "left"

    assert profile.width == 25


def test_display_field_registration_preserves_other_profiles():
    """
    Profile dictionaries merge by profile name.

    Replacing one profile should not remove
    unrelated profiles already registered
    on the field.
    """

    reg = DisplayRegistry()

    reg.register_display_field(
        DisplayField.field(
            "x",
            profiles={
                "table": DisplayProfile(
                    label="Table",
                ),
                "pivot": DisplayProfile(
                    label="Pivot",
                ),
            },
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "x",
            profiles={
                "table": DisplayProfile(
                    width=25,
                ),
            },
        )
    )

    field = reg.get_display_field(
        "x",
    )

    assert set(field.profiles) == {
        "table",
        "pivot",
    }

    # table profile replaced
    assert field.profiles["table"].label is None

    assert field.profiles["table"].width == 25

    # pivot profile preserved
    assert field.profiles["pivot"].label == "Pivot"


def test_display_field_registration_can_clear_notes():
    """
    Explicitly supplying an empty notes
    string should clear previously
    registered notes.
    """

    reg = DisplayRegistry()

    reg.register_display_field(
        DisplayField.field(
            "x",
            notes="Original notes",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "x",
            notes="",
        )
    )

    field = reg.get_display_field(
        "x",
    )

    assert field.notes == ""


# =========================================================
# Repr
# =========================================================


def test_registry_repr():
    reg = DisplayRegistry()

    text = repr(reg)

    assert "DisplayRegistry" in text

    assert "fields=0" in text

    assert "groups=0" in text

    assert "views=0" in text
