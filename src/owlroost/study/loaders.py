# src/owlroost/study/loaders.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Study row loaders.

Notes
-----
Transforms Study Registry definitions
into runtime rows consumed by the
display materialization pipeline.

Architectural Invariants
------------------------

Loaders own construction of runtime
rows.

They do not:

    * discover studies
    * execute experiments
    * render displays
    * modify registry objects

One row represents one
Study/Experiment pair.
"""

from __future__ import annotations

from owlroost.study.specs import (
    EXPERIMENT_FIELDS,
    STUDY_FIELDS,
    experiment_field_name,
    study_field_name,
)

# =========================================================
# Helpers
# =========================================================


def _spec_to_row(
    spec,
    fields,
    qualify,
) -> dict[str, object]:
    """
    Convert a specification object into
    a qualified row dictionary.

    Parameters
    ----------
    spec
        Specification object.

    fields
        Canonical field definitions.

    qualify
        Function producing the fully
        qualified field name.
    """

    return {
        qualify(field.name): getattr(
            spec,
            field.name,
        )
        for field in fields
    }


# =========================================================
# Row Construction
# =========================================================


def load_study_rows(
    study_registry,
) -> list[dict[str, object]]:
    """
    Construct runtime study rows.

    Each row represents one Study /
    Experiment pair.
    """

    rows: list[dict[str, object]] = []

    for study in study_registry.all_studies():
        experiments = study_registry.experiments_for_study(
            study.name,
        )

        #
        # Permit studies with no
        # registered experiments.
        #

        if not experiments:
            rows.append(
                {
                    "_study": {
                        "study": study,
                        "experiment": None,
                    },
                    **_spec_to_row(
                        study,
                        STUDY_FIELDS,
                        study_field_name,
                    ),
                }
            )

            continue

        #
        # One row per experiment.
        #

        for experiment in experiments:
            rows.append(
                {
                    "_study": {
                        "study": study,
                        "experiment": experiment,
                    },
                    **_spec_to_row(
                        study,
                        STUDY_FIELDS,
                        study_field_name,
                    ),
                    **_spec_to_row(
                        experiment,
                        EXPERIMENT_FIELDS,
                        experiment_field_name,
                    ),
                }
            )

    return rows
