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
* Scenario families
* Choice templates
* Levers

Architectural Invariant
-----------------------

Relationships flow downward only:

    Study
        ↓
    Question
        ↓
    Scenario Family
        ↓
    Choice Template
        ↓
    Lever

    Relationships are stored only once.

StudySpec owns question_names.

QuestionSpec owns scenario_family_names.

Scenario families define evidence spaces.

ChoiceTemplateSpec owns scenario_family_name.

Levers determine applicability.

Reverse relationships are derived by the registry.

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

        self._choice_templates = {}

        self._levers = {}

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
    # Choice Templates
    # =====================================================

    def register_choice_template(
        self,
        spec,
    ):
        self._choice_templates[spec.name] = spec

    def get_choice_template(
        self,
        name,
    ):
        try:
            return self._choice_templates[name]

        except KeyError as exc:
            raise RoostError(f"Choice template not found: {name}") from exc

    def all_choice_templates(
        self,
    ):
        return sorted(
            self._choice_templates.values(),
            key=lambda x: x.name,
        )

    # =====================================================
    # Levers
    # =====================================================

    def register_lever(
        self,
        spec,
    ):
        self._levers[spec.name] = spec

    def get_lever(
        self,
        name,
    ):
        try:
            return self._levers[name]

        except KeyError as exc:
            raise RoostError(f"Lever not found: {name}") from exc

    def all_levers(
        self,
    ):
        return sorted(
            self._levers.values(),
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

    def choice_templates_for_scenario_family(
        self,
        scenario_family_name,
    ):
        return [
            template
            for template in self.all_choice_templates()
            if (template.scenario_family_name == scenario_family_name)
        ]

    def levers_for_choice_template(
        self,
        template_name,
    ):
        template = self.get_choice_template(
            template_name,
        )

        return [
            self.get_lever(
                lever_name,
            )
            for lever_name in template.required_levers
        ]

    # =====================================================
    # Applicability
    # =====================================================

    def applicable_levers(
        self,
        case_row,
    ):
        return [
            lever
            for lever in self.all_levers()
            if lever.applicable_fn(
                case_row,
            )
        ]

    def lever_is_applicable(
        self,
        lever_name,
        case_row,
    ):
        return self.get_lever(
            lever_name,
        ).applicable_fn(
            case_row,
        )

    def choice_template_is_applicable(
        self,
        template_name,
        case_row,
    ):
        template = self.get_choice_template(
            template_name,
        )

        return all(
            self.lever_is_applicable(
                lever_name,
                case_row,
            )
            for lever_name in template.required_levers
        )

    def scenario_family_is_applicable(
        self,
        scenario_family_name,
        case_row,
    ):
        scenario_family = self.get_scenario_family(
            scenario_family_name,
        )

        return all(
            self.lever_is_applicable(
                lever_name,
                case_row,
            )
            for lever_name in scenario_family.required_levers
        )

    def question_is_applicable(
        self,
        question_name,
        case_row,
    ):
        question = self.get_question(
            question_name,
        )

        if not all(
            self.lever_is_applicable(
                lever_name,
                case_row,
            )
            for lever_name in question.required_levers
        ):
            return False

        return all(
            self.scenario_family_is_applicable(
                scenario_family_name,
                case_row,
            )
            for scenario_family_name in question.scenario_family_names
        )

    def applicable_questions(
        self,
        case_row,
    ):
        return [
            question
            for question in self.all_questions()
            if self.question_is_applicable(
                question.name,
                case_row,
            )
        ]

    # =====================================================
    # Missing Levers
    # =====================================================

    def missing_levers_for_question(
        self,
        question_name,
        case_row,
    ):
        question = self.get_question(
            question_name,
        )

        missing = set()

        for lever_name in question.required_levers:
            if not self.lever_is_applicable(
                lever_name,
                case_row,
            ):
                missing.add(
                    lever_name,
                )

        for scenario_family_name in question.scenario_family_names:
            scenario_family = self.get_scenario_family(
                scenario_family_name,
            )

            for lever_name in scenario_family.required_levers:
                if not self.lever_is_applicable(
                    lever_name,
                    case_row,
                ):
                    missing.add(
                        lever_name,
                    )

        return sorted(
            missing,
        )
