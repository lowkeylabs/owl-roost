from owlroost.guide.engine import (
    evaluate,
)
from owlroost.guide.registry import (
    GuideRegistry,
)
from owlroost.guide.specs import (
    Requirement,
    SuggestionSpec,
)


def make_row():
    return {
        "_context": {
            "workspace_initialized": False,
            "valid_case_count": 2,
        }
    }


def make_registry(suggestion):
    registry = GuideRegistry()
    registry.register(suggestion)
    return registry


def test_no_requirements_is_applicable():
    row = make_row()

    suggestion = SuggestionSpec(
        name="x",
        title="X",
        description="",
    )

    evaluation = evaluate(
        row=row,
        registry=make_registry(suggestion),
    )

    assert len(evaluation.applicable_suggestions) == 1
    assert evaluation.applicable_suggestions[0].applicable


def test_equal_requirement():
    row = make_row()

    suggestion = SuggestionSpec(
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
        registry=make_registry(suggestion),
    )

    assert len(evaluation.applicable_suggestions) == 1
    assert evaluation.applicable_suggestions[0].applicable


def test_greater_than_requirement():
    row = make_row()

    suggestion = SuggestionSpec(
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
        registry=make_registry(suggestion),
    )

    assert len(evaluation.applicable_suggestions) == 1
    assert evaluation.applicable_suggestions[0].applicable


def test_failed_requirement():
    row = make_row()

    suggestion = SuggestionSpec(
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
        registry=make_registry(suggestion),
    )

    assert len(evaluation.applicable_suggestions) == 0
    assert len(evaluation.rejected_suggestions) == 1
    assert not evaluation.rejected_suggestions[0].applicable
