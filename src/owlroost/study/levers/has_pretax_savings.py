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


def has_pretax_savings(
    row,
):
    savings = row.get("_inputs", {}).get("savings_assets", {})
    pretax = savings.get("tax_deferred_savings_balances", [])
    return sum(pretax) > 0


def register_levers(
    reg,
):
    reg.register_lever(
        LeverSpec(
            name="has_pretax_savings",
            title=("Lever - has pre-tax savings"),
            description=("Case contains tax deferred assets."),
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
            applicable_fn=(has_pretax_savings),
        )
    )
