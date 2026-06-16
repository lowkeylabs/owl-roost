# src/owlroost/study/levers/has_ss_pia.py
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
            name="has_ss_pia",
            title=("Has Social Security PIA"),
            description=("Case contains Social Security income."),
            applicable_fn=(has_social_security),
            profiles={
                "table": DisplayProfile(
                    label="Has\nPIA",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Lever - Has SS PIA",
                ),
            },
        )
    )
