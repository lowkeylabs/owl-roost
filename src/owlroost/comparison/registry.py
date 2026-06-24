# src/owlroost/comparison/registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Comparison registry.

Notes
-----
Owns registration and lookup of
comparison observations.

Comparison observations describe
relationships between rows after
selection, filtering, grouping,
and comparison analysis.

Examples
--------

    comparison.session.common_overrides

    comparison.session.run_specific_overrides

    comparison.working_set.common_overrides

    comparison.working_set.run_specific_overrides

Architectural Invariant
-----------------------
Comparison fields are canonical
semantic definitions.

Computed comparison values are
materialized into:

    row["_comparison"]

at runtime.
"""

from __future__ import annotations

from collections.abc import Iterator

from owlroost.comparison.specs import (
    ComparisonSpec,
)


class ComparisonRegistry:
    """
    Registry of comparison observations.
    """

    def __init__(
        self,
    ):
        self._fields: dict[
            str,
            ComparisonSpec,
        ] = {}

    def register(
        self,
        field: ComparisonSpec,
    ):
        """
        Register comparison field.
        """

        if field.name in self._fields:
            raise ValueError(f"Duplicate comparison field registered: {field.name}")

        self._fields[field.name] = field

    def get(
        self,
        name: str,
    ) -> ComparisonSpec:
        """
        Lookup comparison field.
        """

        return self._fields[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Test field existence.
        """

        return name in self._fields

    def all(
        self,
    ) -> list[ComparisonSpec]:
        """
        Return all registered fields.
        """

        return [
            self._fields[name]
            for name in sorted(
                self._fields,
            )
        ]

    def items(
        self,
    ):
        """
        Iterate over registered fields.
        """

        for name in sorted(
            self._fields,
        ):
            yield (
                name,
                self._fields[name],
            )

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return name in self._fields

    def __len__(
        self,
    ):
        return len(
            self._fields,
        )

    def __iter__(
        self,
    ) -> Iterator[ComparisonSpec]:
        return iter(
            self.all(),
        )
