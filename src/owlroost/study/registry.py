# src/owlroost/study/registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study registry.

Notes
-----
Owns registration and relationship
resolution for:

    * Studies
    * Experiments

Architectural Invariant
-----------------------

Relationships flow downward only:

    Study
        ↓
    Experiment

Relationships are stored only once.

StudySpec owns:

    experiments

Experiments are reusable
experimental designs.

Applicability is evaluated by
workspace materializers rather
than by the registry.
"""

from __future__ import annotations

from owlroost.exceptions import (
    RoostError,
)


class StudyRegistry:
    """
    Registry of analytical study
    definitions.

    The registry owns definition-layer
    entities only.

    Execution artifacts (Sessions,
    Runs, Trials) are materialized
    elsewhere.
    """

    def __init__(
        self,
    ):
        self._studies = {}

        self._experiments = {}

    # =====================================================
    # Studies
    # =====================================================

    def register_study(
        self,
        spec,
    ):
        self._studies[spec.name] = spec

    def get_study(
        self,
        name,
    ):
        try:
            return self._studies[name]

        except KeyError as exc:
            raise RoostError(f"Study not found: {name}") from exc

    def all_studies(
        self,
    ):
        return sorted(
            self._studies.values(),
            key=lambda study: study.name,
        )

    # =====================================================
    # Experiments
    # =====================================================

    def register_experiment(
        self,
        spec,
    ):
        self._experiments[spec.name] = spec

    def get_experiment(
        self,
        name,
    ):
        try:
            return self._experiments[name]

        except KeyError as exc:
            raise RoostError(f"Experiment not found: {name}") from exc

    def all_experiments(
        self,
    ):
        return sorted(
            self._experiments.values(),
            key=lambda experiment: experiment.name,
        )

    # =====================================================
    # Relationships
    # =====================================================

    def experiments_for_study(
        self,
        study_name,
    ):
        """
        Return the experiments belonging
        to a study.
        """

        study = self.get_study(
            study_name,
        )

        return [
            self.get_experiment(
                experiment_name,
            )
            for experiment_name in study.experiment_names
        ]
