# src/owlroost/metrics/plugins/hydra_overrides.py
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

from ..registry import MetricSpec

# =========================================================
# Plugin
# =========================================================


class HydraOverridesPlugin:
    """
    Comparative analytical metrics derived
    from Hydra override structure.

    These metrics are:

        - NOT persisted
        - computed dynamically
        - depend on comparison groups
        - support multirun comparison
        - support explainability workflows
        - support sweep interpretation

    These metrics intentionally model:

        comparative analytical semantics

    rather than direct runtime
    observations.
    """

    def register(
        self,
        registry,
    ):
        # =================================================
        # Common Overrides
        # =================================================

        registry.register(
            MetricSpec(
                # =========================================
                # Identity
                # =========================================
                name=("run_execution.common_overrides"),
                category="derived_metric",
                description=("Overrides shared across comparison group."),
                # =========================================
                # Provenance
                # =========================================
                defined_in=__name__,
                derived_from=[
                    "_meta.task_overrides",
                ],
                # =========================================
                # Typing
                # =========================================
                dtype=dict,
                # =========================================
                # Ontology
                # =========================================
                owner="ROOST",
                semantic_domain="design",
                value_origin="roost-computed",
                projection_kind="synthetic",
                analytic_kind="comparative",
                materialization_level="session",
                # =========================================
                # Materialization
                # =========================================
                compute_fn=None,
                # =========================================
                # Aggregation
                # =========================================
                aggregatable=False,
                default_aggregates=[],
                aggregate_function=None,
                # =========================================
                # Notes
                # =========================================
                notes=(
                    "Computed dynamically from "
                    "Hydra task overrides visible "
                    "within a comparison group."
                ),
            )
        )

        # =================================================
        # Run-Specific Overrides
        # =================================================

        registry.register(
            MetricSpec(
                # =========================================
                # Identity
                # =========================================
                name=("run_execution.run_specific_overrides"),
                category="derived_metric",
                description=("Overrides unique within comparison group."),
                # =========================================
                # Provenance
                # =========================================
                defined_in=__name__,
                derived_from=[
                    "_meta.task_overrides",
                ],
                # =========================================
                # Typing
                # =========================================
                dtype=dict,
                # =========================================
                # Ontology
                # =========================================
                owner="ROOST",
                semantic_domain="design",
                value_origin="roost-computed",
                projection_kind="synthetic",
                analytic_kind="comparative",
                materialization_level="session",
                # =========================================
                # Materialization
                # =========================================
                compute_fn=None,
                # =========================================
                # Aggregation
                # =========================================
                aggregatable=False,
                default_aggregates=[],
                aggregate_function=None,
                # =========================================
                # Notes
                # =========================================
                notes=(
                    "Computed dynamically from "
                    "Hydra task overrides visible "
                    "within a comparison group."
                ),
            )
        )

        registry.register(
            MetricSpec(
                # =========================================
                # Identity
                # =========================================
                name=("run_execution.task_overrides"),
                category="derived_metric",
                description=("Overrides shared across comparison group."),
                # =========================================
                # Provenance
                # =========================================
                defined_in=__name__,
                derived_from=[
                    "_meta.task_overrides",
                ],
                # =========================================
                # Typing
                # =========================================
                dtype=dict,
                # =========================================
                # Ontology
                # =========================================
                owner="ROOST",
                semantic_domain="design",
                value_origin="roost-computed",
                projection_kind="synthetic",
                analytic_kind="comparative",
                materialization_level="run",
                # =========================================
                # Materialization
                # =========================================
                compute_fn=lambda row: row.get("_meta", {}).get("task_overrides", "xxx"),
                # =========================================
                # Aggregation
                # =========================================
                aggregatable=False,
                default_aggregates=[],
                aggregate_function=None,
                # =========================================
                # Notes
                # =========================================
                notes=(
                    "Computed dynamically from "
                    "Hydra task overrides visible "
                    "within a comparison group."
                ),
            )
        )
