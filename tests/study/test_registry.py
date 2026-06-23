from __future__ import annotations

from owlroost.study.registry import (
    StudyRegistry,
)
from owlroost.study.specs import (
    QuestionSpec,
    ScenarioFamilySpec,
    StudySpec,
)


def test_register_study():
    reg = StudyRegistry()

    reg.register_study(
        StudySpec(
            name="retirement_readiness",
            title="Retirement Readiness",
            description="Test",
        )
    )

    study = reg.get_study(
        "retirement_readiness",
    )

    assert study.name == ("retirement_readiness")


def test_all_studies():
    reg = StudyRegistry()

    reg.register_study(
        StudySpec(
            name="b",
            title="B",
            description="B",
        )
    )

    reg.register_study(
        StudySpec(
            name="a",
            title="A",
            description="A",
        )
    )

    names = [study.name for study in reg.all_studies()]

    assert names == [
        "a",
        "b",
    ]


def test_register_question():
    reg = StudyRegistry()

    reg.register_question(
        QuestionSpec(
            name="can_i_retire",
            title="Can I Retire?",
            category="retirement",
            description="Test",
        )
    )

    question = reg.get_question(
        "can_i_retire",
    )

    assert question.name == ("can_i_retire")


def test_all_questions():
    reg = StudyRegistry()

    reg.register_question(
        QuestionSpec(
            name="b",
            title="B",
            category="test",
            description="B",
        )
    )

    reg.register_question(
        QuestionSpec(
            name="a",
            title="A",
            category="test",
            description="A",
        )
    )

    names = [question.name for question in reg.all_questions()]

    assert names == [
        "a",
        "b",
    ]


def test_register_scenario_family():
    reg = StudyRegistry()

    reg.register_scenario_family(
        ScenarioFamilySpec(
            name="retirement_timing",
            title="Retirement Timing",
            category="retirement",
            description="Test",
        )
    )

    family = reg.get_scenario_family(
        "retirement_timing",
    )

    assert family.name == ("retirement_timing")


def test_all_scenario_families():
    reg = StudyRegistry()

    reg.register_scenario_family(
        ScenarioFamilySpec(
            name="b",
            title="B",
            category="test",
            description="B",
        )
    )

    reg.register_scenario_family(
        ScenarioFamilySpec(
            name="a",
            title="A",
            category="test",
            description="A",
        )
    )

    names = [family.name for family in reg.all_scenario_families()]

    assert names == [
        "a",
        "b",
    ]
