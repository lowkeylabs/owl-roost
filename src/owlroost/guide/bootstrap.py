# src/owlroost/guide/bootstrap.py
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

from owlroost.guide.providers import (
    iter_providers,
)
from owlroost.guide.registry import (
    GuideRegistry,
)


def build_guide_registry():
    reg = GuideRegistry()

    for provider in iter_providers():
        provider.register(reg)

    return reg
