# src/owlroost/display/bootstrap.py
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

from owlroost.display.dashboards.bootstrap import (
    register_display_dashboards,
)
from owlroost.display.fields import (
    register_all_display_fields,
)
from owlroost.display.groups import (
    register_display_groups,
)
from owlroost.display.registry import (
    DisplayRegistry,
)
from owlroost.display.sync import (
    sync_comparison_registry,
    sync_metrics_registry,
    sync_schema_registry,
    sync_workspace_registry,
)
from owlroost.display.views import (
    register_display_views,
)

# =========================================================
# Bootstrap
# =========================================================


def build_display_registry(
    schema_registry,
    metrics_registry,
    workspace_registry,
    comparison_registry,
):
    """
    Construct fully initialized DisplayRegistry.

    Notes
    -----
    DisplayRegistry is renderer-facing overlay
    infrastructure layered atop canonical
    ontology registries.

    Canonical semantic ownership belongs to:

        - schema_registry
        - metrics_registry
        - workspace_registry
        - comparison_registry

    DisplayRegistry owns only presentation
    semantics:

        - labels
        - formatting
        - alignment
        - visibility
        - grouping
        - views
        - rendering overlays

    Initialization Order
    --------------------

    1. schema ontology overlays
    2. metrics ontology overlays
    3. workspace ontology overlays
    4. comparison ontology overlays
    5. explicit display field overlays
    6. display groups
    7. display views
    8. validation
    """

    reg = DisplayRegistry()

    # =====================================================
    # Canonical Ontology Registries
    # =====================================================

    reg.schema_registry = schema_registry

    reg.metrics_registry = metrics_registry

    reg.workspace_registry = workspace_registry

    reg.comparison_registry = comparison_registry

    # =====================================================
    # Schema Display Overlays
    # =====================================================

    sync_schema_registry(
        schema_registry=(schema_registry),
        display_registry=reg,
    )

    # =====================================================
    # Metrics Display Overlays
    # =====================================================

    sync_metrics_registry(
        metrics_registry=(metrics_registry),
        display_registry=reg,
    )

    # =====================================================
    # Workspace Display Overlays
    # =====================================================

    sync_workspace_registry(
        workspace_registry=workspace_registry,
        display_registry=reg,
    )

    # =====================================================
    # Comparison Display Overlays
    # =====================================================

    sync_comparison_registry(
        comparison_registry=comparison_registry,
        display_registry=reg,
    )

    # =====================================================
    # Explicit Manual Display Overlays
    # =====================================================

    register_all_display_fields(
        reg,
    )

    # =====================================================
    # Display Groups
    # =====================================================

    register_display_groups(
        reg,
    )

    # =====================================================
    # Display Views
    # =====================================================

    register_display_views(
        reg,
    )

    register_display_dashboards(
        reg,
    )

    # =====================================================
    # Validation
    # =====================================================

    reg.validate()

    return reg
