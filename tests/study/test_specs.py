# tests/study/test_specs.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for study subsystem specifications.
"""

from __future__ import annotations

from owlroost.study.specs import (
    ExperimentSpec,
    StudySpec,
)

# =========================================================
# StudySpec
# =========================================================


def test_study_defaults():
    study = StudySpec(
        name="market_uncertainty",
        title="Market Uncertainty",
        description="Evaluate spending robustness.",
    )

    assert study.name == "market_uncertainty"
    assert study.title == "Market Uncertainty"
    assert study.description == "Evaluate spending robustness."

    assert study.experiment_names == []
    assert study.profiles == {}


def test_study_experiments():
    study = StudySpec(
        name="market_uncertainty",
        title="Market Uncertainty",
        description="",
        experiment_names=[
            "bootstrap_quick",
            "historical_regimes",
        ],
    )

    assert study.experiment_names == [
        "bootstrap_quick",
        "historical_regimes",
    ]


# =========================================================
# ExperimentSpec
# =========================================================


def test_experiment_defaults():
    experiment = ExperimentSpec(
        name="bootstrap",
        title="Bootstrap",
        description="Bootstrap market returns.",
    )

    assert experiment.name == "bootstrap"
    assert experiment.title == "Bootstrap"
    assert experiment.description == "Bootstrap market returns."

    assert experiment.required_levers == [
        "workspace.levers.is_initialized",
    ]

    assert experiment.optional_levers == []

    assert experiment.fixed_overrides == []

    assert experiment.variable_overrides == []

    assert experiment.defined_in is None

    assert experiment.profiles == {}


def test_experiment_custom_fields():
    experiment = ExperimentSpec(
        name="bootstrap",
        title="Bootstrap",
        description="",
        required_levers=[
            "workspace.levers.has_results",
        ],
        optional_levers=[
            "workspace.levers.has_history",
        ],
        fixed_overrides=[
            "method=bootstrap",
            "trials=100",
        ],
        variable_overrides=[
            "window=full,modern",
        ],
        defined_in="market_uncertainty.py",
    )

    assert experiment.required_levers == [
        "workspace.levers.has_results",
    ]

    assert experiment.optional_levers == [
        "workspace.levers.has_history",
    ]

    assert experiment.fixed_overrides == [
        "method=bootstrap",
        "trials=100",
    ]

    assert experiment.variable_overrides == [
        "window=full,modern",
    ]

    assert experiment.defined_in == "market_uncertainty.py"


def test_hydra_overrides():
    experiment = ExperimentSpec(
        name="bootstrap",
        title="Bootstrap",
        description="",
        fixed_overrides=[
            "method=bootstrap",
            "trials=100",
        ],
        variable_overrides=[
            "window=full",
            "window=modern",
        ],
    )

    assert experiment.hydra_overrides() == [
        "method=bootstrap",
        "trials=100",
        "window=full",
        "window=modern",
    ]


def test_hydra_overrides_empty():
    experiment = ExperimentSpec(
        name="empty",
        title="Empty",
        description="",
    )

    assert experiment.hydra_overrides() == []
