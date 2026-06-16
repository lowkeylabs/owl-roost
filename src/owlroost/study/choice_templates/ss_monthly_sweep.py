# src/owlroost/study/choice_templates/ss_monthly_sweep.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Social Security monthly sweep methodology.

Notes
-----
Evaluates Social Security claiming
ages at monthly granularity between
ages 62 and 70.

This methodology provides finer
resolution than the yearly sweep
and is intended for decision
refinement after a coarse annual
analysis.
"""

from __future__ import annotations

from owlroost.display.specs import (
    DisplayProfile,
)
from owlroost.study.specs import (
    ChoiceTemplateSpec,
)


def register_choice_templates(
    reg,
):
    reg.register_choice_template(
        ChoiceTemplateSpec(
            name="ss_monthly_sweep",
            decision_name="social_security",
            title="Monthly Sweep",
            description=("Evaluate monthly Social Security claiming ages between 62 and 70."),
            required_levers=[
                "has_ss_pia",
            ],
            overrides=[
                ("roost_sweeps.ss_age_pair=range(62,70,1/12)"),
            ],
            tags=[
                "retirement",
                "social-security",
                "sweep",
                "monthly",
                "refinement",
            ],
            profiles={
                "table": DisplayProfile(
                    label="Template\nSS Monthly",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label=("Choice Template - Social Security Monthly Sweep"),
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
            },
        )
    )
