# src/owlroost/workspace/registry.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from collections.abc import Iterator

from owlroost.workspace.specs import (
    WorkspaceSpec,
)


class WorkspaceRegistry:
    """
    Registry of workspace observations.
    """

    def __init__(
        self,
    ):
        self._fields: dict[
            str,
            WorkspaceSpec,
        ] = {}

    def register(
        self,
        field: WorkspaceSpec,
    ):
        if field.name in self._fields:
            raise ValueError(f"Duplicate workspace field registered: {field.name}")

        self._fields[field.name] = field

    def get(
        self,
        name: str,
    ) -> WorkspaceSpec:
        return self._fields[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        return name in self._fields

    def all(
        self,
    ) -> list[WorkspaceSpec]:
        return [self._fields[name] for name in sorted(self._fields)]

    def items(
        self,
    ):
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
    ) -> Iterator[WorkspaceSpec]:
        return iter(
            self.all(),
        )
