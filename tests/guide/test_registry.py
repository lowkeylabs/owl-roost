# tests/guide/test_registry.py

from owlroost.guide.registry import (
    GuideRegistry,
)
from owlroost.guide.specs import (
    GuideSpec,
)


def test_register_single_guide():
    reg = GuideRegistry()

    reg.register(
        GuideSpec(
            name="x",
            title="X",
            description="desc",
        )
    )

    guides = reg.all()

    assert len(guides) == 1

    assert guides[0].name == "x"


def test_registry_sorted_by_priority():
    reg = GuideRegistry()

    reg.register(
        GuideSpec(
            name="b",
            title="B",
            description="",
            priority=20,
        )
    )

    reg.register(
        GuideSpec(
            name="a",
            title="A",
            description="",
            priority=10,
        )
    )

    names = [guide.name for guide in reg.all()]

    assert names == [
        "a",
        "b",
    ]


def test_get_returns_registered_item():
    reg = GuideRegistry()

    guide = GuideSpec(
        name="hello",
        title="Hello",
        description="",
    )

    reg.register(
        guide,
    )

    assert reg.get("hello") is guide


def test_get_unknown_returns_none():
    reg = GuideRegistry()

    assert reg.get("missing") is None
