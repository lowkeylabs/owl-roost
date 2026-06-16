from __future__ import annotations

from owlroost.study.specs import (
    DecisionSpec,
    LeverSpec,
)


def test_decision_spec():
    spec = DecisionSpec(
        name="social_security",
        title="Social Security",
        category="decision",
        description="Test",
    )

    assert spec.name == "social_security"

    assert spec.title == "Social Security"


def test_lever_spec():
    spec = LeverSpec(
        name="social_security",
        title="Social Security Lever",
        description="Test",
        decision_names=[
            "social_security",
        ],
        applicable_fn=lambda row: True,
    )

    assert spec.name == "social_security"

    assert spec.decision_names == [
        "social_security",
    ]
