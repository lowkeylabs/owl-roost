from __future__ import annotations

from owlroost.schema.sweeps import (
    expand_cli_overrides,
)

# =========================================================
# Pass-through
# =========================================================


def test_ss_age_pair_single_pair():
    """
    A single Social Security age pair
    does not require Hydra sweep expansion.
    """

    overrides = [
        "roost_sweeps.ss_age_pair=69-67",
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == overrides


def test_non_sweep_override_passthrough():
    """
    Non-sweep overrides are not modified.
    """

    overrides = [
        "solver_options.bequest=100",
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == overrides


def test_ss_age_pair_multiple_pairs_passthrough():
    """
    Explicit multiple Social Security age
    pairs remain a single Hydra override.
    """

    overrides = [
        "roost_sweeps.ss_age_pair=64-64,67-67,70-70",
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == overrides


# =========================================================
# Integer Range Expansion
# =========================================================


def test_ss_age_pair_range_first():
    """
    A range on the first spouse expands
    into independent Hydra choices.
    """

    overrides = [
        "roost_sweeps.ss_age_pair=range(62,64)-67",
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == [
        "roost_sweeps.ss_age_person0=62,63,64",
        "roost_sweeps.ss_age_person1=67",
    ]


def test_ss_age_pair_range_second():
    """
    A range on the second spouse expands
    into independent Hydra choices.
    """

    overrides = [
        "roost_sweeps.ss_age_pair=67-range(62,64)",
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == [
        "roost_sweeps.ss_age_person0=67",
        "roost_sweeps.ss_age_person1=62,63,64",
    ]


def test_ss_age_pair_cartesian():
    """
    Ranges on both spouses become two
    independent Hydra sweep dimensions.
    """

    overrides = [
        ("roost_sweeps.ss_age_pair=range(62,63)-range(65,66)"),
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == [
        "roost_sweeps.ss_age_person0=62,63",
        "roost_sweeps.ss_age_person1=65,66",
    ]


# =========================================================
# Fractional Range Expansion
# =========================================================


def test_ss_age_pair_monthly():
    """
    A monthly range expands into explicit
    Hydra choices.
    """

    overrides = [
        ("roost_sweeps.ss_age_pair=range(62,62.25,1/12)-67"),
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == [
        ("roost_sweeps.ss_age_person0=62,62.083333,62.166667,62.25"),
        "roost_sweeps.ss_age_person1=67",
    ]


def test_ss_age_pair_both_monthly():
    """
    Monthly ranges for both spouses become
    independent Hydra sweep dimensions.
    """

    overrides = [
        ("roost_sweeps.ss_age_pair=range(62,62.25,1/12)-range(67,67.25,1/12)"),
    ]

    expanded = expand_cli_overrides(
        overrides,
    )

    assert expanded == [
        ("roost_sweeps.ss_age_person0=62,62.083333,62.166667,62.25"),
        ("roost_sweeps.ss_age_person1=67,67.083333,67.166667,67.25"),
    ]
