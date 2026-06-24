# src/owlroost/comparison/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Comparison bootstrap.

Notes
-----
Constructs the canonical ComparisonRegistry.

Comparison observations define
comparative analysis fields that are
materialized into:

    row["_comparison"]

Examples
--------

    comparison.session.common_overrides

    comparison.session.run_specific_overrides

    comparison.working_set.common_overrides

    comparison.working_set.run_specific_overrides

Architectural Invariant
-----------------------
Comparison field definitions are owned
by comparison plugins.

Bootstrap is responsible only for:

    - registry construction
    - plugin discovery
    - plugin registration
"""

from __future__ import annotations

from owlroost.comparison.plugins import (
    register_comparison_fields,
)
from owlroost.comparison.registry import (
    ComparisonRegistry,
)


def build_comparison_registry():
    """
    Construct ComparisonRegistry.
    """

    reg = ComparisonRegistry()

    register_comparison_fields(
        reg,
    )

    return reg
