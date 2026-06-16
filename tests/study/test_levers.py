from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_social_security_choice_template():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "ss_yearly_sweep",
    )

    assert template.decision_name == ("social_security")

    assert "has_ss_pia" in (template.required_levers)


def test_roth_conversion_choice_template():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "roth_bracket_fill",
    )

    assert template.decision_name == ("roth_conversion")

    assert "has_pretax_savings" in (template.required_levers)
