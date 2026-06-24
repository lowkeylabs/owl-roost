import pytest

from owlroost.comparison.bootstrap import (
    build_comparison_registry,
)


@pytest.fixture
def comparison_registry():
    return build_comparison_registry()
