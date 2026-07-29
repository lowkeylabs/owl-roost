# tests/study/test_registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for the study registry.
"""

from __future__ import annotations

import pytest

from owlroost.exceptions import RoostError
from owlroost.study.registry import StudyRegistry
from owlroost.study.specs import (
    ExperimentSpec,
    StudySpec,
)

# =========================================================
# Helpers
# =========================================================


def make_study(
    name: str = "market_uncertainty",
    experiments: list[str] | None = None,
) -> StudySpec:
    return StudySpec(
        name=name,
        title=name.replace("_", " ").title(),
        description="",
        experiment_names=experiments or [],
    )


def make_experiment(
    name: str,
) -> ExperimentSpec:
    return ExperimentSpec(
        name=name,
        title=name.replace("_", " ").title(),
        description="",
    )


# =========================================================
# Construction
# =========================================================


def test_empty_registry():
    registry = StudyRegistry()

    assert registry.all_studies() == []
    assert registry.all_experiments() == []


# =========================================================
# Studies
# =========================================================


def test_register_and_get_study():
    registry = StudyRegistry()

    study = make_study()

    registry.register_study(
        study,
    )

    assert (
        registry.get_study(
            "market_uncertainty",
        )
        is study
    )


def test_all_studies_sorted():
    registry = StudyRegistry()

    registry.register_study(
        make_study("zeta"),
    )

    registry.register_study(
        make_study("alpha"),
    )

    registry.register_study(
        make_study("beta"),
    )

    assert [study.name for study in registry.all_studies()] == [
        "alpha",
        "beta",
        "zeta",
    ]


def test_get_missing_study():
    registry = StudyRegistry()

    with pytest.raises(
        RoostError,
        match="Study not found",
    ):
        registry.get_study(
            "missing",
        )


# =========================================================
# Experiments
# =========================================================


def test_register_and_get_experiment():
    registry = StudyRegistry()

    experiment = make_experiment(
        "bootstrap",
    )

    registry.register_experiment(
        experiment,
    )

    assert (
        registry.get_experiment(
            "bootstrap",
        )
        is experiment
    )


def test_all_experiments_sorted():
    registry = StudyRegistry()

    registry.register_experiment(
        make_experiment("zeta"),
    )

    registry.register_experiment(
        make_experiment("alpha"),
    )

    registry.register_experiment(
        make_experiment("beta"),
    )

    assert [experiment.name for experiment in registry.all_experiments()] == [
        "alpha",
        "beta",
        "zeta",
    ]


def test_get_missing_experiment():
    registry = StudyRegistry()

    with pytest.raises(
        RoostError,
        match="Experiment not found",
    ):
        registry.get_experiment(
            "missing",
        )


# =========================================================
# Relationships
# =========================================================


def test_experiments_for_study():
    registry = StudyRegistry()

    registry.register_experiment(
        make_experiment(
            "bootstrap",
        ),
    )

    registry.register_experiment(
        make_experiment(
            "historical",
        ),
    )

    registry.register_study(
        make_study(
            experiments=[
                "bootstrap",
                "historical",
            ],
        ),
    )

    experiments = registry.experiments_for_study(
        "market_uncertainty",
    )

    assert [experiment.name for experiment in experiments] == [
        "bootstrap",
        "historical",
    ]


def test_study_with_no_experiments():
    registry = StudyRegistry()

    registry.register_study(
        make_study(),
    )

    assert (
        registry.experiments_for_study(
            "market_uncertainty",
        )
        == []
    )


def test_experiments_for_unknown_study():
    registry = StudyRegistry()

    with pytest.raises(
        RoostError,
        match="Study not found",
    ):
        registry.experiments_for_study(
            "missing",
        )


def test_missing_experiment_reference_raises():
    registry = StudyRegistry()

    registry.register_study(
        make_study(
            experiments=[
                "bootstrap",
            ],
        ),
    )

    with pytest.raises(
        RoostError,
        match="Experiment not found",
    ):
        registry.experiments_for_study(
            "market_uncertainty",
        )
