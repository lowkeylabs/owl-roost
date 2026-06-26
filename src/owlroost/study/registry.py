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
* Questions
* Scenario Families
* Experiments

Architectural Invariant
-----------------------

Relationships flow downward only:

    Study
        ↓
    Question
        ↓
    Scenario Family
        ↓
    Experiment

Relationships are stored only once.

StudySpec owns:

    question_names

QuestionSpec owns:

    scenario_family_names

ScenarioFamilySpec owns:

    experiment_names

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
    def __init__(
        self,
    ):
        self._studies = {}

        self._questions = {}

        self._scenario_families = {}

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
            key=lambda x: x.name,
        )

    # =====================================================
    # Questions
    # =====================================================

    def register_question(
        self,
        spec,
    ):
        self._questions[spec.name] = spec

    def get_question(
        self,
        name,
    ):
        try:
            return self._questions[name]

        except KeyError as exc:
            raise RoostError(f"Question not found: {name}") from exc

    def all_questions(
        self,
    ):
        return sorted(
            self._questions.values(),
            key=lambda x: x.name,
        )

    # =====================================================
    # Scenario Families
    # =====================================================

    def register_scenario_family(
        self,
        spec,
    ):
        self._scenario_families[spec.name] = spec

    def get_scenario_family(
        self,
        name,
    ):
        try:
            return self._scenario_families[name]

        except KeyError as exc:
            raise RoostError(f"Scenario family not found: {name}") from exc

    def all_scenario_families(
        self,
    ):
        return sorted(
            self._scenario_families.values(),
            key=lambda x: x.name,
        )

    # =====================================================
    # Experiment Templates
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
            key=lambda x: x.name,
        )

    # =====================================================
    # Relationships
    # =====================================================

    def questions_for_study(
        self,
        study_name,
    ):
        study = self.get_study(
            study_name,
        )

        return [
            self.get_question(
                question_name,
            )
            for question_name in study.question_names
        ]

    def scenario_families_for_question(
        self,
        question_name,
    ):
        question = self.get_question(
            question_name,
        )

        return [
            self.get_scenario_family(
                scenario_family_name,
            )
            for scenario_family_name in question.scenario_family_names
        ]

    def experiments_for_scenario_family(
        self,
        scenario_family_name,
    ):
        scenario_family = self.get_scenario_family(
            scenario_family_name,
        )

        return [
            self.get_experiment(
                template_name,
            )
            for template_name in scenario_family.experiment_names
        ]
