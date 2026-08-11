# src/owlroost/templates/library/households/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Built-in Household Library.

Notes
-----
Identifies the built-in Household Library
distributed with ROOST.

Architectural Invariants
------------------------

This package owns the built-in household
library only.

It does not:

    * Discover household projects
    * Parse manifest files
    * Construct HouseholdSpec objects
    * Populate registries

Those responsibilities belong to the
household loaders and bootstrap modules.

Future Directions
-----------------

The built-in library should remain
structurally identical to user and
workspace household libraries.

A household library consists of one or
more Household Projects, each identified
by the presence of:

    manifest.toml

within the project directory.
"""

from __future__ import annotations

from pathlib import Path

# =========================================================
# Built-in Household Library
# =========================================================

BUILTIN_HOUSEHOLD_LIBRARY = Path(__file__).resolve().parent

__all__ = [
    "BUILTIN_HOUSEHOLD_LIBRARY",
]
