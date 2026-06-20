from __future__ import annotations

from owlroost.core.utils import normalize_module_path
from owlroost.display.specs import (
    DisplayView,
)

SHARED_VIEW_ONTOLOGY = dict(
    defined_in=normalize_module_path(__file__),
)


def register_display_views(
    reg,
):
    """
    Register catalog inspection views.
    """

    reg.register_view(
        DisplayView(
            level="workspace",
            name="workspace",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "workspace.name",
                "workspace.title",
                "workspace.description",
            ],
            description=("workspace description"),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
