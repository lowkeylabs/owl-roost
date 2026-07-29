from __future__ import annotations


def test_roost_sections_registered(
    schema_registry,
):
    """
    At least one ROOST section field exists.
    """

    roost_fields = [
        f
        for f in schema_registry
        if getattr(
            f,
            "owner",
            None,
        )
        == "ROOST"
    ]

    assert roost_fields


def test_section_fields_have_paths(
    schema_registry,
):
    """
    Registered fields should carry paths.
    """

    for field in schema_registry:
        assert isinstance(
            field.path,
            tuple,
        )


# =========================================================
# Planning Checkpoint History
# =========================================================


def test_planning_checkpoint_fields_registered(
    schema_registry,
):
    """
    Planning cycle history fields should
    be registered.
    """

    names = {field.name for field in schema_registry}

    expected = {
        "history.planning_checkpoint.as_of",
        "history.planning_checkpoint.taxable_savings_balances",
        "history.planning_checkpoint.tax_deferred_savings_balances",
        "history.planning_checkpoint.tax_free_savings_balances",
        "history.planning_checkpoint.hsa_savings_balances",
        "history.planning_checkpoint.prior_12_months_essential_spending",
        "history.planning_checkpoint.prior_12_months_discretionary_spending",
    }

    assert expected <= names


def test_planning_checkpoint_paths(
    schema_registry,
):
    """
    Planning cycle history fields should
    have the expected runtime paths.
    """

    lookup = {field.name: field for field in schema_registry}

    assert lookup["history.planning_checkpoint.as_of"].path == (
        "history",
        "planning_checkpoint",
        "as_of",
    )

    assert lookup["history.planning_checkpoint.taxable_savings_balances"].path == (
        "history",
        "planning_checkpoint",
        "taxable_savings_balances",
    )


# =========================================================
# Tax Payment History
# =========================================================


def test_tax_payment_fields_registered(
    schema_registry,
):
    """
    Tax payment history fields should
    be registered.
    """

    names = {field.name for field in schema_registry}

    expected = {
        "history.tax_payment.date",
        "history.tax_payment.tax_year",
        "history.tax_payment.tax_type",
        "history.tax_payment.agency",
        "history.tax_payment.payment_type",
        "history.tax_payment.amount",
    }

    assert expected <= names


def test_tax_payment_paths(
    schema_registry,
):
    """
    Tax payment history fields should
    have the expected runtime paths.
    """

    lookup = {field.name: field for field in schema_registry}

    assert lookup["history.tax_payment.date"].path == (
        "history",
        "tax_payment",
        "date",
    )

    assert lookup["history.tax_payment.amount"].path == (
        "history",
        "tax_payment",
        "amount",
    )


# =========================================================
# History Ontology
# =========================================================


def test_history_fields_are_inputs(
    schema_registry,
):
    """
    History fields should be registered as
    canonical input variables.
    """

    history_fields = [field for field in schema_registry if field.name.startswith("history.")]

    assert history_fields

    for field in history_fields:
        assert field.owner == "ROOST"
        assert field.source == "input"
        assert field.semantic_domain == "history"
