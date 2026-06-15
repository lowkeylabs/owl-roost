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

The returned tuple exposes the
individual objects directly rather
than wrapping them in a runtime class.

Returns
-------
(
    schema_registry,
    metrics_registry,
    display_registry,
    catalog_rows,
    catalog_index,
)
"""

from __future__ import annotations

from owlroost.catalog.loaders import (
    load_catalog_rows,
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


def build_catalog_context():
    """
    Build complete catalog context.

    Returns
    -------
    tuple
        (
            schema_registry,
            metrics_registry,
            display_registry,
            catalog_rows,
            catalog_index,
        )
    """

    schema_registry = build_schema_registry()

    metrics_registry = build_metrics_registry()

    display_registry = build_display_registry(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
    )

    catalog_rows = load_catalog_rows(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
        display_registry=display_registry,
    )

    catalog_index = {row["field_name"]: row for row in catalog_rows}

    return (
        schema_registry,
        metrics_registry,
        display_registry,
        catalog_rows,
        catalog_index,
    )
