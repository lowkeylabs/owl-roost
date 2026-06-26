# src/owlroost/display/fields/scenario_families.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Scenario family display fields.

Notes
-----
Dynamically materializes one display
field per registered scenario family.

Each field indicates whether the
scenario family is available for
the current workspace.
"""

from __future__ import annotations

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.display.specs import (
    DisplayField,
)
from owlroost.study.bootstrap import (
    build_study_registry,
)

SCENARIO_FAMILY_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="decision",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="case",
    node_type=CatalogNodeType.VARIABLE,
)

CHECK_MARK = "✓"

NO_MARK = "-"


def make_display_fn(
    scenario_family,
):
    family_name = scenario_family.name

    def display_fn(
        row,
    ):
        family = (
            row.get(
                "_study",
                {},
            )
            .get(
                "scenario_families",
                {},
            )
            .get(
                family_name,
            )
        )

        if family is None:
            return NO_MARK

        experiments = family.get(
            "experiments",
            {},
        )

        if not experiments:
            return "-add experiments-"

        #
        # Scenario family is available if
        # ANY experiment is applicable.
        #
        for experiment in experiments.values():
            if experiment.get(
                "applicable",
                False,
            ):
                return CHECK_MARK

        return NO_MARK

    return display_fn


def register_display_fields(
    reg,
):
    study_registry = build_study_registry()

    for scenario_family in study_registry.all_scenario_families():
        reg.register_display_field(
            DisplayField.field(
                f"scenario_family.{scenario_family.name}",
                display_fn=make_display_fn(
                    scenario_family,
                ),
                description=(scenario_family.description),
                profiles=(scenario_family.profiles),
                **SCENARIO_FAMILY_ONTOLOGY,
                defined_in=(scenario_family.defined_in),
            )
        )
