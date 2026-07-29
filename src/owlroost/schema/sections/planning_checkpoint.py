# src/owlroost/schema/sections/planning_checkpoint.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
planning checkpoint history schema section.

Notes
-----
Defines historical planning checkpoint observations.

Each ``[[history.planning_cycle]]`` TOML table
represents one completed planning checkpoint and
captures the household financial state at the
beginning of that cycle.

Architectural Invariant
-----------------------
This module owns:

    - record model
    - collection model
    - schema registration
    - ontology metadata

for the ``history.planning_cycle`` record
collection.
"""

from __future__ import annotations

from datetime import date

from pydantic import (
    Field,
)

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import normalize_module_path
from owlroost.schema.registry import (
    FieldSpec,
)
from owlroost.schema.utils import (
    resolve_field_default,
    unwrap_annotation,
    walk_model,
)

from ..specs import (
    BaseSectionConfig,
    HistoryCollection,
)

# =========================================================
# Record Model
# =========================================================


class PlanningCheckpointRecord(
    BaseSectionConfig,
):
    """
    One historical planning checkpoint.
    """

    as_of: date = Field(
        description="Planning checkpoint effective date.",
    )

    taxable_savings_balances: list[float] = Field(
        default_factory=list,
        description="Taxable savings balances by household member.",
    )

    tax_deferred_savings_balances: list[float] = Field(
        default_factory=list,
        description="Tax-deferred savings balances by household member.",
    )

    tax_free_savings_balances: list[float] = Field(
        default_factory=list,
        description="Tax-free savings balances by household member.",
    )

    hsa_savings_balances: list[float] = Field(
        default_factory=list,
        description="Health Savings Account balances by household member.",
    )

    prior_12_months_essential_spending: float = Field(
        default=0.0,
        description="Essential spending during the previous twelve months.",
    )

    prior_12_months_discretionary_spending: float = Field(
        default=0.0,
        description="Discretionary spending during the previous twelve months.",
    )


# =========================================================
# Collection Model
# =========================================================


class PlanningCheckpointHistoryConfig(
    BaseSectionConfig,
):
    """
    Historical planning checkpoint collection.
    """

    planning_cycle: list[PlanningCheckpointRecord] = Field(
        default_factory=list,
        description="Historical planning checkpoint observations.",
    )


# =========================================================
# Registration
# =========================================================


def register_schema_fields(
    reg,
):
    """
    Register planning checkpoint history fields.

    Only the record fields are cataloged.

    Individual planning checkpoint instances are
    runtime observations rather than schema
    variables.
    """

    prefix = "history.planning_checkpoint"

    for name, field in walk_model(
        "",
        PlanningCheckpointRecord,
    ):
        full_name = f"{prefix}.{name}"

        if full_name in reg:
            continue

        reg.register(
            FieldSpec(
                # =========================================
                # Identity
                # =========================================
                name=full_name,
                dtype=unwrap_annotation(
                    field.annotation,
                ),
                # =========================================
                # Runtime Realization
                # =========================================
                path=(
                    "history",
                    "planning_checkpoint",
                )
                + tuple(name.split(".")),
                source="input",
                default=resolve_field_default(
                    field,
                ),
                # =========================================
                # Ontology
                # =========================================
                owner="ROOST",
                semantic_domain="history",
                value_origin="user-specified",
                projection_kind="canonical",
                analytic_kind="primary",
                materialization_level="case",
                node_type=CatalogNodeType.VARIABLE,
                # =========================================
                # Documentation
                # =========================================
                description=field.description or "",
                # =========================================
                # Provenance
                # =========================================
                defined_in=normalize_module_path(
                    __file__,
                ),
            )
        )


class PlanningCheckpointHistory(
    HistoryCollection[PlanningCheckpointRecord],
):
    """
    Materialized planning checkpoint history.

    Represents the collection of historical
    planning checkpoint observations associated
    with a household.

    Each record corresponds to one completed
    planning checkpoint.
    """

    pass


def register_history_collection(
    reg,
):
    reg.register(
        name="planning_checkpoint",
        collection_type=PlanningCheckpointHistory,
    )
