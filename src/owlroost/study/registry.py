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

* Decisions
* Choice templates
* Levers

Architectural Invariant
-----------------------

Relationships flow downward only:

    Decision
        ↓
    Choice Template
        ↓
    Lever

Decisions do not own applicability.

Choice templates own applicability.

A decision is applicable when at
least one of its choice templates
is applicable.
"""

from __future__ import annotations

from owlroost.exceptions import (
    RoostError,
)


class StudyRegistry:
    def __init__(
        self,
    ):
        self._decisions = {}

        self._choice_templates = {}

        self._levers = {}

    # =====================================================
    # Decisions
    # =====================================================

    def register_decision(
        self,
        spec,
    ):
        self._decisions[spec.name] = spec

    def get_decision(
        self,
        name,
    ):
        try:
            return self._decisions[name]

        except KeyError as exc:
            raise RoostError(f"Decision not found: {name}") from exc

    def all_decisions(
        self,
    ):
        return sorted(
            self._decisions.values(),
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

    def choice_templates_for_decision(
        self,
        decision_name,
    ):
        return [
            template
            for template in self.all_choice_templates()
            if (template.decision_name == decision_name)
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

    def choice_template_is_applicable(
        self,
        template_name,
        case_row,
    ):
        template = self.get_choice_template(
            template_name,
        )

        return all(
            self.get_lever(
                lever_name,
            ).applicable_fn(
                case_row,
            )
            for lever_name in template.required_levers
        )

    def applicable_choice_templates(
        self,
        case_row,
    ):
        applicable = []

        for template in self.all_choice_templates():
            if self.choice_template_is_applicable(
                template.name,
                case_row,
            ):
                applicable.append(
                    template,
                )

        return applicable

    def decision_is_applicable(
        self,
        decision_name,
        case_row,
    ):
        return any(
            template.decision_name == decision_name
            for template in self.applicable_choice_templates(
                case_row,
            )
        )

    def applicable_decisions(
        self,
        case_row,
    ):
        return [
            decision
            for decision in self.all_decisions()
            if (
                self.decision_is_applicable(
                    decision.name,
                    case_row,
                )
            )
        ]
