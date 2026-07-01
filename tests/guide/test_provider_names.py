from owlroost.guide.bootstrap import (
    build_guide_registry,
)


def test_registered_names_are_unique():
    reg = build_guide_registry()

    names = [guide.name for guide in reg.all()]

    assert len(names) == len(set(names))
