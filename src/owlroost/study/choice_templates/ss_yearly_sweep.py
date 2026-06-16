# src/owlroost/study/choice_templates/ss_yearly_sweep.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Social Security yearly sweep methodology.

Notes
-----
Evaluates annual Social Security
claiming ages between 62 and 70.

This methodology is intended as a
simple educational and exploratory
starting point for Social Security
timing analysis.
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
            name="ss_yearly_sweep",
            decision_name="social_security",
            title="Yearly Sweep",
            description=("Evaluate annual Social Security claiming ages between 62 and 70."),
            required_levers=[
                "has_ss_pia",
            ],
            overrides=[
                ("roost_sweeps.ss_age_pair=62,63,64,65,66,67,68,69,70"),
            ],
            tags=[
                "retirement",
                "social-security",
                "sweep",
                "education",
            ],
            profiles={
                "table": DisplayProfile(
                    label="Template\nSS Yearly",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label=("Choice Template - Social Security Yearly Sweep"),
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
            },
        )
    )
