from __future__ import annotations

from owlroost.study.bootstrap import (
    build_study_registry,
)


def test_social_security_decision_applicable():
    reg = build_study_registry()

    row = {
        "_inputs": {
            "fixed_income": {
                "social_security_pia_amounts": [
                    2500,
                    0,
                ],
            },
        },
    }

    names = {
        d.name
        for d in reg.applicable_decisions(
            row,
        )
    }

    assert "social_security" in names


def test_social_security_decision_not_applicable():
    reg = build_study_registry()

    row = {
        "_inputs": {
            "fixed_income": {
                "social_security_pia_amounts": [
                    0,
                    0,
                ],
            },
        },
    }

    names = {
        d.name
        for d in reg.applicable_decisions(
            row,
        )
    }

    assert "social_security" not in names


def test_roth_conversion_decision_applicable():
    reg = build_study_registry()

    row = {
        "_inputs": {
            "savings_assets": {
                "tax_deferred_savings_balances": [
                    100_000,
                ],
            },
        },
    }

    names = {
        d.name
        for d in reg.applicable_decisions(
            row,
        )
    }

    assert "roth_conversion" in names


def test_roth_conversion_decision_not_applicable():
    reg = build_study_registry()

    row = {
        "_inputs": {
            "savings_assets": {
                "tax_deferred_savings_balances": [
                    0,
                ],
            },
        },
    }

    names = {
        d.name
        for d in reg.applicable_decisions(
            row,
        )
    }

    assert "roth_conversion" not in names
