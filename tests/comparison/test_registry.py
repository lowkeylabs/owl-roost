import pytest

from owlroost.comparison.registry import (
    ComparisonRegistry,
)
from owlroost.comparison.specs import (
    ComparisonSpec,
)


def test_register_field():
    reg = ComparisonRegistry()

    reg.register(
        ComparisonSpec(
            name="comparison.test",
        )
    )

    assert reg.exists(
        "comparison.test",
    )


def test_duplicate_registration_raises():
    reg = ComparisonRegistry()

    spec = ComparisonSpec(
        name="comparison.test",
    )

    reg.register(
        spec,
    )

    with pytest.raises(
        ValueError,
    ):
        reg.register(
            spec,
        )


def test_get_field():
    reg = ComparisonRegistry()

    spec = ComparisonSpec(
        name="comparison.test",
    )

    reg.register(
        spec,
    )

    assert (
        reg.get(
            "comparison.test",
        )
        is spec
    )


def test_len():
    reg = ComparisonRegistry()

    reg.register(
        ComparisonSpec(
            name="comparison.a",
        )
    )

    reg.register(
        ComparisonSpec(
            name="comparison.b",
        )
    )

    assert (
        len(
            reg,
        )
        == 2
    )


def test_contains():
    reg = ComparisonRegistry()

    reg.register(
        ComparisonSpec(
            name="comparison.a",
        )
    )

    assert "comparison.a" in reg

    assert "comparison.b" not in reg


def test_all_sorted():
    reg = ComparisonRegistry()

    reg.register(
        ComparisonSpec(
            name="comparison.z",
        )
    )

    reg.register(
        ComparisonSpec(
            name="comparison.a",
        )
    )

    names = [x.name for x in reg.all()]

    assert names == [
        "comparison.a",
        "comparison.z",
    ]
