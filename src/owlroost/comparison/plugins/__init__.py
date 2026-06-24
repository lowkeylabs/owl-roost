# src/owlroost/comparison/plugins/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Comparison plugin discovery.

Notes
-----
Comparison observations are distributed
across modules within this package.

Any module exporting:

    register_comparison_fields(reg)

will be automatically discovered and
executed during bootstrap.

Examples
--------
overrides.py
    Shared and run-specific override
    comparisons.

deltas.py
    Baseline-relative metric deltas.

statistics.py
    Comparative statistical measures.

similarity.py
    Comparison similarity metrics.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path


def register_comparison_fields(
    reg,
):
    """
    Register all comparison observations.
    """

    package_path = Path(
        __file__,
    ).parent

    for module_info in sorted(
        pkgutil.iter_modules(
            [str(package_path)],
        ),
        key=lambda m: m.name,
    ):
        if module_info.name.startswith(
            "_",
        ):
            continue

        module = importlib.import_module(
            f"{__name__}.{module_info.name}",
        )

        register_fn = getattr(
            module,
            "register_comparison_fields",
            None,
        )

        if register_fn is None:
            continue

        register_fn(
            reg,
        )
