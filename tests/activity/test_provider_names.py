from owlroost.activity.bootstrap import (
    build_activity_registry,
)


def test_registered_names_are_unique():
    reg = build_activity_registry()

    names = [activity.name for activity in reg.all()]

    assert len(names) == len(set(names))
