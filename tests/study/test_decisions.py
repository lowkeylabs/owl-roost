from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_social_security_decision():
    reg = build_study_registry()

    decision = reg.get_decision(
        "social_security",
    )

    assert decision.name == "social_security"

    assert decision.required_levers == [
        "has_ss_pia",
    ]


def test_roth_conversion_decision():
    reg = build_study_registry()

    decision = reg.get_decision(
        "roth_conversion",
    )

    assert decision.name == "roth_conversion"

    assert decision.required_levers == [
        "has_pretax_savings",
    ]
