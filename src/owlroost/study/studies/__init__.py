# src/owlroost/study/studies/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study package discovery.

Notes
-----
Discovers and registers all study
packages contained in this directory.

Each study is implemented as a Python
package exporting a ``register_studies()``
function.

The study package directory also serves
as the root for shared study resources,
including Markdown documents used when
constructing evidence packages.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from types import ModuleType

# =========================================================
# Package Resources
# =========================================================

RESOURCE_DIR = Path(__file__).parent

# =========================================================
# Discovery
# =========================================================


def _discover_modules() -> list[ModuleType]:
    """
    Discover study packages.
    """

    modules: list[ModuleType] = []

    for module_info in sorted(
        pkgutil.iter_modules(
            [str(RESOURCE_DIR)],
        ),
        key=lambda m: m.name,
    ):
        #
        # Ignore private modules/packages.
        #

        if module_info.name.startswith("_"):
            continue

        #
        # Only import packages.
        #

        if not module_info.ispkg:
            continue

        modules.append(
            importlib.import_module(
                f"{__name__}.{module_info.name}",
            )
        )

    return modules


# =========================================================
# Registration
# =========================================================


def register_all_studies(
    reg,
):
    """
    Register every discovered study.
    """

    for module in _discover_modules():
        register_fn = getattr(
            module,
            "register_studies",
            None,
        )

        if register_fn is None:
            continue

        register_fn(
            reg,
        )


__all__ = [
    "RESOURCE_DIR",
    "register_all_studies",
]
