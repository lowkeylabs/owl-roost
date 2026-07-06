from owlroost.activity.bootstrap import (
    build_activity_registry,
)


def test_bootstrap_builds_registry():
    reg = build_activity_registry()

    guides = reg.all()

    assert len(guides) > 0


def test_workspace_provider_registered():
    reg = build_activity_registry()

    assert reg.get("workspace.initialize") is not None
