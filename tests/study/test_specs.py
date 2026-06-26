from __future__ import annotations

from owlroost.study.specs import (
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
