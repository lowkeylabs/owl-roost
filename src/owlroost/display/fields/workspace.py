from __future__ import annotations

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import normalize_module_path
from owlroost.display.specs import (
    DisplayField,
    DisplayProfile,
)

# =========================================================
# Methodology Ontology
# =========================================================

SHARED_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="execution",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="primary",
    materialization_level="workspace",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)


def register_display_fields(
    reg,
):
    """
    Register  display fields.
    """

    reg.register_display_field(
        DisplayField.field(
            "workspace.name",
            path="workspace_name",
            profiles={
                "table": DisplayProfile(label="Workspace\nName", width="auto"),
                "pivot": DisplayProfile(label="Workspace Name", width="auto"),
            },
            **SHARED_ONTOLOGY,
            description="Folder name of workspace",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.title",
            path="workspace_title",
            profiles={
                "table": DisplayProfile(
                    label="Workspace\nTitle",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Workspace Title",
                    width="auto",
                ),
            },
            **SHARED_ONTOLOGY,
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.description",
            path="workspace_description",
            profiles={
                "table": DisplayProfile(
                    label="Workspace\nDescription",
                    width=50,
                    wrap=True,
                ),
                "pivot": DisplayProfile(
                    label="Workspace Description",
                    width="auto",
                ),
            },
            **SHARED_ONTOLOGY,
        )
    )
