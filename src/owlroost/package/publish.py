# src/owlroost/package/publish.py
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

from pathlib import Path

import tomlkit


def _write_manifest(
    package,
    destination: Path,
):
    """
    Write the package manifest.

    The manifest establishes the
    identity of the published
    evidence package.
    """

    doc = tomlkit.document()

    doc.add(
        "title",
        package.title,
    )

    doc.add(
        "generated_at",
        package.generated_at.isoformat(),
    )

    package_table = tomlkit.table()

    package_table.add(
        "format",
        1,
    )

    doc.add(
        "package",
        package_table,
    )

    workspace_table = tomlkit.table()

    workspace_table.add(
        "name",
        package.planning_context.workspace_name,
    )

    doc.add(
        "workspace",
        workspace_table,
    )

    (destination / "manifest.toml").write_text(
        tomlkit.dumps(doc),
        encoding="utf-8",
    )


def publish_evidence_package(
    package,
    output_dir: Path,
):
    """
    Publish an evidence package.
    """

    timestamp = package.generated_at.strftime(
        "%Y%m%d-%H%M%S",
    )

    destination = output_dir / timestamp

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_manifest(
        package,
        destination,
    )

    return destination
