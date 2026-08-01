# src/owlroost/package/specs.py
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

from dataclasses import dataclass
from datetime import datetime

from owlroost.workspace.specs import (
    WorkspacePlanningContext,
)


@dataclass(
    slots=True,
    frozen=True,
)
class EvidencePackage:
    """
    Publishable retirement planning
    evidence.

    This is the primary artifact
    produced by ROOST.
    """

    title: str

    generated_at: datetime

    planning_context: WorkspacePlanningContext

    documents: list[dict] | None = None
