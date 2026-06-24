from owlroost.comparison.plugins.overrides import (
    comparison_lookup,
)


def test_comparison_lookup():
    row = {
        "_comparison": {
            "session": {
                "common_overrides": {
                    "solver": "MOSEK",
                },
            },
        },
    }

    fn = comparison_lookup(
        "session.common_overrides",
    )

    assert fn(
        row,
    ) == {
        "solver": "MOSEK",
    }


def test_comparison_lookup_missing():
    row = {}

    fn = comparison_lookup(
        "session.common_overrides",
    )

    assert (
        fn(
            row,
        )
        is None
    )
