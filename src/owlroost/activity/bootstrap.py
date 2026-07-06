# src/owlroost/activity/bootstrap.py
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

from .activities import (
    iter_activities,
)
from .registry import (
    ActivityRegistry,
)


def build_activity_registry():
    reg = ActivityRegistry()

    for activity_module in iter_activities():
        activity_module.register(reg)

    return reg
