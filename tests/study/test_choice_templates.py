from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_choice_templates_discovered():
    reg = build_study_registry()

    names = {template.name for template in reg.all_choice_templates()}

    assert "ss_yearly_sweep" in names

    assert "ss_monthly_sweep" in names

    assert "ss_owl_optimizer" in names

    assert "roth_bracket_fill" in names


def test_ss_yearly_sweep():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "ss_yearly_sweep",
    )

    assert template.scenario_family_name == "social_security_claiming"

    assert template.required_levers == [
        "has_ss_pia",
    ]


def test_ss_monthly_sweep():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "ss_monthly_sweep",
    )

    assert template.scenario_family_name == "social_security_claiming"

    assert template.required_levers == [
        "has_ss_pia",
    ]


def test_ss_owl_optimizer():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "ss_owl_optimizer",
    )

    assert template.scenario_family_name == "social_security_claiming"

    assert template.required_levers == [
        "has_ss_pia",
    ]


def test_roth_bracket_fill():
    reg = build_study_registry()

    template = reg.get_choice_template(
        "roth_bracket_fill",
    )

    assert template.scenario_family_name == "roth_conversion"

    assert template.required_levers == [
        "has_pretax_savings",
    ]


def test_social_security_templates():
    reg = build_study_registry()

    names = {
        template.name
        for template in (
            reg.choice_templates_for_scenario_family(
                "social_security_claiming",
            )
        )
    }

    assert names == {
        "ss_yearly_sweep",
        "ss_monthly_sweep",
        "ss_owl_optimizer",
    }


def test_roth_conversion_templates():
    reg = build_study_registry()

    names = {
        template.name
        for template in (
            reg.choice_templates_for_scenario_family(
                "roth_conversion",
            )
        )
    }

    assert names == {
        "roth_bracket_fill",
    }
