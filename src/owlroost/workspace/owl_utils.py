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

    return config_to_plan(
        diconf,
        dirname=dirname,
        logstreams=logstreams,
    )


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

    plan.resolve()

    return plan
