from owlroost.guide.bootstrap import (
    build_guide_registry,
)


def test_bootstrap_builds_registry():
    reg = build_guide_registry()

    suggestions = reg.suggestions()

    assert len(suggestions) > 0


def test_welcome_provider_registered():
    reg = build_guide_registry()

    assert reg.get("welcome") is not None


def test_workspace_provider_registered():
    reg = build_guide_registry()

    assert reg.get("workspace.initialize") is not None
