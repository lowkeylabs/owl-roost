from __future__ import annotations

import pytest

from owlroost.catalog.service import (
    load_catalog,
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


@pytest.fixture
def registries():
    schema_registry = build_schema_registry()

    metrics_registry = build_metrics_registry()

    workspace_registry = build_workspace_registry()

    display_registry = build_display_registry(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
        workspace_registry=workspace_registry,
    )

    return (
        schema_registry,
        metrics_registry,
        workspace_registry,
        display_registry,
    )


@pytest.fixture
def catalog_rows(
    registries,
):
    (
        schema_registry,
        metrics_registry,
        workspace_registry,
        display_registry,
    ) = registries

    return load_catalog(
        schema_registry=schema_registry,
        metrics_registry=metrics_registry,
        workspace_registry=workspace_registry,
        display_registry=display_registry,
    )
