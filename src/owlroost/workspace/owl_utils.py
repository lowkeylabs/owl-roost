# src/owlroost/workspace/owl_utils.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
OWL workspace utilities.

Notes
-----
Provides thin wrappers around
native OWL functionality used by
the Workspace subsystem.

Architectural Invariant
-----------------------

This module owns ROOST's direct
interaction with OWL for household
loading and validation.

Other ROOST subsystems should call
these helpers rather than importing
OWL directly.

Responsibilities
----------------
* Load household TOML
* Construct OWL Plan
* Validate household inputs

Does NOT
---------
* Solve plans
* Execute runs
* Generate reports
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from loguru import logger
from owlplanner.config.plan_bridge import (
    config_to_plan,
)
from owlplanner.config.toml_io import (
    load_toml,
)


def load_household(
    toml_file,
):
    """
    Construct an OWL Plan from a
    household TOML.

    Parameters
    ----------
    toml_file
        Household TOML file.

    Returns
    -------
    owlplanner.Plan
    """

    toml_file = Path(
        toml_file,
    ).resolve()

    #
    # Suppress OWL logging.
    #

    stream = StringIO()

    logstreams = [
        stream,
        stream,
    ]

    logger.remove()

    logger.add(
        stream,
        level="WARNING",
    )

    #
    # Load TOML.
    #

    diconf, dirname, _ = load_toml(
        str(
            toml_file,
        ),
    )

    #
    # Construct Plan.
    #

    plan = config_to_plan(
        diconf,
        dirname=dirname,
        logstreams=logstreams,
        loadHFP=True,
    )

    return plan


def validate_household(
    toml_file,
):
    """
    Validate a household.

    Returns
    -------
    bool
        True if OWL successfully
        constructs a Plan.
    """

    try:
        load_household(
            toml_file,
        )

        return True

    except Exception:
        return False


def try_load_household(
    toml_file,
):
    """
    Attempt to construct a
    household.

    Returns
    -------
    tuple[Plan | None, Exception | None]
    """

    try:
        plan = load_household(
            toml_file,
        )

        return (
            plan,
            None,
        )

    except Exception as exc:
        return (
            None,
            exc,
        )


def resolve_household(
    toml_file,
):
    """
    Construct and resolve an
    OWL Plan.

    Returns
    -------
    owlplanner.Plan
    """

    plan = load_household(
        toml_file,
    )

    # plan.resolve()

    return plan


def save_household(
    plan,
    output_dir,
    *,
    case_file: str = "case_household.toml",
    hfp_file: str = "case_household.xlsx",
):
    """
    Write a resolved household
    into a household library.

    Parameters
    ----------
    plan
        OWL Plan.

    output_dir
        Destination directory.

    Returns
    -------
    pathlib.Path
        Output directory.
    """

    output_dir = Path(
        output_dir,
    ).resolve()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    #
    # Save household TOML.
    #

    plan.saveConfig(
        str(
            output_dir / case_file,
        )
    )

    #
    # Save resolved HFP.
    #

    plan.saveHFP(
        str(
            output_dir / hfp_file,
        )
    )

    return output_dir


def resolve_and_save_household(
    toml_file,
    output_dir,
    *,
    case_file: str = "case_household.toml",
    hfp_file: str = "case_household.xlsx",
):
    """
    Resolve a household and
    write the resulting
    household library entry.

    Parameters
    ----------
    toml_file
        Household TOML.

    output_dir
        Destination directory.

    case_file
        Destination TOML filename.

    hfp_file
        Destination HFP filename.

    Returns
    -------
    owlplanner.Plan
    """

    plan = resolve_household(
        toml_file,
    )

    save_household(
        plan,
        output_dir,
        case_file=case_file,
        hfp_file=hfp_file,
    )

    return plan


def save_resolved_household(
    plan,
    output_dir,
    *,
    case_file: str = "case_household.toml",
    hfp_file: str = "case_household.xlsx",
):
    """
    Resolve and save an
    existing OWL Plan.

    Parameters
    ----------
    plan
        OWL Plan.

    output_dir
        Destination directory.

    case_file
        Destination TOML filename.

    hfp_file
        Destination HFP filename.

    Returns
    -------
    pathlib.Path
        Output directory.
    """

    plan.resolve()

    return save_household(
        plan,
        output_dir,
        case_file=case_file,
        hfp_file=hfp_file,
    )
