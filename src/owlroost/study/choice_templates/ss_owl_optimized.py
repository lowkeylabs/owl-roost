# src/owlroost/study/choice_templates/ss_owl_optimized.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Social Security OWL optimization methodology.

Notes
-----
Uses OWL's internal optimization
capabilities to identify candidate
Social Security claiming ages.

Unlike sweep-based methodologies,
this approach delegates search of
the decision space to OWL rather
than exhaustively evaluating a
predefined grid of ages.
"""

from __future__ import annotations

from owlroost.display.specs import (
    DisplayProfile,
)
from owlroost.study.specs import (
    ChoiceTemplateSpec,
)


def register_choice_templates(reg):
    reg.register_choice_template(
        ChoiceTemplateSpec(
            name="ss_owl_optimizer",
            scenario_family_name=("social_security_claiming"),
            title="OWL Optimizer",
            description=("Use OWL optimization to identify Social Security claiming ages."),
            required_levers=[
                "has_ss_pia",
            ],
            overrides=[
                ("fixed_income.social_security_optimization=true"),
            ],
            tags=[
                "retirement",
                "social-security",
                "optimization",
                "owl",
            ],
            profiles={
                "table": DisplayProfile(
                    label="Template\nSS OWL",
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label=("Choice Template - Social Security OWL Optimizer"),
                    width="auto",
                    label_align="center",
                    content_align="center",
                ),
            },
        )
    )
