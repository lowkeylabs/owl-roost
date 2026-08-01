# src/owlroost/package/builder.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Evidence package builder.

Assembles an ordered stream of Markdown
documents representing the evidence
package.

The builder consumes the semantic study
model already materialized into the
planning context.

The builder owns:

    * loading static Markdown documents
    * generating dynamic Markdown tables
    * assembling the ordered document
      stream

The publisher later decides how those
documents are written to disk (directory,
zip, Quarto project, etc.).
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from owlroost.cli.utils import (
    render_table,
    resolve_renderer,
)
from owlroost.display.materializers.materialize import (
    materialize_view,
)

from .specs import (
    EvidencePackage,
)


def build_evidence_package(
    planning_context,
    run_rows,
    catalog,
):
    """
    Assemble an EvidencePackage.
    """

    studies = planning_context["_study"]["studies"]

    #
    # Determine which studies are represented
    # by the supplied run rows.
    #

    table = materialize_view(
        rows=run_rows,
        registry=catalog.display_registry,
        catalog_index=catalog.catalog_index,
        level="run",
        view_name="table_of_runs",
        mode="table",
        explain_facets=None,
    )

    #
    # Preserve encounter order while removing
    # duplicates.
    #

    study_names = list(dict.fromkeys(row[2] for row in table.rows))

    documents = []

    # =====================================================
    # Studies
    # =====================================================

    for study_name in study_names:
        study = studies[study_name]

        # ---------------------------------------------
        # Static markdown documents
        # ---------------------------------------------

        for document in study["documents"]:
            documents.append(
                {
                    "filename": document["filename"],
                    "markdown": Path(
                        document["path"],
                    ).read_text(
                        encoding="utf-8",
                    ),
                }
            )

        # ---------------------------------------------
        # Dynamic tables
        # ---------------------------------------------

        for view in study["run_row_views"]:
            table = materialize_view(
                rows=run_rows,
                registry=catalog.display_registry,
                catalog_index=catalog.catalog_index,
                level=view["level"],
                view_name=view["view"],
                mode=view.get(
                    "mode",
                    "table",
                ),
                explain_facets=view.get(
                    "explain_facets",
                ),
                show_header=True,
            )

            markdown = render_table(
                table,
                resolve_renderer(
                    markdown=True,
                    #                    color=False,
                ),
            )

            documents.append(
                {
                    "filename": (view["save_file"] + ".md"),
                    "markdown": markdown,
                }
            )

    #
    # Sort into narrative order.
    #

    documents.sort(
        key=lambda document: document["filename"],
    )

    return EvidencePackage(
        title="Retirement Planning Evidence",
        generated_at=datetime.now(),
        planning_context=None,
        documents=documents,
    )
