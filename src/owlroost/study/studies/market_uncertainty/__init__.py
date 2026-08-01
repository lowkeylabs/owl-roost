# src/owlroost/study/studies/market_uncertainty/__init__.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Market Uncertainty study.

Notes
-----
This package contains all resources
required to define and publish the
Market Uncertainty study.

Contents include:

    * Study definition
    * Narrative Markdown
    * Figures and other static assets

The package directory itself is the
authoritative location for study
resources.

Publishers discover numbered Markdown
files and other assets directly from
``RESOURCE_DIR`` using filesystem
conventions.
"""

from __future__ import annotations

from pathlib import Path

from .definition import (
    register_studies,
)

# =========================================================
# Package Resources
# =========================================================

RESOURCE_DIR = Path(__file__).parent

__all__ = [
    "register_studies",
    "RESOURCE_DIR",
]
