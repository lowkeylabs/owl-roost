# src/owlroost/schema/sweeps/named_window.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
rates_selection.regime sweep variable.
"""

from __future__ import annotations

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import normalize_module_path

from ..registry import (
    FieldSpec,
)

# These are ordered by most stressful to least stressful on a retirement plan
# from sequence of returns perspective.

MARKET_REGIMES = {
    # Great for stress testing
    "lost_decade": (
        2000,
        2015,
    ),  # "slow-grind" - Two major bear markets with a slow recovery; emphasizes sequence-of-returns risk.
    "stagflation": (
        1966,
        1982,
    ),  # "double-shock" - High inflation, weak real returns, and difficult stock/bond conditions.
    "dotcom": (
        1994,
        2008,
    ),  # "bubble burst" - Technology boom followed by the dot-com crash and Global Financial Crisis.
    # Good for baseline evaluation
    "modern": (
        1990,
        2025,
    ),  # Contemporary market era spanning dot-com, GFC, COVID, and post-pandemic inflation.
    "full": (
        1928,
        2025,
    ),  # Entire available market history; long-run baseline across all economic environments.
    # Totally optimistic
    "secular_bull": (
        1982,
        1999,
    ),  # Extended bull market with declining interest rates and exceptional equity growth.
}


def register_schema_fields(
    reg,
):
    reg.register(
        FieldSpec(
            name="roost_sweeps.named_window",
            dtype=str,
            path=(
                "roost_sweeps",
                "named_window",
            ),
            source="sweep",
            owner="ROOST",
            semantic_domain="design",
            value_origin="user-specified",
            projection_kind="synthetic",
            analytic_kind="primary",
            materialization_level="run",
            node_type=CatalogNodeType.VARIABLE,
            materializes_to=[
                "rates_selection.from",
                "rates_selection.to",
            ],
            description=("Named historical market time window."),
            defined_in=normalize_module_path(__file__),
        )
    )


def materialize_override_to_canonical(
    run_dict,
):
    roost = run_dict.setdefault(
        "roost_sweeps",
        {},
    )

    regime = roost.pop(
        "named_window",
        None,
    )

    rates = run_dict.setdefault(
        "rates_selection",
        {},
    )

    if not regime:
        return

    if regime not in MARKET_REGIMES:
        raise ValueError(f"Unknown regime: {regime}")

    start, end = MARKET_REGIMES[regime]

    rates["from"] = start
    rates["to"] = end
