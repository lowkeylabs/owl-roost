# src/owlroost/display/views/row.py
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
            level="row",
            name="build",
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
            level="row",
            name="cases",
            entries=[
                # =====================================
                # Identity
                # =====================================
                # "case_name",
                # ("description", {"modes": ["pivot"]}),
                ("basic_info.names", {"modes": ["table", "pivot"]}),
                "display.starting_ages",
                "basic_info.life_expectancy",
                "balance_sheet.net_worth",
                "balance_sheet.total_assets",
                "balance_sheet.total_liabilities",
                "balance_sheet.has_hfp_file",
                # "rates_selection.method",
                # "rates_selection.values",
                # "display.compact_rates",
                # "display.optimization_goal",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="row",
            name="hfp",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "case_name",
                ("description", {"modes": ["pivot"]}),
                "household_financial_profile.HFP_file_name",
                "balance_sheet.has_hfp_file",
                "balance_sheet.fixed_assets_current_value",
                "balance_sheet.fixed_assets_debt_remaining_value",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="row",
            name="descriptions",
            entries=[
                # =====================================
                # Identity
                # =====================================
                "case_name",
                "description",
            ],
            description=(""),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="row",
            name="balance_sheet",
            entries=[
                # -------------------------------------------------
                # Summary
                # -------------------------------------------------
                ("case_name"),
                ("section", "Net Worth"),
                "balance_sheet.net_worth",
                ("section", "Assets and Liabilities"),
                "balance_sheet.total_assets",
                "balance_sheet.total_liabilities",
                # -------------------------------------------------
                # Asset Detail
                # -------------------------------------------------
                ("section", "Asset Details"),
                "balance_sheet.total_taxable_savings",
                "balance_sheet.total_tax_deferred_savings",
                "balance_sheet.total_tax_free_savings",
                "balance_sheet.fixed_assets_current_value",
                ("section", "Liability Detail"),
                "balance_sheet.fixed_assets_debt_remaining_value",
            ],
            description=(
                "Summarizes household financial position "
                "including retirement savings, fixed "
                "assets, liabilities, total assets, "
                "and net worth."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="row",
            name="planning_checkpoints",
            entries=[
                # -------------------------------------------------
                # Summary
                # -------------------------------------------------
                ("case_name"),
                ("section", "Planning Checkpoints"),
                "history.planning_checkpoint.as_of",
                "history.planning_checkpoint.hsa_savings_balances",
                "history.planning_checkpoint.prior_12_months_discretionary_spending",
                "history.planning_checkpoint.prior_12_months_essential_spending",
                "history.planning_checkpoint.tax_deferred_savings_balances",
                "history.planning_checkpoint.tax_free_savings_balances",
                "history.planning_checkpoint.taxable_savings_balances",
            ],
            description=(
                "Summarizes household financial position "
                "including retirement savings, fixed "
                "assets, liabilities, total assets, "
                "and net worth."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )

    reg.register_view(
        DisplayView(
            level="row",
            name="tax_payments",
            entries=[
                # -------------------------------------------------
                # Summary
                # -------------------------------------------------
                ("case_name"),
                ("section", "tax_payments"),
                "history.tax_payment.date",
                "history.tax_payment.tax_year",
                "history.tax_payment.tax_type",
                "history.tax_payment.agency",
                "history.tax_payment.payment_type",
                "history.tax_payment.amount",
            ],
            description=(
                "Summarizes household financial position "
                "including retirement savings, fixed "
                "assets, liabilities, total assets, "
                "and net worth."
            ),
            **SHARED_VIEW_ONTOLOGY,
        )
    )
