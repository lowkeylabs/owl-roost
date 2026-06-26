from __future__ import annotations

from owlroost.display.materializers.materialize import (
    expand_entries,
)


def test_all_view_fields_exist(
    catalog,
):
    """
    Every field referenced by every view
    must have a registered DisplayField.
    """

    for view in catalog.display_registry.all_views():
        entries = expand_entries(
            catalog.display_registry,
            view.entries,
        )

        for entry in entries:
            if entry.get("kind") == "section":
                continue

            catalog.display_registry.get_display_field(
                entry["field"],
            )
