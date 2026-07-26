# src/owlroost/display/views/results.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from owlroost.core.utils import normalize_module_path
from owlroost.display.specs import (
    DisplayView,
)

SHARED_VIEW_ONTOLOGY = dict(
    defined_in=normalize_module_path(__file__),
)


def register_display_views(
    reg,
):
    """
    Register all display views.

    Views are declarative layouts composed
    from reusable display groups and fields.

    Views are uniquely identified by:

        (level, name)

    Examples:

        ("case", "basic")
        ("run", "results")
        ("session", "results")
    """

    reg.register_view(
        DisplayView(
            level="run",
            name="results",
            entries=[
                # =====================================
                # Identity
                # =====================================
                ("case_name", {"modes": ["pivot"]}),
                #                "basic_info.names",
                "display.compact_id",
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                "financial.spending.year0.today__median",
                "financial.spending.year5.today__median",
                "financial.spending.total.today__median",
                "financial.taxes.total.today__median",
                "financial.bequest.terminal.today__median",
                ("description", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="results2",
            entries=[
                # =====================================
                # Identity
                # =====================================
                ("case_name", {"modes": ["pivot"]}),
                # "basic_info.names",
                "display.compact_id",
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                ("section", "First year spending (todays dollars)"),
                "financial.spending.year0.today__p10",
                "financial.spending.year0.today__median",
                "financial.spending.year0.today__p90",
                ("section", "Spending through year 5 (todays dollars)"),
                "financial.spending.year5.today__p10",
                "financial.spending.year5.today__median",
                "financial.spending.year5.today__p90",
                ("section", "Spending through year 10 (todays dollars)"),
                "financial.spending.year10.today__p10",
                "financial.spending.year10.today__median",
                "financial.spending.year10.today__p90",
                ("section", "Lifetime spending (todays dollars)"),
                "financial.spending.total.today__p10",
                "financial.spending.total.today__median",
                "financial.spending.total.today__p90",
                ("section", "Lifetime taxes (todays dollars)"),
                "financial.taxes.total.today__p10",
                "financial.taxes.total.today__median",
                "financial.taxes.total.today__p90",
                ("section", "Bequest (todays dollars, tax adjusted)"),
                "financial.bequest.terminal.today__p10",
                "financial.bequest.terminal.today__median",
                "financial.bequest.terminal.today__p90",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
