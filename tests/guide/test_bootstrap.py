from owlroost.guide.bootstrap import (
    build_guide_registry,
)


def test_bootstrap_builds_registry():
    reg = build_guide_registry()

    guides = reg.all()

    assert len(guides) > 0


def test_workspace_provider_registered():
    reg = build_guide_registry()

    assert reg.get("workspace.initialize") is not None
