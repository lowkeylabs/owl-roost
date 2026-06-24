# src/owlroost/comparison/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Comparison semantic specifications.

Notes
-----
ComparisonSpec defines canonical
comparison ontology.

Comparison observations describe:

    - comparison groups
    - shared attributes
    - differing attributes
    - comparative relationships

These values materialize into:

    row["_comparison"]

and participate in catalog synthesis
alongside schema, metrics, and workspace
observations.

Architectural Invariant
-----------------------
Comparison observations are not produced
during OWL execution.

They are computed after row selection and
group formation, operating across multiple
rows simultaneously.

Comparison values therefore represent
comparative analysis rather than primary
execution outputs.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from owlroost.catalog.ontology import (
    OntologySpec,
)


@dataclass(kw_only=True)
class ComparisonSpec(
    OntologySpec,
):
    """
    Canonical comparison observation.
    """

    # =====================================================
    # Identity
    # =====================================================

    name: str

    description: str = ""

    # =====================================================
    # Authoring
    # =====================================================

    defined_in: str | None = None

    # =====================================================
    # Typing
    # =====================================================

    dtype: type | None = object

    # =====================================================
    # Materialization
    # =====================================================

    compute_fn: Callable[[dict[str, Any]], Any] | None = None

    # =====================================================
    # Notes
    # =====================================================

    notes: str = ""
