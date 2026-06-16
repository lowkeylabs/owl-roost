from __future__ import annotations

from owlroost.study.specs import (
    ChoiceTemplateSpec,
    DecisionSpec,
    LeverSpec,
)


def test_decision_spec():
    spec = DecisionSpec(
        name="social_security",
        title="Social Security",
        category="retirement",
        description="Test",
    )

    assert spec.name == "social_security"

    assert spec.title == "Social Security"

    assert spec.category == "retirement"


def test_choice_template_spec():
    spec = ChoiceTemplateSpec(
        name="yearly_sweep",
        decision_name="social_security",
        title="Yearly Sweep",
        description="Test",
        required_levers=[
            "has_ss_pia",
        ],
    )

    assert spec.name == "yearly_sweep"

    assert spec.decision_name == ("social_security")

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

    assert spec.name == "has_ss_pia"

    assert spec.applicable_fn(
        {},
    )
