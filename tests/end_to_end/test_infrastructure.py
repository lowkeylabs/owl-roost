from __future__ import annotations


def test_infrastructure(
    build_session,
    load_run_plan,
    load_trial_toml,
):
    """
    Verify the basic ROOST BUILD
    infrastructure survives the complete
    workspace-based end-to-end pipeline.

    The end-to-end fixture constructs an
    initialized temporary workspace and
    executes ROOST with that workspace as
    the current working directory.

    This test verifies:

        * session creation
        * run creation
        * HFP propagation
        * trial creation
        * command-line override application
        * OWL plan materialization
        * trial HFP references
    """

    session = build_session(
        "case_alex+jamie.toml",
        "roost_settings.trials_per_run=10",
        "rates_selection.method=historical_bootstrap",
    )

    # =====================================================
    # Session Structure
    # =====================================================

    assert session.is_dir()

    session_file = session / "session.toml"

    assert session_file.is_file()

    # =====================================================
    # Run Structure
    # =====================================================

    run0 = session / "run_0"

    assert run0.is_dir()

    run_file = run0 / "run.toml"

    assert run_file.is_file()

    # =====================================================
    # HFP Propagation
    # =====================================================

    run_hfp = run0 / "run-hfp.xlsx"

    assert run_hfp.is_file()

    # =====================================================
    # Trial Hierarchy
    # =====================================================

    trial_root = run0 / "trials"

    assert trial_root.is_dir()

    trials = sorted(path for path in trial_root.iterdir() if path.is_dir())

    assert len(trials) == 10

    trial0 = trial_root / "0000"

    assert trial0.is_dir()

    trial_file = trial0 / "trial.toml"

    assert trial_file.is_file()

    # =====================================================
    # Effective Run Configuration
    # =====================================================

    plan = load_run_plan(
        session,
        run_id=0,
    )

    #
    # This value originated as an explicit
    # command-line override and must survive:
    #
    #     command line
    #         ->
    #     build_hydra_command
    #         ->
    #     Hydra
    #         ->
    #     run.toml
    #         ->
    #     OWL Plan
    #

    assert plan.rateMethod == "historical_bootstrap"

    # =====================================================
    # Trial HFP Reference
    # =====================================================

    trial_dict = load_trial_toml(
        session,
        run_id=0,
        trial_id=0,
    )

    assert "household_financial_profile" in trial_dict

    hfp_name = trial_dict["household_financial_profile"]["HFP_file_name"]

    #
    # Trials live at:
    #
    #     run_0/trials/0000/
    #
    # while the copied HFP lives at:
    #
    #     run_0/run-hfp.xlsx
    #
    # Therefore the trial configuration
    # references the parent run HFP using
    # two parent traversals.
    #

    assert "../../run-hfp.xlsx" in hfp_name
