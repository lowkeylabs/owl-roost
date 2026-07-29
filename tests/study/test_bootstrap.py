# tests/study/test_bootstrap.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for study subsystem bootstrap.
"""

from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)
from owlroost.study.registry import (
    StudyRegistry,
)

# =========================================================
# Bootstrap
# =========================================================


def test_build_study_registry_returns_registry():
    registry = build_study_registry()

    assert isinstance(
        registry,
        StudyRegistry,
    )


def test_registry_contains_studies():
    registry = build_study_registry()

    assert registry.all_studies()


def test_registry_contains_experiments():
    registry = build_study_registry()

    assert registry.all_experiments()


def test_all_study_experiment_relationships_resolve():
    registry = build_study_registry()

    for study in registry.all_studies():
        experiments = registry.experiments_for_study(
            study.name,
        )

        assert len(experiments) == len(
            study.experiment_names,
        )


def test_bootstrap_returns_fresh_registry():
    registry1 = build_study_registry()

    registry2 = build_study_registry()

    assert registry1 is not registry2


def test_studies_are_sorted():
    registry = build_study_registry()

    studies = registry.all_studies()

    assert studies == sorted(
        studies,
        key=lambda study: study.name,
    )


def test_all_referenced_experiments_are_registered():
    """
    Every experiment referenced by a study
    must be registered.
    """

    registry = build_study_registry()

    registered = {experiment.name for experiment in registry.all_experiments()}

    referenced = {
        experiment_name
        for study in registry.all_studies()
        for experiment_name in study.experiment_names
    }

    missing = referenced - registered

    assert not missing, f"Studies reference unregistered experiments: {sorted(missing)}"


def test_every_study_has_experiments():
    """
    Every registered study should expose
    at least one experiment.
    """

    registry = build_study_registry()

    empty = [study.name for study in registry.all_studies() if not study.experiment_names]

    assert not empty, f"Studies without experiments: {sorted(empty)}"
