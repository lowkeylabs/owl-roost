# tests/household/conftest.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household test fixtures.

Notes
-----
Provides commonly used fixtures for the
Household subsystem test suite.

Architectural Invariants
------------------------

Tests should construct the Household
Registry through the public bootstrap
interface.

Tests should avoid constructing registry
internals directly whenever practical.
"""

from __future__ import annotations

import pytest

from owlroost.household.bootstrap import (
    build_household_registry,
)


@pytest.fixture
def registry():
    """
    Return a populated Household Registry.

    Returns
    -------
    HouseholdRegistry
    """

    return build_household_registry()
