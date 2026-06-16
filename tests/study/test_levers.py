from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_social_security_decision():
    reg = build_study_registry()

    decision = reg.get_decision(
        "social_security",
    )

    assert "has_ss_pia" in decision.required_levers


def test_roth_conversion_decision():
    reg = build_study_registry()

    decision = reg.get_decision(
        "roth_conversion",
    )

    assert "has_pretax_savings" in decision.required_levers
