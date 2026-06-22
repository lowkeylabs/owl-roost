# src/owlroost/display/fields/workspace.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from pathlib import Path

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
            description="Short workspace name from study.toml",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.path",
            path="workspace_path",
            profiles={
                "table": DisplayProfile(label="Workspace\nPath", width="auto"),
                "pivot": DisplayProfile(label="Workspace path", width="auto"),
            },
            **SHARED_ONTOLOGY,
            description="Full pathstr for workspace",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.folder",
            display_fn=lambda row: str(Path(row.get("workspace_path", Path.cwd())).name),
            profiles={
                "table": DisplayProfile(label="Workspace\nFolder", width="auto"),
                "pivot": DisplayProfile(label="Workspace folder", width="auto"),
            },
            **SHARED_ONTOLOGY,
            description="Full pathstr for workspace",
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
            description="Workspace title from study.toml",
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
            description="Workspace description from study.toml",
        )
    )

    # ------
    # Counts
    # ------

    reg.register_display_field(
        DisplayField.field(
            "workspace.trial_cnt",
            path="workspace.summary.trial_cnt",
            profiles={
                "table": DisplayProfile(
                    label="Trial\nCnt",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Trial Count",
                    width="auto",
                ),
            },
            **SHARED_ONTOLOGY,
            description="Workspace trial count",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.run_cnt",
            path="workspace.summary.run_cnt",
            profiles={
                "table": DisplayProfile(
                    label="Run\nCnt",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Run Count",
                    width="auto",
                ),
            },
            **SHARED_ONTOLOGY,
            description="Workspace run count",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.session_cnt",
            path="workspace.summary.session_cnt",
            profiles={
                "table": DisplayProfile(
                    label="Session\nCnt",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Session Count",
                    width="auto",
                ),
            },
            **SHARED_ONTOLOGY,
            description="Workspace session count",
        )
    )

    reg.register_display_field(
        DisplayField.field(
            "workspace.case_cnt",
            path="workspace.summary.case_cnt",
            profiles={
                "table": DisplayProfile(
                    label="Case\nCnt",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Case Count",
                    width="auto",
                ),
            },
            **SHARED_ONTOLOGY,
            description="Workspace case count",
        )
    )
