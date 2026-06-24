# src/owlroost/catalog/context.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Catalog bootstrap context.

Notes
-----
Constructs the complete catalog
construction context used by:

    - CLI commands
    - notebooks
    - reports
    - dashboards
    - audit tools

The returned CatalogContext provides
named access to all registries and
catalog structures.

Returns
-------
CatalogContext
"""

from __future__ import annotations

from dataclasses import dataclass

from owlroost.catalog.loaders import (
    load_catalog_rows,
)
from owlroost.comparison.bootstrap import (
    build_comparison_registry,
)
from owlroost.display.bootstrap import (
    build_display_registry,
)
from owlroost.metrics.bootstrap import (
    build_metrics_registry,
)
from owlroost.schema.bootstrap import (
    build_schema_registry,
)
from owlroost.workspace.bootstrap import (
    build_workspace_registry,
)

# =========================================================
# Catalog Context
# =========================================================


@dataclass(
    slots=True,
)
class CatalogContext:
    """
    Fully initialized catalog bootstrap context.

    Notes
    -----
    Provides convenient access to all
    ontology registries, display overlays,
    and unified catalog structures.
    """

    schema_registry: object

    metrics_registry: object

    workspace_registry: object

    comparison_registry: object

    display_registry: object

    catalog_rows: list[dict]

    catalog_index: dict[str, dict]


# =========================================================
# Bootstrap
# =========================================================


def build_catalog_context() -> CatalogContext:
    """
    Build complete catalog context.

    Returns
    -------
    CatalogContext
    """

    # =====================================================
    # Canonical Ontology Registries
    # =====================================================

    schema_registry = build_schema_registry()

    metrics_registry = build_metrics_registry()

    workspace_registry = build_workspace_registry()

    comparison_registry = build_comparison_registry()

    # =====================================================
    # Display Overlay Registry
    # =====================================================

    display_registry = build_display_registry(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
        workspace_registry=workspace_registry,
        comparison_registry=comparison_registry,
    )

    # =====================================================
    # Unified Catalog
    # =====================================================

    catalog_rows = load_catalog_rows(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
        workspace_registry=workspace_registry,
        comparison_registry=comparison_registry,
        display_registry=display_registry,
    )

    catalog_index = {row["field_name"]: row for row in catalog_rows}

    # =====================================================
    # Context
    # =====================================================

    return CatalogContext(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
        workspace_registry=workspace_registry,
        comparison_registry=comparison_registry,
        display_registry=display_registry,
        catalog_rows=catalog_rows,
        catalog_index=catalog_index,
    )
