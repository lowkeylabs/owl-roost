# src/owlroost/templates/library/households/minimum/household.py
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

import owlplanner as owl

from owlroost.workspace.owl_utils import (
    save_household,
)


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

    plan = owl.Plan(["Peter", "Wendy"], ["1962-01-15", "1965-01-16"], [89, 92], "minimum")

    plan.setAccountBalances(
        taxable=[90.5, 60],
        taxDeferred=[600.2, 150],
        taxFree=[50 + 20.6, 40.8],
        startDate="01-01",
    )

    plan.setAllocationRatios(
        "account",
        taxable=[[[60, 40, 0, 0], [70, 30, 0, 0]], [[60, 40, 0, 0], [80, 20, 0, 0]]],
        taxDeferred=[[[60, 40, 0, 0], [70, 30, 0, 0]], [[60, 40, 0, 0], [70, 30, 0, 0]]],
        taxFree=[[[100, 0, 0, 0], [100, 0, 0, 0]], [[50, 50, 0, 0], [60, 40, 0, 0]]],
    )

    plan.setSpendingProfile("flat")
    plan.setRates("conservative")

    options = {"bequest": 0}
    plan.solve("maxSpending", options=options)

    return plan


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

    plan.resolve()

    destination = Path(".").resolve()
    id = destination.parent.name

    case_file = destination / f"case_{id}.toml"

    hfp_file = destination / f"hfp_{id}.xlsx"

    save_household(
        plan,
        destination,
        case_file=case_file.name,
        hfp_file=hfp_file.name,
    )


if __name__ == "__main__":
    main()
