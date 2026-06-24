from __future__ import annotations

import pytest

from owlroost.catalog.context import (
    build_catalog_context,
)


@pytest.fixture
def catalog():
    """
    Fully initialized catalog context.
    """

    return build_catalog_context()


@pytest.fixture
def catalog_rows(
    catalog,
):
    """
    Unified catalog rows.
    """

    return catalog.catalog_rows
