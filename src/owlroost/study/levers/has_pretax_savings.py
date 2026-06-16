# src/owlroost/study/levers/has_pretax_savings.py
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

from owlroost.display.specs import DisplayProfile
from owlroost.study.specs import (
    LeverSpec,
)


def has_pre_tax_assets(
    row,
):
    savings = row.get("_inputs", {}).get("savings_assets", {})
    pretax = savings.get("tax_deferred_savings_balances", [])
    return sum(pretax) > 0


def has_social_security(
    row,
):
    inputs = row.get("_inputs", {}).get("fixed_income", {})
    pias = inputs.get("social_security_pia_amounts", {})
    return any(pia > 0 for pia in pias)


def register_levers(
    reg,
):
    reg.register_lever(
        LeverSpec(
            name="has_pretax_savings",
            title=("Lever - has pre-tax savings"),
            description=("Case contains tax deferred assets."),
            decision_names=[
                "roth_conversion",
            ],
            profiles={
                "table": DisplayProfile(
                    label="Has\nPretax\nSavings",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Lever - has pre-taxable savings",
                ),
            },
            applicable_fn=(has_pre_tax_assets),
        )
    )
