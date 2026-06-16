# src/owlroost/study/registry.py
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

from owlroost.exceptions import (
    RoostError,
)


class StudyRegistry:
    def __init__(self):
        self._decisions = {}
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
    # Evaluation
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

    def applicable_decisions(
        self,
        case_row,
    ):
        applicable = []

        for decision in self.all_decisions():
            if all(
                self.get_lever(
                    lever_name,
                ).applicable_fn(
                    case_row,
                )
                for lever_name in decision.required_levers
            ):
                applicable.append(
                    decision,
                )

        return applicable
