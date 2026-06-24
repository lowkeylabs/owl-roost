def test_bootstrap_registers_override_fields(
    comparison_registry,
):
    expected = {
        "comparison.session.common_overrides",
        "comparison.session.run_specific_overrides",
        "comparison.working_set.common_overrides",
        "comparison.working_set.run_specific_overrides",
    }

    registered = {field.name for field in comparison_registry.all()}

    assert expected.issubset(
        registered,
    )
