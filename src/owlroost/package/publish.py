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


def publish_evidence_package(
    package,
    output_dir: Path,
):
    """
    Publish an evidence package.

    Current implementation creates
    a timestamped publication
    directory.
    """

    timestamp = package.generated_at.strftime(
        "%Y%m%d-%H%M%S",
    )

    destination = output_dir / timestamp

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Publishing evidence package to {destination}")

    return destination
