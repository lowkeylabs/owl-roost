# tests/guide/test_engine.py

from owlroost.activity.engine import (
    evaluate,
)
from owlroost.activity.registry import (
    ActivityRegistry,
)
from owlroost.activity.specs import (
    ActivitySpec,
    Requirement,
)


def make_row():
    return {
        "_context": {
            "workspace_initialized": False,
            "valid_case_count": 2,
        }
    }


def make_registry(
    activity,
):
    registry = ActivityRegistry()

    registry.register(
        activity,
    )

    return registry


def test_no_requirements_is_applicable():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
        description="",
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(
            activity,
        ),
    )

    assert len(evaluation.applicable_activities) == 1

    assert evaluation.applicable_activities[0].applicable


def test_equal_requirement():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
        description="",
        requirements=[
            Requirement(
                "context.workspace_initialized",
                "==",
                False,
            )
        ],
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(
            activity,
        ),
    )

    assert len(evaluation.applicable_activities) == 1

    assert evaluation.applicable_activities[0].applicable


def test_greater_than_requirement():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
        description="",
        requirements=[
            Requirement(
                "context.valid_case_count",
                ">",
                0,
            )
        ],
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(
            activity,
        ),
    )

    assert len(evaluation.applicable_activities) == 1

    assert evaluation.applicable_activities[0].applicable


def test_failed_requirement():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
        description="",
        requirements=[
            Requirement(
                "context.valid_case_count",
                ">",
                5,
            )
        ],
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(
            activity,
        ),
    )

    assert len(evaluation.applicable_activities) == 0

    assert len(evaluation.rejected_activities) == 1

    assert not evaluation.rejected_activities[0].applicable


def test_requirement_results_are_recorded():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
        description="",
        requirements=[
            Requirement(
                "context.valid_case_count",
                ">",
                0,
            )
        ],
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(
            activity,
        ),
    )

    result = evaluation.applicable_activities[0]

    assert len(result.requirement_results) == 1

    requirement = result.requirement_results[0]

    assert requirement.actual == 2

    assert requirement.satisfied
