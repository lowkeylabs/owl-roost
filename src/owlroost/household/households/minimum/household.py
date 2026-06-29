# src/owlroost/household/households/minimum/household.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Minimum Household Project.

Notes
-----
This project represents the smallest valid
Household Project shipped with ROOST.

It serves as:

    * architectural example
    * regression fixture
    * documentation example

Future revisions will construct and return
an OWL Plan.

The executable specification intentionally
separates construction from serialization.

Conceptually:

    create_plan()
            ↓
         OWL Plan
            ↓
    write_household()
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def create_plan() -> Any:
    """
    Construct the canonical household.

    Notes
    -----
    Placeholder implementation.

    Future revisions will construct and
    return a fully configured OWL Plan.

    Returns
    -------
    Any
        Placeholder for an OWL Plan.
    """

    return None


def write_household(
    plan: Any,
    directory: Path = Path("."),
) -> None:
    """
    Write household artifacts.

    Parameters
    ----------
    plan
        Household Plan returned by
        ``create_plan()``.

    directory
        Destination directory.

    Notes
    -----
    Future revisions will serialize one
    or more household artifacts including:

    * case.toml
    * HFP.xlsx

    The minimum household intentionally
    provides only a placeholder
    implementation.
    """

    raise RuntimeError("write_household() has not yet been implemented.")


def main() -> None:
    """
    Execute the executable specification.

    Notes
    -----
    Running this module directly constructs
    the canonical household and writes the
    resulting household artifacts into the
    current working directory.
    """

    plan = create_plan()

    write_household(
        plan,
    )


if __name__ == "__main__":
    main()
