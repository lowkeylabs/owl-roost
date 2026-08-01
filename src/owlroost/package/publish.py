# src/owlroost/package/publish.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Evidence package publisher.

Notes
-----
Publishes an EvidencePackage to disk.

The publisher owns filesystem
serialization only.

The EvidencePackage already contains
an ordered stream of Markdown
documents.

The publisher writes:

    * manifest.toml
    * evidence.qmd
    * Markdown documents
    * ZIP archive
"""

from __future__ import annotations

import shutil
from pathlib import Path

import tomlkit

# =========================================================
# Manifest
# =========================================================


def _write_manifest(
    package,
    destination: Path,
):
    """
    Write the package manifest.
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

    package_table.add(
        "documents",
        len(
            package.documents,
        ),
    )

    doc.add(
        "package",
        package_table,
    )

    (destination / "manifest.toml").write_text(
        tomlkit.dumps(
            doc,
        ),
        encoding="utf-8",
    )


# =========================================================
# Markdown documents
# =========================================================


def _write_documents(
    package,
    destination: Path,
):
    """
    Write Markdown documents.
    """

    for document in package.documents:
        (destination / document["filename"]).write_text(
            document["markdown"],
            encoding="utf-8",
        )


# =========================================================
# Quarto
# =========================================================


def _write_quarto(
    package,
    destination: Path,
):
    """
    Write the Quarto master
    document.

    The generated QMD simply
    includes each Markdown
    document in order.
    """

    lines = [
        "---",
        f'title: "{package.title}"',
        "format:",
        "  html: default",
        "  pdf: default",
        "toc: true",
        "number-sections: false",
        "---",
        "",
    ]

    for document in package.documents:
        lines.append("{{< include " + document["filename"] + " >}}")

        lines.append("")

    (destination / "evidence.qmd").write_text(
        "\n".join(
            lines,
        ),
        encoding="utf-8",
    )


# =========================================================
# ZIP archive
# =========================================================


def _create_zip(
    destination: Path,
):
    """
    Create a ZIP archive of the
    published evidence package.

    The archive contains the
    complete publication
    directory.
    """

    shutil.make_archive(
        str(destination),
        "zip",
        root_dir=destination,
    )


# =========================================================
# Publish
# =========================================================


def publish_evidence_package(
    package,
    output_dir: Path,
):
    """
    Publish an EvidencePackage.
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

    _write_documents(
        package,
        destination,
    )

    _write_quarto(
        package,
        destination,
    )

    _create_zip(
        destination,
    )

    return destination
