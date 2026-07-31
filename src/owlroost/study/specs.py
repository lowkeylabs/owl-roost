# src/owlroost/study/specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study subsystem specifications.

Notes
-----
Owns the analytical definition layer of
the study subsystem.

The study subsystem consists of two
definition-layer concepts:

    Study
        A collection of related
        experimental designs.

    Experiment
        A reusable experimental
        methodology.

Execution artifacts (Sessions, Runs,
and Trials) belong to the execution
subsystem and are not defined here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from owlroost.display.specs import DisplayProfile

STUDY_NAMESPACE = "study"
EXPERIMENT_NAMESPACE = "experiment"


@dataclass(
    frozen=True,
    slots=True,
)
class StudyFieldSpec:
    """
    Canonical description
    """

    name: str

    description: str


STUDY_FIELDS: tuple[StudyFieldSpec, ...] = (
    StudyFieldSpec(
        "name",
        "Canonical study identifier.",
    ),
    StudyFieldSpec(
        "title",
        "Human-readable study title.",
    ),
    StudyFieldSpec(
        "description",
        "Study description.",
    ),
    StudyFieldSpec(
        "experiment_names",
        "Experiments belonging to the study.",
    ),
    StudyFieldSpec(
        "prolog_files",
        "List of files to include at top of evidence package",
    ),
    StudyFieldSpec(
        "epilog_files",
        "List of files to include at bottom of evidence package",
    ),
    StudyFieldSpec(
        "case_row_views",
        "List of views displayed using load_case_rows",
    ),
    StudyFieldSpec(
        "run_row_views",
        "List of views displayed using load_run_rows.",
    ),
)

EXPERIMENT_FIELDS: tuple[StudyFieldSpec, ...] = (
    StudyFieldSpec(
        "name",
        "Canonical experiment identifier.",
    ),
    StudyFieldSpec(
        "title",
        "Human-readable experiment title.",
    ),
    StudyFieldSpec(
        "description",
        "Experiment description.",
    ),
    StudyFieldSpec(
        "required_levers",
        "Workspace requirements that must be satisfied.",
    ),
    StudyFieldSpec(
        "optional_levers",
        "Optional workspace capabilities.",
    ),
    StudyFieldSpec(
        "fixed_overrides",
        "Hydra overrides applied to every run.",
    ),
    StudyFieldSpec(
        "variable_overrides",
        "Hydra overrides expanded into multiple runs.",
    ),
    StudyFieldSpec(
        "defined_in",
        "Source module defining the experiment.",
    ),
)

# =========================================================
# Studies
# =========================================================


@dataclass(slots=True, frozen=True)
class StudySpec:
    """
    Defines a collection of related
    experimental designs.

    A study represents one coherent
    area of retirement investigation.

    Examples include:

        Market Uncertainty

        Beginning-of-Year Spending

        Social Security Claiming

        Roth Conversion

        Retirement Timing

    Studies organize experiments.

    Studies are definition-layer
    objects and do not own execution
    artifacts.
    """

    #
    # Identity
    #

    name: str

    title: str

    description: str

    #
    # Relationships
    #

    experiment_names: list[str] = field(
        default_factory=list,
    )

    prolog_files: list[dict | None] = field(
        default_factory=list,
    )

    epilog_files: list[dict | None] = field(
        default_factory=list,
    )

    case_row_views: list[dict | None] = field(
        default_factory=list,
    )
    run_row_views: list[dict | None] = field(
        default_factory=list,
    )

    #
    # Display
    #

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )


# =========================================================
# Experiments
# =========================================================


@dataclass(slots=True, frozen=True)
class ExperimentSpec:
    """
    Defines a reusable experimental
    design.

    An experiment specifies a
    methodology for generating
    retirement evidence.

    An experiment consists of:

        • Applicability requirements

        • Fixed model overrides

        • Variable model overrides

    Experiments are unrealized
    analytical designs.

    When materialized for a household,
    an experiment becomes a Session.

    The Session expands the variable
    overrides into one or more Runs.

    Runs are the primary analytical
    objects compared by ROOST.

    Examples include:

        Bootstrap Sequence of Returns

        Historical Average Returns

        Fixed Return Models

        Historical Replay

        Social Security Age Sweep

        Retirement Date Sweep
    """

    #
    # Identity
    #

    name: str

    title: str

    description: str

    #
    # Applicability
    #

    required_levers: list[str] = field(
        default_factory=lambda: [
            "workspace.levers.is_initialized",
        ],
    )

    optional_levers: list[str] = field(
        default_factory=list,
    )

    #
    # Experimental Design
    #

    fixed_overrides: list[str] = field(
        default_factory=list,
    )

    variable_overrides: list[str] = field(
        default_factory=list,
    )

    #
    # Provenance
    #

    defined_in: str | None = None

    #
    # Display
    #

    profiles: dict[
        str,
        DisplayProfile,
    ] = field(
        default_factory=dict,
    )

    def hydra_overrides(self) -> list[str]:
        """
        Return the complete Hydra
        override list required to
        execute the experiment.
        """
        return [
            *self.fixed_overrides,
            *self.variable_overrides,
        ]


def study_field_name(
    name: str,
) -> str:
    """
    Return the fully-qualified study
    field name.
    """
    return f"{STUDY_NAMESPACE}.{name}"


def experiment_field_name(
    name: str,
) -> str:
    """
    Return the fully-qualified
    experiment field name.
    """
    return f"{EXPERIMENT_NAMESPACE}.{name}"
