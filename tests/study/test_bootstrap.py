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
