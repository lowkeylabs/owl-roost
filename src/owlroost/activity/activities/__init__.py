# src/owlroost/activity/activities/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning activity discovery.

Automatically imports every activity
module within this package.

Each module should implement:

    register(reg)

No manual updates are required when
new activity modules are added.
"""

from __future__ import annotations

import importlib
import pkgutil


def iter_activities():
    """
    Yield every planning activity
    module.
    """

    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue

        yield importlib.import_module(f"{__name__}.{module_info.name}")


__all__ = [
    "iter_activities",
]
