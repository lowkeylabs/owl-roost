# src/owlroost/review/service.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Review workflow service.

Notes
-----
Owns orchestration of retirement
planning workflows.

Architectural Invariant
-----------------------

Review owns sequence.

Review does NOT own analytical
knowledge.

Review composes capabilities from
other ROOST subsystems including:

    workspace
    study
    comparison
    results
    reports

The public methods of this module
are intended to become the common
Python interface used by:

    CLI
    Jupyter notebooks
    Quarto documents
    automated workflows
    future graphical interfaces

This module should remain free of
presentation logic.

Rendering belongs to the CLI or
other user interfaces.
"""

from __future__ import annotations

from pathlib import Path

from owlroost.workspace.checks import (
    has_household,
    has_valid_household,
    has_workspace,
)


class ReviewService:
    """
    Retirement review orchestration.

    Version 1 intentionally provides
    only a lightweight scaffold.

    Future versions will coordinate
    workspace checks, study levers,
    execution plans, evidence
    generation, reporting, and
    interpretation workflows.
    """

    def review(
        self,
        root: str | Path = ".",
    ) -> dict:
        """
        Perform a review of the
        current workspace.

        Parameters
        ----------
        root
            Starting directory.

        Returns
        -------
        dict
            Review observations.
        """

        root = Path(
            root,
        ).resolve()

        observations = {
            "root": root,
            # -------------------------------------
            # Workspace
            # -------------------------------------
            "has_workspace": has_workspace(
                root,
            ),
            # -------------------------------------
            # Household
            # -------------------------------------
            "has_household": has_household(
                root,
            ),
            "has_valid_household": has_valid_household(
                root,
            ),
            # -------------------------------------
            # Recommendation
            # -------------------------------------
            "next_step": None,
        }

        return observations

    def determine_next_step(
        self,
        observations: dict,
    ) -> str:
        """
        Determine the next recommended
        review activity.

        Notes
        -----
        Version 1 simply establishes
        the minimal prerequisites for
        a retirement planning review.

        Future versions will consider
        workspace state, review
        history, applicable studies,
        evidence, and calendar phase.
        """

        if not observations["has_household"]:
            return "Locate a household."

        if not observations["has_valid_household"]:
            return "Correct the household."

        if not observations["has_workspace"]:
            return "Initialize a workspace."

        return "Review complete."


def review(
    root: str | Path = ".",
) -> dict:
    """
    Convenience entry point.

    Provides the stable Python API
    used by the CLI, notebooks,
    Quarto documents, and future
    interfaces.
    """

    service = ReviewService()

    observations = service.review(
        root,
    )

    observations["next_step"] = service.determine_next_step(
        observations,
    )

    return observations
