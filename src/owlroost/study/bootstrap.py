# src/owlroost/study/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study subsystem bootstrap.

Notes
-----
Owns construction of the study
registry and registration of all
study subsystem components.

Architectural Invariant
-----------------------

The bootstrap process registers
all definition-layer entities:

    Studies
    Questions
    Scenario Families
    Choice Templates
    Levers

The registry is fully populated
before it is returned.

Registration order follows the
conceptual hierarchy but should
not affect correctness.
"""

from __future__ import annotations

from owlroost.study.choice_templates import (
    register_all_choice_templates,
)
from owlroost.study.questions import (
    register_all_questions,
)
from owlroost.study.registry import (
    StudyRegistry,
)
from owlroost.study.scenario_families import (
    register_all_scenario_families,
)
from owlroost.study.studies import (
    register_all_studies,
)


def build_study_registry():
    """
    Construct and populate a
    StudyRegistry instance.
    """

    reg = StudyRegistry()

    register_all_studies(
        reg,
    )

    register_all_questions(
        reg,
    )

    register_all_scenario_families(
        reg,
    )

    register_all_choice_templates(
        reg,
    )

    return reg
