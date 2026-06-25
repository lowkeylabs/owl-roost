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

        Notes
        -----
        Version 1 performs only
        minimal discovery.

        Future versions will
        progressively orchestrate
        additional review phases.
        """

        root = Path(root).resolve()

        observations = {
            "root": root,
            "workspace_found": False,
            "household_found": False,
            "next_step": None,
        }

        #
        # Future:
        #
        #   workspace.evaluate_checks(...)
        #
        #   study.evaluate_levers(...)
        #
        #   comparison.evaluate(...)
        #
        #   reports.evaluate(...)
        #

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
        Version 1 is intentionally
        simple.

        Future versions will use
        workspace state, study
        applicability, completed
        evidence, and calendar
        history.
        """

        if not observations["household_found"]:
            return "Locate a household (TOML/HFP)."

        if not observations["workspace_found"]:
            return "Initialize a workspace."

        return "Review complete."


def review(
    root: str | Path = ".",
) -> dict:
    """
    Convenience entry point.

    This function provides the
    stable Python API intended for
    notebooks, Quarto documents,
    and the command-line interface.
    """

    service = ReviewService()

    observations = service.review(
        root,
    )

    observations["next_step"] = service.determine_next_step(
        observations,
    )

    return observations
