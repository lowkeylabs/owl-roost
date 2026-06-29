# src/owlroost/household/registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Household registry.

Notes
-----
Owns registration and lookup of
Household Projects.

The registry provides the canonical
collection of Household Specifications
available to ROOST.

Architectural Invariants
------------------------

The registry owns:

    * Registration
    * Lookup
    * Enumeration

The registry does not own:

    * Filesystem discovery
    * Manifest parsing
    * Household construction
    * Filesystem inspection
    * Display row materialization

Filesystem discovery belongs to the
loaders.

Display row materialization belongs to
the loaders and display pipeline.

Household projects are registered
explicitly by bootstrap code.

Future Directions
-----------------

Future revisions may support:

* Multiple Household Libraries
* XDG search paths
* Dynamic discovery
* Provider capabilities
* Registry diagnostics
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
)

from owlroost.household.specs import (
    HouseholdSpec,
)


class HouseholdRegistry:
    """
    Registry of Household Projects.
    """

    def __init__(
        self,
    ) -> None:
        self._households: dict[
            str,
            HouseholdSpec,
        ] = {}

    # =====================================================
    # Registration
    # =====================================================

    def register_household(
        self,
        spec: HouseholdSpec,
    ) -> None:
        """
        Register a Household Project.

        Parameters
        ----------
        spec
            Household specification.

        Raises
        ------
        ValueError
            Duplicate household id.
        """

        if spec.id in self._households:
            raise ValueError(f"Duplicate household id: {spec.id}")

        self._households[spec.id] = spec

    def register_many(
        self,
        specs: Iterable[HouseholdSpec],
    ) -> None:
        """
        Register multiple households.
        """

        for spec in specs:
            self.register_household(
                spec,
            )

    # =====================================================
    # Lookup
    # =====================================================

    def has_household(
        self,
        household_id: str,
    ) -> bool:
        """
        Return True if a household is
        registered.
        """

        return household_id in self._households

    def get_household(
        self,
        household_id: str,
    ) -> HouseholdSpec:
        """
        Retrieve a registered household.

        Parameters
        ----------
        household_id
            Household identifier.

        Returns
        -------
        HouseholdSpec

        Raises
        ------
        KeyError
            Unknown household.
        """

        return self._households[household_id]

    # =====================================================
    # Enumeration
    # =====================================================

    def household_ids(
        self,
    ) -> tuple[str, ...]:
        """
        Return registered household ids
        in canonical order.
        """

        return tuple(
            sorted(
                self._households,
            )
        )

    def household_specs(
        self,
    ) -> tuple[HouseholdSpec, ...]:
        """
        Return registered Household
        Specifications in canonical
        order.
        """

        return tuple(self._households[household_id] for household_id in self.household_ids())

    # =====================================================
    # Container Protocol
    # =====================================================

    def __len__(
        self,
    ) -> int:
        """
        Return number of registered
        households.
        """

        return len(
            self._households,
        )

    def __contains__(
        self,
        household_id: object,
    ) -> bool:
        """
        Membership test by household id.
        """

        return (
            isinstance(
                household_id,
                str,
            )
            and household_id in self._households
        )

    def __iter__(
        self,
    ) -> Iterator[HouseholdSpec]:
        """
        Iterate over registered
        households in canonical order.
        """

        yield from self.household_specs()
