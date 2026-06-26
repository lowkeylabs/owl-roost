# src/owlroost/workspace/levers/workspace.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Workspace readiness levers.

Notes
-----
Defines semantic workspace levers
describing the readiness and
capabilities of a workspace.

Architectural Invariant
-----------------------

This module owns:

    * lever computation
    * lever metadata
    * catalog registration

These levers are reusable by:

    review
    study applicability
    question applicability
    scenario families
    choice templates
    future planners

Levers answer semantic questions.

They do NOT mutate the workspace.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from owlroost.catalog.ontology import (
    CatalogNodeType,
)
from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.workspace.owl_utils import (
    validate_household,
)
from owlroost.workspace.specs import (
    WorkspaceSpec,
)

# =========================================================
# Ontology
# =========================================================

WORKSPACE_LEVER: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="execution",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="workspace",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Discovery
# =========================================================


def find_household_files(
    root=".",
):
    """
    Discover household TOML files.

    Workspace metadata is excluded.
    """

    root = Path(root)

    return sorted(path for path in root.glob("*.toml") if path.name != "workspace.toml")


def find_hfp_files(
    root=".",
):
    """
    Discover HFP workbooks.
    """

    root = Path(root)

    return sorted(
        root.glob("*.xlsx"),
    )


# =========================================================
# Lever Implementations
# =========================================================


def has_workspace(
    root=".",
):
    root = Path(root)

    return (root / "workspace.toml").exists()


def is_initialized(
    root=".",
):
    return has_workspace(root)


def has_household(
    root=".",
):
    return len(find_household_files(root)) == 1


def has_valid_household(
    root=".",
):
    households = find_household_files(
        root,
    )

    if len(households) != 1:
        return False

    return validate_household(
        households[0],
    )


def has_cases(
    root=".",
):
    root = Path(root)

    return (root / "cases").exists()


def has_results(
    root=".",
):
    root = Path(root)

    return (root / "results").exists()


def has_reports(
    root=".",
):
    root = Path(root)

    return (root / "reports").exists()


# =========================================================
# Lever Definitions
# =========================================================

WORKSPACE_LEVERS = [
    dict(
        name="has_workspace",
        compute_fn=has_workspace,
        description=("Workspace definition file is present."),
    ),
    dict(
        name="is_initialized",
        compute_fn=is_initialized,
        description=("Workspace has been initialized."),
    ),
    dict(
        name="has_household",
        compute_fn=has_household,
        description=("Workspace contains exactly one household."),
    ),
    dict(
        name="has_valid_household",
        compute_fn=has_valid_household,
        description=("OWL successfully constructs a household plan."),
    ),
    dict(
        name="has_cases",
        compute_fn=has_cases,
        description=("Workspace contains a cases directory."),
    ),
    dict(
        name="has_results",
        compute_fn=has_results,
        description=("Workspace contains a results directory."),
    ),
    dict(
        name="has_reports",
        compute_fn=has_reports,
        description=("Workspace contains a reports directory."),
    ),
]

# =========================================================
# Registration
# =========================================================


def register_levers(
    reg,
):
    """
    Register workspace levers.
    """

    for lever in WORKSPACE_LEVERS:
        reg.register(
            WorkspaceSpec(
                name=f"workspace.levers.{lever['name']}",
                dtype=bool,
                compute_fn=lambda row, fn=lever["compute_fn"]: fn(
                    row["_path"],
                ),
                description=lever["description"],
                **WORKSPACE_LEVER,
            )
        )
