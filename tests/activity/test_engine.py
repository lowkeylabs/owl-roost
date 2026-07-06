# tests/activity/test_engine.py

from owlroost.activity.engine import (
    evaluate,
)
from owlroost.activity.registry import (
    ActivityRegistry,
)
from owlroost.activity.specs import (
    ActivitySpec,
    ActivityState,
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


def test_no_requirements_is_ready():
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

    assert (
        len(
            evaluation.ready_activities,
        )
        == 1
    )

    result = evaluation.ready_activities[0]

    assert result.is_ready

    assert result.state == ActivityState.READY


def test_equal_requirement_is_ready():
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

    assert (
        len(
            evaluation.ready_activities,
        )
        == 1
    )

    result = evaluation.ready_activities[0]

    assert result.is_ready

    assert result.state == ActivityState.READY


def test_greater_than_requirement_is_ready():
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

    assert (
        len(
            evaluation.ready_activities,
        )
        == 1
    )

    result = evaluation.ready_activities[0]

    assert result.is_ready

    assert result.state == ActivityState.READY


def test_failed_requirement_is_blocked():
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

    assert (
        len(
            evaluation.ready_activities,
        )
        == 0
    )

    assert (
        len(
            evaluation.blocked_activities,
        )
        == 1
    )

    result = evaluation.blocked_activities[0]

    assert result.is_blocked

    assert result.state == ActivityState.BLOCKED


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

    result = evaluation.ready_activities[0]

    assert (
        len(
            result.requirement_results,
        )
        == 1
    )

    requirement = result.requirement_results[0]

    assert requirement.actual == 2

    assert requirement.satisfied


def test_ready_activity_counts():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(
            activity,
        ),
    )

    assert evaluation.activity_count == 1

    assert evaluation.ready_count == 1
    assert evaluation.blocked_count == 0

    #
    # Recommendation state.
    #
    assert len(evaluation.next_activities) == 1
    assert len(evaluation.upcoming_activities) == 0
    assert len(evaluation.hidden_activities) == 0

    result = evaluation.next_activities[0]

    assert result.is_ready
    assert result.is_next


def test_state_counts():
    row = make_row()

    activity = ActivitySpec(
        name="x",
        title="X",
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

    assert evaluation.state_counts[ActivityState.BLOCKED] == 1


def test_first_ready_activity_is_next():
    registry = ActivityRegistry()

    registry.register(
        ActivitySpec(
            name="a",
            title="A",
            display_order=10,
        )
    )

    registry.register(
        ActivitySpec(
            name="b",
            title="B",
            display_order=20,
        )
    )

    evaluation = evaluate(
        row=make_row(),
        registry=registry,
    )

    assert len(evaluation.next_activities) == 1
    assert len(evaluation.upcoming_activities) == 1

    assert evaluation.next_activities[0].activity.name == "a"
    assert evaluation.upcoming_activities[0].activity.name == "b"

    assert evaluation.next_activities[0].is_next
    assert evaluation.upcoming_activities[0].is_upcoming
