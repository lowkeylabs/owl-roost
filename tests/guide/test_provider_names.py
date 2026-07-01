from owlroost.guide.bootstrap import (
    build_guide_registry,
)


def test_registered_names_are_unique():
    reg = build_guide_registry()

    names = [s.name for s in reg.suggestions()]

    assert len(names) == len(set(names))
