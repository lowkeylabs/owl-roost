# src/owlroost/study/bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study subsystem bootstrap.

Notes
-----
Constructs and populates the study
definition registry.

Architectural Invariant
-----------------------

The bootstrap process registers all
definition-layer study entities:

    • Studies

    • Experiments

The registry is fully populated before
being returned.

Registration order follows the
conceptual hierarchy:

    Study
        ↓
    Experiment

Execution artifacts (Sessions, Runs,
and Trials) are materialized elsewhere.
"""

from __future__ import annotations

from owlroost.study.experiments import (
    register_all_experiments,
)
from owlroost.study.registry import (
    StudyRegistry,
)
from owlroost.study.studies import (
    register_all_studies,
)

# =========================================================
# Bootstrap
# =========================================================


def build_study_registry() -> StudyRegistry:
    """
    Construct and populate the
    study registry.
    """

    registry = StudyRegistry()

    # -----------------------------------------------------
    # Studies
    # -----------------------------------------------------

    register_all_studies(
        registry,
    )

    # -----------------------------------------------------
    # Experiments
    # -----------------------------------------------------

    register_all_experiments(
        registry,
    )

    return registry
