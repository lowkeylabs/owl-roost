# src/owlroost/workspace/levers/context.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Planning context levers.

Notes
-----
Context levers describe the current
planning environment rather than a
particular initialized workspace.

A planning context always exists.

Context answers:

    * Where am I?
    * What planning artifacts exist?
    * What workflows are available?

Inventory is represented primarily
using counts rather than booleans.
Workflow readiness remains semantic.
"""

from __future__ import annotations

from functools import cache
from io import StringIO
from pathlib import Path
from typing import Any

from owlplanner.config.plan_bridge import config_to_plan
from owlplanner.config.toml_io import load_toml

from owlroost.catalog.ontology import (
    ONTOLOGY_DIMENSIONS,
    CatalogNodeType,
)
from owlroost.core.utils import (
    normalize_module_path,
)
from owlroost.workspace.specs import (
    WorkspaceSpec,
)

# =========================================================
# Ontology
# =========================================================

LEVER_ONTOLOGY: dict[str, Any] = dict(
    owner="ROOST",
    semantic_domain="planning",
    value_origin="roost-computed",
    projection_kind="canonical",
    analytic_kind="primary",
    materialization_level="context",
    node_type=CatalogNodeType.VARIABLE,
    defined_in=normalize_module_path(__file__),
)

# =========================================================
# Discovery Helpers
# =========================================================


def _root(root=".") -> Path:
    return Path(root)


def find_case_files(
    root=".",
):
    """
    Discover TOML files.

    workspace.toml is excluded.
    """

    root = _root(root)

    files = [
        p
        for p in Path(root).glob("*")
        if p.is_file() and p.name.lower().startswith("c") and p.name.lower().endswith(".toml")
    ]

    return sorted(files)


@cache
def is_valid_case(filename: Path | None = None):
    if None:
        return False

    plan = None
    try:
        s = StringIO()
        logstreams = [s, s]
        toml_path = str(filename)
        diconf, dirname, _ = load_toml(toml_path)
        plan = config_to_plan(diconf, dirname=dirname, logstreams=logstreams)

    except Exception:
        plan = None

    return plan is not None


@cache
def find_valid_case_files(root="."):
    files = find_case_files(root)
    valid_files = [h for h in files if is_valid_case(h)]
    return valid_files


def find_hfp_files(
    root=".",
):
    """
    Discover Household Financial
    Profile workbooks.
    """

    root = _root(root)

    return sorted(
        root.glob("*.xlsx"),
    )


# =========================================================
# Inventory Counts
# =========================================================


def case_count(
    root=".",
):
    return len(find_case_files(root))


def valid_case_count(
    root=".",
):
    return len(find_valid_case_files(root))


# =========================================================
# Semantic Readiness
# =========================================================


def workspace_initialized(
    root=".",
):
    return (Path(root).resolve() / "workspace.toml").exists()


def has_valid_case(
    root=".",
):
    cases = find_valid_case_files(
        root,
    )

    return len(cases) >= 1


# =========================================================
# Lever Definitions
# =========================================================

LEVERS = [
    # ---------------------------------------------
    # Inventory
    # ---------------------------------------------
    dict(
        name="case_count",
        dtype=int,
        analytic_kind="primary",
        compute_fn=case_count,
        description="Count of OWL case files in planning context.",
    ),
    dict(
        name="valid_case_count",
        dtype=int,
        analytic_kind="primary",
        compute_fn=valid_case_count,
        description="Count of loadable OWL case files in planning context.",
    ),
    # ---------------------------------------------
    # Workflow readiness
    # ---------------------------------------------
    dict(
        name="workspace_initialized",
        dtype=bool,
        analytic_kind="primary",
        compute_fn=workspace_initialized,
        description="Planning context is an initialized workspace.",
    ),
    dict(
        name="has_valid_case",
        dtype=bool,
        analytic_kind="derived",
        compute_fn=has_valid_case,
        description="Planning context contains at least one valid case.",
    ),
]

# =========================================================
# Registration
# =========================================================


def register_levers(
    reg,
):
    """
    Register planning context levers.
    """

    for lever in LEVERS:
        ontology = dict(LEVER_ONTOLOGY)

        for dimension in ONTOLOGY_DIMENSIONS:
            field = dimension.field_name

            if field in lever:
                ontology[field] = lever[field]

        reg.register(
            WorkspaceSpec(
                name=f"context.{lever['name']}",
                dtype=lever["dtype"],
                compute_fn=lambda row, fn=lever["compute_fn"]: fn(
                    row["_path"],
                ),
                description=lever["description"],
                **ontology,
            )
        )
