from owlroost.guide.registry import (
    GuideRegistry,
)
from owlroost.guide.specs import (
    SuggestionSpec,
)


def test_register_single_suggestion():
    reg = GuideRegistry()

    reg.register(
        SuggestionSpec(
            name="x",
            title="X",
            description="desc",
        )
    )

    suggestions = reg.suggestions()

    assert len(suggestions) == 1
    assert suggestions[0].name == "x"


def test_registry_sorted_by_priority():
    reg = GuideRegistry()

    reg.register(
        SuggestionSpec(
            name="b",
            title="B",
            description="",
            priority=20,
        )
    )

    reg.register(
        SuggestionSpec(
            name="a",
            title="A",
            description="",
            priority=10,
        )
    )

    names = [s.name for s in reg.suggestions()]

    assert names == [
        "a",
        "b",
    ]


def test_get_returns_registered_item():
    reg = GuideRegistry()

    suggestion = SuggestionSpec(
        name="hello",
        title="Hello",
        description="",
    )

    reg.register(
        suggestion,
    )

    assert reg.get("hello") is suggestion


def test_get_unknown_returns_none():
    reg = GuideRegistry()

    assert reg.get("missing") is None
