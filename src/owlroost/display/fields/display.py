# src/owlroost/display/fields/display.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Methodology display fields.

Notes
-----
Synthetic display fields used by
planning and methodology views.

These fields provide catalog identity
and presentation metadata for
computed methodology displays and
profile overrides for methodology-
related variables.
"""

from __future__ import annotations

from datetime import date

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import normalize_module_path
from owlroost.display.formatting import format_value
from owlroost.display.operations.normalize import (
    get_units_multiplier,
)
from owlroost.display.specs import (
    DisplayField,
    DisplayProfile,
)

# =========================================================
# Abbreviations
# =========================================================

ABBREVIATIONS = {
    "optimization_parameters.objective": {
        "maxSpending": "mxSpd",
        "maxBequest": "mxBeq",
    },
    "rates_selection.method": {
        "historical_average": "histAvg",
        "historical": "hist",
        "historical_bootstrap": "hBoot",
        "garch_dcc": "garDcc",
        "historical_lognormal": "hLogNorm",
    },
}

# =========================================================
# Methodology Ontology
# =========================================================


DISPLAY_ONTOLOGY = dict(
    defined_in=normalize_module_path(__file__),
)

STARTING_AGES_DISPLAY_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="decision",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="primary",
    materialization_level="run",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

RATES_WINDOW_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="design",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="primary",
    materialization_level="run",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

COMPLETION_FRACTION_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="design",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="primary",
    materialization_level="run",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

OG_ONTOLOGY = dict(
    owner="ROOST",
    semantic_domain="decision",
    value_origin="roost-computed",
    projection_kind="synthetic",
    analytic_kind="primary",
    materialization_level="run",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)


# =========================================================
# Registration
# =========================================================


def register_display_fields(
    reg,
):
    """
    Register methodology display fields.
    """

    # =====================================================
    # Optimization Goal
    # =====================================================

    reg.register_display_field(
        DisplayField.field(
            "display.optimization_goal",
            display_fn=compute_optimization_goal,
            description=(
                "Combined optimization objective and associated target (for display.  there is another for input)."
            ),
            profiles={
                "table": DisplayProfile(
                    label="Goal",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Optimization Goal",
                    width=24,
                ),
            },
            **OG_ONTOLOGY,
            derived_from=[
                "optimization_parameters.objective",
                "solver_options.bequest",
                "solver_options.net_spending",
            ],
        )
    )

    # =====================================================
    # Compact Rates
    # =====================================================

    reg.register_display_field(
        DisplayField.field(
            "display.compact_rates",
            display_fn=display_compact_rates,
            description=("Combined rates_method and relavant params for brevity."),
            profiles={
                "table": DisplayProfile(
                    label="Rate Model",
                    width="auto",
                ),
                "pivot": DisplayProfile(
                    label="Compact rate model and params",
                    width="auto",
                ),
            },
            **OG_ONTOLOGY,
            derived_from=[
                "rates_selection.method",
                "rates_selection.from",
                "rates_selection.to",
                "rates_selection.values",
            ],
        )
    )

    # =====================================================
    # Rates Window
    # =====================================================

    reg.register_display_field(
        DisplayField.field(
            "display.rates_window",
            display_fn=compute_rates_window,
            description=("Historical rates selection window."),
            profiles={
                "table": DisplayProfile(
                    label="Rates\nWindow",
                    width=12,
                ),
                "pivot": DisplayProfile(
                    label="Rates Window",
                    width=18,
                ),
            },
            **RATES_WINDOW_ONTOLOGY,
        )
    )

    # =====================================================
    # Trials Per Run
    # =====================================================

    reg.register_display_field(
        DisplayField.field(
            "roost_settings.trials_per_run",
            profiles={
                "table": DisplayProfile(
                    label="Trials\nPer\nRun",
                    width=10,
                ),
                "pivot": DisplayProfile(
                    label="Trials Per Run",
                    width=16,
                ),
            },
            **DISPLAY_ONTOLOGY,
        )
    )

    # =====================================================
    # Rates Method
    # =====================================================

    reg.register_display_field(
        DisplayField.field(
            "rates_selection.method",
            description=("Rates sampling methodology."),
            profiles={
                "table": DisplayProfile(
                    label="Rates",
                    width=10,
                ),
                "pivot": DisplayProfile(
                    label="Rates Method",
                    width=16,
                ),
            },
            **DISPLAY_ONTOLOGY,
        )
    )

    reg.register_display_field(
        DisplayField.field(
            field_name="display.completion_fraction",
            display_fn=completion_ratio_display,
            description=("Completed trials relative to configured trials per run."),
            profiles={
                "table": DisplayProfile(
                    label="Trials",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Completion Fraction",
                    content_align="center",
                ),
            },
            **COMPLETION_FRACTION_ONTOLOGY,
        )
    )

    reg.register_display_field(
        DisplayField.field(
            field_name="display.starting_ages",
            display_fn=current_ages_display,
            description=("Ages of household members (Start Date - DOB)"),
            profiles={
                "table": DisplayProfile(
                    label="Start\nAge(s)",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Ages(s) on OWL start date",
                    content_align="center",
                ),
            },
            **STARTING_AGES_DISPLAY_ONTOLOGY,
        )
    )

    reg.register_display_field(
        DisplayField.field(
            field_name="basic_info.life_expectancy",
            profiles={
                "table": DisplayProfile(
                    label="Expect\nAge(s)",
                    content_align="center",
                ),
                "pivot": DisplayProfile(
                    label="Life expectancy(ies)",
                    content_align="center",
                ),
            },
            **DISPLAY_ONTOLOGY,
        )
    )


# =========================================================
# Display Functions
# =========================================================


def get_inputs(
    row,
):
    return row.get(
        "_inputs",
        {},
    )


def get_hfp(
    row,
):
    return row.get(
        "_hfp",
        {},
    )


def safe_sum(
    values,
):
    return sum(float(v or 0) for v in values)


def make_abbreviation_display(
    field_path,
):
    """
    Build abbreviation display function.

    Maps long-form semantic values to compact
    operational display abbreviations.

    Examples:

        maxSpending -> mxSpd
        historical  -> hist
    """

    mapping = ABBREVIATIONS.get(
        field_path,
        {},
    )

    path_parts = field_path.split(".")

    def display_fn(
        row,
    ):
        try:
            value = row.get(
                "_inputs",
                {},
            )

            for part in path_parts:
                value = value.get(
                    part,
                )

                if value is None:
                    return None

            return mapping.get(
                value,
                value,
            )

        except Exception:
            return None

    return display_fn


def compute_optimization_goal(row):
    """
    Combined optimization goal display.

    Examples:

        mxSpd/$0
        mxBeq/$180K
        mxBeq/$1.2M
    """

    # -----------------------------------------------------
    # Objective abbreviation
    # -----------------------------------------------------

    objective_short = make_abbreviation_display("optimization_parameters.objective")(row)

    if objective_short is None:
        return None

    # -----------------------------------------------------
    # Inputs
    # -----------------------------------------------------

    inputs = row.get(
        "_inputs",
        {},
    )

    solver = inputs.get(
        "solver_options",
        {},
    )

    objective = inputs.get(
        "optimization_parameters",
        {},
    ).get(
        "objective",
    )

    # -----------------------------------------------------
    # Select relevant value
    # -----------------------------------------------------

    if objective == "maxSpending":
        value = solver.get("bequest")

    elif objective == "maxBequest":
        value = solver.get("netSpending")

    else:
        return objective_short

    # -----------------------------------------------------
    # No associated value
    # -----------------------------------------------------

    if value is None:
        return objective_short

    # -----------------------------------------------------
    # Convert OWL-scaled units -> dollars
    # -----------------------------------------------------

    units = solver.get(
        "units",
        "k",
    )

    multiplier = get_units_multiplier(
        units,
    )

    canonical_dollars = float(value) * multiplier

    # -----------------------------------------------------
    # Compact currency formatting
    # -----------------------------------------------------

    formatted = format_value(
        canonical_dollars,
        fmt="currency_short",
    )

    return f"{objective_short}/{formatted}"


def compute_rates_window(row):
    """
    Combined historical rates window.

    Examples:

        1928-2025
        1960-1975
    """

    inputs = row.get(
        "_inputs",
        {},
    )

    rates = inputs.get(
        "rates_selection",
        {},
    )

    start = rates.get("from")
    end = rates.get("to")

    if start is None or end is None:
        return None

    return f"{start}-{end}"


def completion_ratio_display(
    row,
):
    """
    Return compact completion ratio.

    Examples:

        0/50
        17/50
        50/50
    """

    try:
        completed = row.get(
            "_metrics",
            {},
        ).get("trial.completed")

        total = (
            row.get(
                "_inputs",
                {},
            )
            .get(
                "roost_settings",
                {},
            )
            .get("trials_per_run")
        )

        if completed is None or total is None:
            return "."

        return f"{completed}/{total}"

    except Exception:
        return "."


def current_ages_display(
    row,
):
    try:
        basic = get_inputs(row).get("basic_info", {})

        dob_values = basic.get(
            "date_of_birth",
            [],
        )

        start_date_str = basic.get(
            "start_date",
        )

        if not dob_values or not start_date_str:
            return None

        start = date.fromisoformat(start_date_str)

        ages = []

        for dob_str in dob_values:
            dob = date.fromisoformat(dob_str)

            age = start.year - dob.year - ((start.month, start.day) < (dob.month, dob.day))

            ages.append(age)

        return "/".join(str(x) for x in ages)

    except Exception:
        return None


def format_rate(
    value,
):
    value = float(value)

    if value.is_integer():
        return str(
            int(value),
        )

    return f"{value:.1f}"


def display_compact_rates(
    row,
):
    """
    Compact rates display.

    Examples
    --------
    hist(1928-2025)
    histAvg(1928-2025)
    bSOR(1960-2020)
    hLogNorm(1928-2025)

    user(7,5,2)

    optimistic
    conservative
    default
    """

    rates = row.get(
        "_inputs",
        {},
    ).get(
        "rates_selection",
        {},
    )

    sweeps = row.get(
        "_inputs",
        {},
    ).get(
        "roost_sweeps",
        {},
    )
    named_window = sweeps.get("named_window", None)

    method = rates.get(
        "method",
    )

    if not method:
        return None

    short = make_abbreviation_display(
        "rates_selection.method",
    )(row)

    # -----------------------------------------------------
    # Historical window methods
    # -----------------------------------------------------

    if method in {
        "bootstrap_sor",
        "historical_bootstrap",
        "garch_dcc",
        "historical",
        "historical_average",
        "historical_lognormal",
    }:
        start = rates.get("from")
        end = rates.get("to")

        if named_window:
            return rf"{short}\[{named_window}]"

        if start is not None and end is not None:
            window = f"{start}-{end}"
            return f"{short}[{window}]"

        return short

    # -----------------------------------------------------
    # User-specified rates
    # -----------------------------------------------------

    if method == "user":
        values = rates.get(
            "values",
        )

        if values:
            values_str = ",".join(format_rate(v) for v in values)

            return f"{short}[{values_str}]"

        return short

    # -----------------------------------------------------
    # Standalone methods
    # -----------------------------------------------------

    if method in {
        "optimistic",
        "conservative",
        "trailing_30",
        "default",
    }:
        return short

    # -----------------------------------------------------
    # Fallback
    # -----------------------------------------------------

    return f"{short}-untrapped"
