from __future__ import annotations

from owlroost.schema.sweeps.ss_age_person0 import (
    materialize_override_to_canonical as materialize_person0,
)
from owlroost.schema.sweeps.ss_age_person1 import (
    materialize_override_to_canonical as materialize_person1,
)

# =========================================================
# End-to-End Sweep Materialization
# =========================================================


def test_materialize_ss_age_pair(
    build_session,
    load_run_plan,
):
    """
    Verify ss_age_pair materialization
    survives the complete workspace-based
    BUILD pipeline.

    The command-line sweep override must
    survive:

        command line
            ->
        build_hydra_command
            ->
        Hydra
            ->
        canonical materialization
            ->
        run.toml
            ->
        OWL Plan
    """

    session = build_session(
        "case_alex+jamie.toml",
        "roost_sweeps.ss_age_pair=69.0-69.25",
        "roost_settings.trials_per_run=10",
        "rates_selection.method=historical_bootstrap",
    )

    plan = load_run_plan(
        session,
        run_id=0,
    )

    assert plan.ssecAges.tolist() == [
        69.0,
        69.25,
    ]


def test_materialize_regime(
    build_session,
    load_run_plan,
):
    """
    Verify named-window materialization
    survives the complete workspace-based
    BUILD pipeline.
    """

    from owlroost.schema.sweeps.named_window import (
        MARKET_REGIMES,
    )

    regime = "stagflation"

    session = build_session(
        "case_alex+jamie.toml",
        "rates_selection.method=bootstrap_sor",
        f"roost_sweeps.named_window={regime}",
    )

    plan = load_run_plan(
        session,
        run_id=0,
    )

    assert plan.rateFrm == MARKET_REGIMES[regime][0]

    assert plan.rateTo == MARKET_REGIMES[regime][1]


def test_materialize_rates_from_to(
    build_session,
    load_run_plan,
):
    """
    Verify rates_from_to materialization
    survives the complete workspace-based
    BUILD pipeline.
    """

    session = build_session(
        "case_alex+jamie.toml",
        "rates_selection.method=bootstrap_sor",
        "roost_sweeps.rates_from_to=1928-2020",
    )

    plan = load_run_plan(
        session,
        run_id=0,
    )

    assert plan.rateFrm == 1928
    assert plan.rateTo == 2020


def test_materialize_optimization_goal(
    build_session,
    load_run_plan,
):
    """
    Verify optimization_goal
    materialization survives the complete
    workspace-based BUILD pipeline.
    """

    session = build_session(
        "case_alex+jamie.toml",
        "roost_sweeps.optimization_goal=maxBeq-100",
    )

    plan = load_run_plan(
        session,
        run_id=0,
    )

    assert plan.objective == "maxBequest"

    assert plan.solverOptions["netSpending"] == 100


# =========================================================
# Social Security Age Materializers
# =========================================================


def test_ss_age_person0_single_person():
    """
    Person0 sweep should materialize into a
    single-element SS age vector for a
    one-person household.
    """

    run_dict = {
        "basic_info": {
            "names": [
                "Joe",
            ],
        },
        "roost_sweeps": {
            "ss_age_person0": 62,
        },
    }

    materialize_person0(
        run_dict,
    )

    assert run_dict["fixed_income"]["social_security_ages"] == [
        62.0,
    ]


def test_ss_age_person1_two_person():
    """
    Person1 sweep should populate the
    second SS age slot.
    """

    run_dict = {
        "basic_info": {
            "names": [
                "Alex",
                "Jamie",
            ],
        },
        "roost_sweeps": {
            "ss_age_person1": 67,
        },
    }

    materialize_person1(
        run_dict,
    )

    assert run_dict["fixed_income"]["social_security_ages"] == [
        None,
        67.0,
    ]


def test_ss_age_person0_preserves_existing_person1():
    """
    Person0 sweep should not overwrite an
    existing person1 age.
    """

    run_dict = {
        "basic_info": {
            "names": [
                "Alex",
                "Jamie",
            ],
        },
        "fixed_income": {
            "social_security_ages": [
                None,
                67.0,
            ],
        },
        "roost_sweeps": {
            "ss_age_person0": 62,
        },
    }

    materialize_person0(
        run_dict,
    )

    assert run_dict["fixed_income"]["social_security_ages"] == [
        62.0,
        67.0,
    ]


def test_ss_age_person1_preserves_existing_person0():
    """
    Person1 sweep should not overwrite an
    existing person0 age.
    """

    run_dict = {
        "basic_info": {
            "names": [
                "Alex",
                "Jamie",
            ],
        },
        "fixed_income": {
            "social_security_ages": [
                62.0,
                None,
            ],
        },
        "roost_sweeps": {
            "ss_age_person1": 67,
        },
    }

    materialize_person1(
        run_dict,
    )

    assert run_dict["fixed_income"]["social_security_ages"] == [
        62.0,
        67.0,
    ]


def test_ss_age_person1_single_person():
    """
    Person1 sweep should materialize slot 1
    even when household size is unknown.
    """

    run_dict = {
        "basic_info": {
            "names": [
                "Joe",
            ],
        },
        "roost_sweeps": {
            "ss_age_person1": 67,
        },
    }

    materialize_person1(
        run_dict,
    )

    assert run_dict["fixed_income"]["social_security_ages"] == [
        None,
        67.0,
    ]
