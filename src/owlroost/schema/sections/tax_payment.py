# src/owlroost/schema/sections/tax_payment.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tax payment history schema section.

Notes
-----
Defines historical tax payment observations.

Each ``[[history.tax_payment]]`` TOML table
represents one tax payment made by the
household.

Architectural Invariant
-----------------------
This module owns:

    - record model
    - collection model
    - schema registration
    - ontology metadata

for the ``history.tax_payment`` record
collection.
"""

from __future__ import annotations

import datetime
from typing import Literal

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


class TaxPaymentRecord(
    BaseSectionConfig,
):
    """
    One historical tax payment.
    """

    date: datetime.date = Field(
        description="Date the payment was made.",
    )

    tax_year: int = Field(
        ge=0,
        description="Tax year associated with the payment.",
    )

    tax_type: Literal[
        "federal",
        "state",
        "local",
        "property",
        "estimated",
        "other",
    ] = Field(
        description="Category of tax paid.",
    )

    agency: str = Field(
        description="Receiving tax authority.",
    )

    payment_type: Literal[
        "withholding",
        "quarterly",
        "extension",
        "return",
        "penalty",
        "interest",
        "other",
    ] = Field(
        description="Reason or mechanism for the payment.",
    )

    amount: float = Field(
        ge=0.0,
        description="Payment amount.",
    )


# =========================================================
# Collection Model
# =========================================================


class TaxPaymentHistoryConfig(
    BaseSectionConfig,
):
    """
    Historical tax payment collection.
    """

    tax_payment: list[TaxPaymentRecord] = Field(
        default_factory=list,
        description="Historical tax payment observations.",
    )


# =========================================================
# Registration
# =========================================================


def register_schema_fields(
    reg,
):
    """
    Register tax payment history fields.

    Only the record fields are cataloged.

    Individual tax payment instances are
    runtime observations rather than schema
    variables.
    """

    prefix = "history.tax_payment"

    for name, field in walk_model(
        "",
        TaxPaymentRecord,
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
                    "tax_payment",
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


class TaxPaymentHistory(
    HistoryCollection[TaxPaymentRecord],
):
    """
    Materialized planning cycle history.

    Represents the collection of historical
    planning cycle observations associated
    with a household.

    Each record corresponds to one completed
    planning cycle.
    """

    pass


def register_history_collection(
    reg,
):
    reg.register(
        name="tax_payment",
        collection_type=TaxPaymentHistory,
    )
