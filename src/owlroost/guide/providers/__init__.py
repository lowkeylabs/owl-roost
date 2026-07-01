# src/owlroost/guide/providers/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Guide provider discovery.

Automatically imports every provider module
within this package.

Each provider should implement:

    register(reg)

No manual updates are required when new
providers are added.
"""

from __future__ import annotations

import importlib
import pkgutil


def iter_providers():
    """
    Yield every provider module.
    """

    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue

        yield importlib.import_module(f"{__name__}.{module_info.name}")


__all__ = [
    "iter_providers",
]
