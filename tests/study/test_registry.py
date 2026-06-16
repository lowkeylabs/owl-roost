from __future__ import annotations

from owlroost.study.registry import (
    StudyRegistry,
)
from owlroost.study.specs import (
    DecisionSpec,
)


def test_register_decision():
    reg = StudyRegistry()

    reg.register_decision(
        DecisionSpec(
            name="test",
            title="Test",
            category="decision",
            description="Test",
        )
    )

    decision = reg.get_decision(
        "test",
    )

    assert decision.name == "test"


def test_all_decisions():
    reg = StudyRegistry()

    reg.register_decision(
        DecisionSpec(
            name="b",
            title="B",
            category="decision",
            description="B",
        )
    )

    reg.register_decision(
        DecisionSpec(
            name="a",
            title="A",
            category="decision",
            description="A",
        )
    )

    names = [d.name for d in reg.all_decisions()]

    assert names == [
        "a",
        "b",
    ]
