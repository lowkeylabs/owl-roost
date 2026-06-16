# src/owlroost/study/choice_templates/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
lever discover and loading
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from types import ModuleType

# =========================================================
# Discovery
# =========================================================


def _discover_choice_template_modules() -> list[ModuleType]:
    """
    discover choice template modules
    """

    modules: list[ModuleType] = []

    package_path = Path(__file__).parent

    for module_info in sorted(
        pkgutil.iter_modules([str(package_path)]),
        key=lambda m: m.name,
    ):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(f"{__name__}.{module_info.name}")

        modules.append(module)

    return modules


# =========================================================
# Registration
# =========================================================


def register_all_choice_templates(
    reg,
):
    """ """

    for module in _discover_choice_template_modules():
        register_fn = getattr(
            module,
            "register_choice_templates",
            None,
        )

        if register_fn is None:
            continue

        register_fn(reg)


__all__ = [
    "register_all_choice_templates",
]
