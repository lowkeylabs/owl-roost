# src/owlroost/workspace/checks.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace capability checks.

Notes
-----
Owns reusable predicates describing
the current state of a workspace.

Architectural Invariant
-----------------------

Checks answer questions.

Checks do NOT mutate the workspace.

Checks are intended for reuse by:

    workspace.operations
    review.service
    future notebooks
    future Quarto workflows

Validation should defer to OWL
whenever practical rather than
reimplementing OWL logic.
"""

from __future__ import annotations

from pathlib import Path

from owlroost.workspace.owl_utils import (
    validate_household,
)

# =========================================================
# Discovery
# =========================================================


def find_toml_files(
    root=".",
):
    """
    Discover household TOML files.

    Notes
    -----
    Workspace metadata files are
    excluded.
    """

    root = Path(root)

    return sorted(path for path in root.glob("*.toml") if path.name != "workspace.toml")


def find_hfp_files(
    root=".",
):
    """
    Discover HFP spreadsheets in
    the current directory.

    Returns
    -------
    list[Path]
    """

    root = Path(root)

    return sorted(
        root.glob("*.xlsx"),
    )


# =========================================================
# Workspace
# =========================================================


def has_workspace(
    root=".",
):
    """
    Does this directory contain a
    workspace?
    """

    root = Path(root)

    return (root / "workspace.toml").exists()


# =========================================================
# Household Discovery
# =========================================================


def has_toml(
    root=".",
):
    """
    Does at least one TOML exist?
    """

    return (
        len(
            find_toml_files(
                root,
            )
        )
        > 0
    )


def has_single_toml(
    root=".",
):
    """
    Exactly one TOML exists.
    """

    return (
        len(
            find_toml_files(
                root,
            )
        )
        == 1
    )


def has_multiple_toml(
    root=".",
):
    """
    More than one TOML exists.
    """

    return (
        len(
            find_toml_files(
                root,
            )
        )
        > 1
    )


def has_hfp(
    root=".",
):
    """
    Does at least one HFP exist?
    """

    return (
        len(
            find_hfp_files(
                root,
            )
        )
        > 0
    )


def has_single_hfp(
    root=".",
):
    """
    Exactly one HFP exists.
    """

    return (
        len(
            find_hfp_files(
                root,
            )
        )
        == 1
    )


def has_multiple_hfp(
    root=".",
):
    """
    More than one HFP exists.
    """

    return (
        len(
            find_hfp_files(
                root,
            )
        )
        > 1
    )


# =========================================================
# Household Validation
# =========================================================


def has_household(
    root=".",
):
    """
    Does this workspace contain
    exactly one household?

    Notes
    -----
    A household is currently
    represented by a single
    household TOML.
    """

    return has_single_toml(
        root,
    )


def has_valid_household(
    root=".",
):
    """
    Can OWL successfully construct
    a household Plan?

    Validation is delegated to
    native OWL functionality.
    """

    tomls = find_toml_files(
        root,
    )

    if len(tomls) != 1:
        return False

    return validate_household(
        tomls[0],
    )


# =========================================================
# Workspace Inventory
# =========================================================


def has_results(
    root=".",
):
    """
    Does the workspace contain a
    results directory?
    """

    root = Path(root)

    return (root / "results").exists()


def has_cases(
    root=".",
):
    """
    Does the workspace contain a
    cases directory?
    """

    root = Path(root)

    return (root / "cases").exists()


def has_reports(
    root=".",
):
    """
    Does the workspace contain a
    reports directory?
    """

    root = Path(root)

    return (root / "reports").exists()
