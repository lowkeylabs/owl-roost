from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_levers_discovered():
    reg = build_study_registry()

    names = {lever.name for lever in reg.all_levers()}

    assert "has_ss_pia" in names

    assert "has_pretax_savings" in names


def test_has_ss_pia_lever():
    reg = build_study_registry()

    lever = reg.get_lever(
        "has_ss_pia",
    )

    assert lever.name == ("has_ss_pia")


def test_has_pretax_savings_lever():
    reg = build_study_registry()

    lever = reg.get_lever(
        "has_pretax_savings",
    )

    assert lever.name == ("has_pretax_savings")


def test_social_security_choice_template_requires_ss_lever():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "ss_yearly_sweep",
    )

    assert "has_ss_pia" in (template.required_levers)


def test_roth_choice_template_requires_pretax_lever():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "roth_bracket_fill",
    )

    assert "has_pretax_savings" in (template.required_levers)
