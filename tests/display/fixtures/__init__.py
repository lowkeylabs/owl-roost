# tests/display/fixtures/__init__.py

from .example_views import (
    register_display_views as register_e_views,
)
from .testing_views import (
    register_display_views as register_t_views,
)


def register_testing_views(reg):
    register_t_views(reg)
    register_e_views(reg)


__all__ = [
    "register_testing_views",
]
