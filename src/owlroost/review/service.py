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

    print("nothing happening here yet!")
