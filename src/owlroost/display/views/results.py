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
            name="table_of_runs",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "display.compact_id",
                "case_name",
                "roost_settings.study_name",
                "roost_settings.experiment_name",
                "roost_settings.orphan_overrides",
                ("display.optimization_goal", {"modes": ["pivot"]}),
                ("display.compact_rates", {"modes": ["pivot"]}),
                ("display.completion_fraction", {"modes": ["pivot"]}),
                # ("description", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="table_of_rate_models",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "display.compact_id",
                "display.compact_rates",
                "rates_selection.method",
                "rates_selection.from",
                "rates_selection.to",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="results",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "display.compact_id",
                ("case_name", {"modes": ["pivot"]}),
                ("roost_settings.study_name", {"modes": ["pivot"]}),
                ("roost_settings.experiment_name", {"modes": ["pivot"]}),
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                ("section", "First year spending (todays dollars)"),
                ("financial.spending.year0.today__p10", {"modes": ["pivot"]}),
                "financial.spending.year0.today__median",
                ("financial.spending.year0.today__p90", {"modes": ["pivot"]}),
                ("section", "Spending through year 5 (todays dollars)"),
                ("financial.spending.year5.today__p10", {"modes": ["pivot"]}),
                "financial.spending.year5.today__median",
                ("financial.spending.year5.today__p90", {"modes": ["pivot"]}),
                ("section", "Spending through year 10 (todays dollars)"),
                ("financial.spending.year10.today__p10", {"modes": ["pivot"]}),
                "financial.spending.year10.today__median",
                ("financial.spending.year10.today__p90", {"modes": ["pivot"]}),
                ("section", "Lifetime spending (todays dollars)"),
                ("financial.spending.total.today__p10", {"modes": ["pivot"]}),
                "financial.spending.total.today__median",
                ("financial.spending.total.today__p90", {"modes": ["pivot"]}),
                ("section", "Lifetime taxes (todays dollars)"),
                ("financial.taxes.total.today__p10", {"modes": ["pivot"]}),
                "financial.taxes.total.today__median",
                ("financial.taxes.total.today__p90", {"modes": ["pivot"]}),
                ("section", "Bequest (todays dollars, tax adjusted)"),
                ("financial.bequest.terminal.today__p10", {"modes": ["pivot"]}),
                "financial.bequest.terminal.today__median",
                ("financial.bequest.terminal.today__p90", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
    reg.register_view(
        DisplayView(
            level="run",
            name="spending",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "display.compact_id",
                ("case_name", {"modes": ["pivot"]}),
                ("roost_settings.study_name", {"modes": ["pivot"]}),
                ("roost_settings.experiment_name", {"modes": ["pivot"]}),
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                ("section", "First year spending (todays dollars)"),
                ("financial.spending.year0.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.spending.year0.today__p10", {"modes": ["table", "pivot"]}),
                "financial.spending.year0.today__median",
                ("section", "Spending through year 5 (todays dollars)"),
                ("financial.spending.year5.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.spending.year5.today__p10", {"modes": ["table", "pivot"]}),
                "financial.spending.year5.today__median",
                ("section", "Spending through year 10 (todays dollars)"),
                ("financial.spending.year10.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.spending.year10.today__p10", {"modes": ["table", "pivot"]}),
                "financial.spending.year10.today__median",
                ("section", "Lifetime spending (todays dollars)"),
                ("financial.spending.total.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.spending.total.today__p10", {"modes": ["table", "pivot"]}),
                "financial.spending.total.today__median",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="taxes",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "display.compact_id",
                ("case_name", {"modes": ["pivot"]}),
                ("roost_settings.study_name", {"modes": ["pivot"]}),
                ("roost_settings.experiment_name", {"modes": ["pivot"]}),
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                ("section", "First year taxes (todays dollars)"),
                ("financial.taxes.year0.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.taxes.year0.today__p10", {"modes": ["table", "pivot"]}),
                "financial.taxes.year0.today__median",
                ("section", "Cumulative taxes through year 5 (todays dollars)"),
                ("financial.taxes.year5.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.taxes.year5.today__p10", {"modes": ["table", "pivot"]}),
                "financial.taxes.year5.today__median",
                ("section", "Cumulative taxes through year 10 (todays dollars)"),
                ("financial.taxes.year10.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.taxes.year10.today__p10", {"modes": ["table", "pivot"]}),
                "financial.taxes.year10.today__median",
                ("section", "Lifetime taxes (todays dollars)"),
                ("financial.taxes.total.today__p05", {"modes": ["table", "pivot"]}),
                ("financial.taxes.total.today__p10", {"modes": ["table", "pivot"]}),
                "financial.taxes.total.today__median",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
