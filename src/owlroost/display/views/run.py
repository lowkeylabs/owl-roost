# src/owlroost/display/views/run.py
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
            name="run",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "case_name",
                ("description", {"modes": ["pivot"]}),
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
                ("case_name", {"modes": ["pivot"]}),
                "basic_info.names",
                "display.compact_id",
                "display.optimization_goal",
                "display.compact_rates",
                "display.completion_fraction",
                "financial.spending.year0.today__median",
                "financial.spending.total.today__median",
                "financial.bequest.total.today__median",
                ("description", {"modes": ["pivot"]}),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="social_security",
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
                "social_security.optimized__constant",
                ("social_security.ages__median"),
                (
                    "financial.spending.total.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                "financial.bequest.total.today__median",
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
                # "display.optimization_goal",
                # "rates_selection.method",
                "display.completion_fraction",
                "fixed_income.social_security_ages",
                # "solver_options.withSSAges",
                # "social_security.optimized__constant",
                # ("social_security.ages__median"),
                (
                    "financial.spending.total.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.spending.total.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.spending.total.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.bequest.total.today__p10",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.bequest.total.today__median",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
                (
                    "financial.bequest.total.today__p90",
                    {"profiles": {"table": {"fmt": "currency"}}},
                ),
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="timing",
            entries=[
                "case_name",
                "display.compact_id",
                # -----------------------------------------
                # Execution configuration
                # -----------------------------------------
                "solver_options.solver",
                "roost_settings.workers_per_run",
                "display.compact_threads",
                # -----------------------------------------
                # Completion
                # -----------------------------------------
                "display.completion_fraction",
                # -----------------------------------------
                # Run wall-clock timing
                # -----------------------------------------
                # "run_timing.elapsed_seconds",
                # -----------------------------------------
                # Trial timing aggregates
                # -----------------------------------------
                "timing.elapsed_seconds__median",
                "timing.elapsed_seconds__mean",
                "timing.elapsed_seconds__p90",
                "timing.elapsed_seconds__max",
                # -----------------------------------------
                # Derived execution metrics
                # -----------------------------------------
                "run_execution.trials_per_second",
                "run_execution.concurrency_equivalent",
                "run_execution.worker_utilization",
                # -----------------------------------------
                # Derived timing diagnostics
                # -----------------------------------------
                "run_timing.trial_latency_skew",
            ],
            description=("Run-level execution, throughput, and timing diagnostics."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="working_set_overrides",
            entries=[
                "case_name",
                "display.compact_id",
                "display.completion_fraction",
                "comparison.working_set.common_overrides",
                "comparison.working_set.run_specific_overrides",
            ],
            description=("Run-level specific and common overrides, forming an execution plan."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="run",
            name="session_overrides",
            entries=[
                "case_name",
                "display.compact_id",
                "display.completion_fraction",
                "comparison.session.common_overrides",
                "comparison.session.run_specific_overrides",
            ],
            description=("Run-level specific and common overrides, forming an execution plan."),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
