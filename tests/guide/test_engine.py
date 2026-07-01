from owlroost.guide.engine import (
    applicable,
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


def test_no_requirements_is_applicable():
    row = make_row()

    suggestion = SuggestionSpec(
        name="x",
        title="X",
        description="",
    )

    assert applicable(
        row,
        suggestion,
    )


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

    assert applicable(
        row,
        suggestion,
    )


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

    assert applicable(
        row,
        suggestion,
    )


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

    assert not applicable(
        row,
        suggestion,
    )
