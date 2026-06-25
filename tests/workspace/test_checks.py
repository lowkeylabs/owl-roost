# tests/workspace/test_checks.py


from owlroost.workspace.checks import (
    find_hfp_files,
    find_toml_files,
    has_cases,
    has_hfp,
    has_household,
    has_multiple_hfp,
    has_multiple_toml,
    has_reports,
    has_results,
    has_single_hfp,
    has_single_toml,
    has_toml,
    has_valid_household,
    has_workspace,
)

# =====================================================
# Discovery
# =====================================================


def test_find_toml_files_empty(
    tmp_path,
):
    assert (
        find_toml_files(
            tmp_path,
        )
        == []
    )


def test_find_toml_files_excludes_workspace(
    tmp_path,
):
    (tmp_path / "workspace.toml").write_text("")

    (tmp_path / "case.toml").write_text("")

    files = find_toml_files(
        tmp_path,
    )

    assert files == [
        tmp_path / "case.toml",
    ]


def test_find_hfp_files(
    tmp_path,
):
    (tmp_path / "abc.xlsx").write_text("")

    files = find_hfp_files(
        tmp_path,
    )

    assert files == [
        tmp_path / "abc.xlsx",
    ]


# =====================================================
# Workspace
# =====================================================


def test_has_workspace_false(
    tmp_path,
):
    assert not has_workspace(
        tmp_path,
    )


def test_has_workspace_true(
    tmp_path,
):
    (tmp_path / "workspace.toml").write_text("")

    assert has_workspace(
        tmp_path,
    )


# =====================================================
# Household discovery
# =====================================================


def test_has_household_none(
    tmp_path,
):
    assert not has_household(
        tmp_path,
    )


def test_has_household_single(
    tmp_path,
):
    (tmp_path / "case.toml").write_text("")

    assert has_household(
        tmp_path,
    )


def test_has_household_multiple(
    tmp_path,
):
    (tmp_path / "a.toml").write_text("")

    (tmp_path / "b.toml").write_text("")

    assert not has_household(
        tmp_path,
    )


def test_has_toml(
    tmp_path,
):
    (tmp_path / "case.toml").write_text("")

    assert has_toml(
        tmp_path,
    )


def test_has_single_toml(
    tmp_path,
):
    (tmp_path / "case.toml").write_text("")

    assert has_single_toml(
        tmp_path,
    )


def test_has_multiple_toml(
    tmp_path,
):
    (tmp_path / "a.toml").write_text("")

    (tmp_path / "b.toml").write_text("")

    assert has_multiple_toml(
        tmp_path,
    )


# =====================================================
# HFP discovery
# =====================================================


def test_has_hfp(
    tmp_path,
):
    (tmp_path / "case.xlsx").write_text("")

    assert has_hfp(
        tmp_path,
    )


def test_has_single_hfp(
    tmp_path,
):
    (tmp_path / "case.xlsx").write_text("")

    assert has_single_hfp(
        tmp_path,
    )


def test_has_multiple_hfp(
    tmp_path,
):
    (tmp_path / "a.xlsx").write_text("")

    (tmp_path / "b.xlsx").write_text("")

    assert has_multiple_hfp(
        tmp_path,
    )


# =====================================================
# Validation
# =====================================================


def test_has_valid_household_false_without_household(
    tmp_path,
):
    assert not has_valid_household(
        tmp_path,
    )


def test_has_valid_household_uses_validator(
    monkeypatch,
    tmp_path,
):
    (tmp_path / "case.toml").write_text("")

    called = False

    def fake_validate(
        path,
    ):
        nonlocal called

        called = True

        assert path == (tmp_path / "case.toml")

        return True

    monkeypatch.setattr(
        "owlroost.workspace.checks.validate_household",
        fake_validate,
    )

    assert has_valid_household(
        tmp_path,
    )

    assert called


# =====================================================
# Inventory
# =====================================================


def test_has_results(
    tmp_path,
):
    (tmp_path / "results").mkdir()

    assert has_results(
        tmp_path,
    )


def test_has_cases(
    tmp_path,
):
    (tmp_path / "cases").mkdir()

    assert has_cases(
        tmp_path,
    )


def test_has_reports(
    tmp_path,
):
    (tmp_path / "reports").mkdir()

    assert has_reports(
        tmp_path,
    )


def test_has_household_ignores_workspace_toml(
    tmp_path,
):
    (tmp_path / "workspace.toml").write_text("")

    (tmp_path / "case.toml").write_text("")

    assert has_household(
        tmp_path,
    )


def test_has_valid_household_ignores_workspace_toml(
    monkeypatch,
    tmp_path,
):
    (tmp_path / "workspace.toml").write_text("")

    (tmp_path / "case.toml").write_text("")

    monkeypatch.setattr(
        "owlroost.workspace.checks.validate_household",
        lambda _: True,
    )

    assert has_valid_household(
        tmp_path,
    )
