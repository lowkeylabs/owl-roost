# src/owlroost/study/bootstrap.py
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

from owlroost.study.decisions import (
    register_all_decisions,
)
from owlroost.study.levers import (
    register_all_levers,
)
from owlroost.study.registry import (
    StudyRegistry,
)


def build_study_registry():
    reg = StudyRegistry()

    register_all_decisions(
        reg,
    )

    register_all_levers(
        reg,
    )

    return reg
