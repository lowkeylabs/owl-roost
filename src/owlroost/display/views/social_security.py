# src/owlroost/display/views/social_security.py
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
            name="social_security1",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "case_name",
                "display.compact_id",
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                # "fixed_income.social_security_ages",
                # "solver_options.withSSAges",
                "solver_options.maxRothConversion",
                "social_security.optimized__constant",
                ("social_security.ages__median"),
                (
                    "financial.spending.year0.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.roth.annual.year0.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.taxes.year0.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.spending.total.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.roth.cumulative.terminal.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.taxes.total.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.bequest.terminal.today__median",
                    {
                        "profiles": {
                            "table": {
                                "fmt": "currency",
                            }
                        }
                    },
                ),
                ("description", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="social_security2",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "case_name",
                "display.compact_id",
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                # "fixed_income.social_security_ages",
                # "solver_options.withSSAges",
                "solver_options.maxRothConversion",
                "social_security.optimized__constant",
                ("social_security.ages__median"),
                (
                    "financial.spending.year0.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.roth.annual.year0.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.taxes.year0.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.spending.total.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.roth.cumulative.terminal.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.taxes.total.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.bequest.terminal.today__p10",
                    {
                        "profiles": {
                            "table": {
                                "fmt": "currency",
                            }
                        }
                    },
                ),
                ("description", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
    reg.register_view(
        DisplayView(
            level="run",
            name="social_security3",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "case_name",
                "display.compact_id",
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                # "fixed_income.social_security_ages",
                # "solver_options.withSSAges",
                "solver_options.maxRothConversion",
                "social_security.optimized__constant",
                ("social_security.ages__median"),
                (
                    "financial.spending.year0.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.roth.annual.year0.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.taxes.year0.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.spending.total.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.roth.cumulative.terminal.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.taxes.total.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.bequest.terminal.today__p90",
                    {
                        "profiles": {
                            "table": {
                                "fmt": "currency",
                            }
                        }
                    },
                ),
                ("description", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
