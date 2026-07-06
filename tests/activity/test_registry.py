# tests/guide/test_registry.py

from owlroost.activity.registry import (
    ActivityRegistry,
)
from owlroost.activity.specs import (
    ActivitySpec,
)


def test_register_single_activity():
    reg = ActivityRegistry()

    reg.register(
        ActivitySpec(
            name="x",
            title="X",
            description="desc",
        )
    )

    activities = reg.all()

    assert len(activities) == 1

    assert activities[0].name == "x"


def test_registry_sorted_by_display_order():
    reg = ActivityRegistry()

    reg.register(
        ActivitySpec(
            name="b",
            title="B",
            description="",
            display_order=20,
        )
    )

    reg.register(
        ActivitySpec(
            name="a",
            title="A",
            description="",
            display_order=10,
        )
    )

    names = [activity.name for activity in reg.all()]

    assert names == [
        "a",
        "b",
    ]


def test_get_returns_registered_item():
    reg = ActivityRegistry()

    activity = ActivitySpec(
        name="hello",
        title="Hello",
        description="",
    )

    reg.register(
        activity,
    )

    assert reg.get("hello") is activity


def test_get_unknown_returns_none():
    reg = ActivityRegistry()

    assert reg.get("missing") is None
