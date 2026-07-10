# src/owlroost/package/builder.py
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

from datetime import datetime

from .specs import (
    EvidencePackage,
)


def build_evidence_package(
    planning_context,
):
    """
    Assemble an EvidencePackage.

    Currently scaffolds a minimal
    package containing only the
    planning context.
    """

    return EvidencePackage(
        title="Retirement Planning Evidence",
        generated_at=datetime.now(),
        planning_context=planning_context,
    )
