from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_build_study_registry():
    reg = build_study_registry()

    assert reg is not None


def test_decisions_discovered():
    reg = build_study_registry()

    names = {decision.name for decision in reg.all_decisions()}

    assert "social_security" in names

    assert "roth_conversion" in names


def test_levers_discovered():
    reg = build_study_registry()

    names = {lever.name for lever in reg.all_levers()}

    assert "has_ss_pia" in names

    assert "has_pretax_savings" in names
