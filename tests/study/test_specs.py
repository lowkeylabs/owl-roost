from __future__ import annotations

from owlroost.study.specs import (
    ChoiceTemplateSpec,
    LeverSpec,
    QuestionSpec,
    ScenarioFamilySpec,
    StudySpec,
)


def test_study_spec():
    spec = StudySpec(
        name="retirement_readiness",
        title="Retirement Readiness",
        description="Test",
    )

    assert spec.name == ("retirement_readiness")

    assert spec.title == ("Retirement Readiness")

    assert spec.question_names == []


def test_question_spec():
    spec = QuestionSpec(
        name="can_i_retire",
        title="Can I Retire?",
        category="retirement",
        description="Test",
        scenario_family_names=[
            "retirement_timing",
        ],
    )

    assert spec.name == ("can_i_retire")

    assert spec.category == ("retirement")

    assert spec.scenario_family_names == [
        "retirement_timing",
    ]

    assert spec.required_levers == []

    assert spec.related_questions == []


def test_scenario_family_spec():
    spec = ScenarioFamilySpec(
        name="retirement_timing",
        title="Retirement Timing",
        category="retirement",
        description="Test",
    )

    assert spec.name == ("retirement_timing")

    assert spec.title == ("Retirement Timing")

    assert spec.required_levers == []

    assert spec.related_scenario_families == []


def test_choice_template_spec():
    spec = ChoiceTemplateSpec(
        name="ss_age_yearly_sweep",
        scenario_family_name=("social_security_claiming"),
        title="Yearly Sweep",
        description="Test",
        required_levers=[
            "has_ss_pia",
        ],
    )

    assert spec.name == ("ss_age_yearly_sweep")

    assert spec.scenario_family_name == ("social_security_claiming")

    assert spec.required_levers == [
        "has_ss_pia",
    ]


def test_lever_spec():
    spec = LeverSpec(
        name="has_ss_pia",
        title="Has Social Security",
        description="Test",
        applicable_fn=lambda row: True,
    )

    assert spec.name == ("has_ss_pia")

    assert spec.applicable_fn(
        {},
    )
