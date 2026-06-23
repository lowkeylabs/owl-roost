from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_build_study_registry():
    reg = build_study_registry()

    assert reg is not None


def test_studies_discovered():
    reg = build_study_registry()

    names = {study.name for study in reg.all_studies()}

    assert "retirement_readiness" in names

    assert "social_security_strategy" in names

    assert "roth_conversion_strategy" in names


def test_questions_discovered():
    reg = build_study_registry()

    names = {question.name for question in reg.all_questions()}

    assert "can_i_retire" in names

    assert "should_i_retire" in names

    assert "when_should_i_claim_social_security" in names


def test_scenario_families_discovered():
    reg = build_study_registry()

    names = {scenario_family.name for scenario_family in reg.all_scenario_families()}

    assert "retirement_timing" in names

    assert "social_security_claiming" in names

    assert "roth_conversion" in names

    assert "market_regime" in names


def test_levers_discovered():
    reg = build_study_registry()

    names = {lever.name for lever in reg.all_levers()}

    assert "has_ss_pia" in names

    assert "has_pretax_savings" in names
