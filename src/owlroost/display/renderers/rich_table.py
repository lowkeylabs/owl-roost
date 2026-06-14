# src/owlroost/display/renderers/rich_table.py
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

import textwrap

from rich import box
from rich.console import Console
from rich.table import Table

from owlroost.display.formatting import (
    format_value,
)

# =========================================================
# Rich Table Construction
# =========================================================


def build_rich_table(
    table,
):
    """
    Build Rich Table renderable from
    RoostTable.

    Returns
    -------
    rich.table.Table
    """

    rich_table = Table(
        box=box.HORIZONTALS,
        show_edge=False,
        show_lines=False,
    )

    # swap out this definition for the one above to get borders
    _rich_table_for_debugging = Table(
        box=box.SQUARE,
        show_edge=True,
        show_lines=True,
    )

    # =====================================================
    # Columns
    # =====================================================

    for col_idx, col in enumerate(
        table.columns,
    ):
        if col.content_align == "right":
            justify = "right"

        elif col.content_align == "center":
            justify = "center"

        else:
            justify = "left"

        rich_table.add_column(
            col.label,
            justify=justify,
            width=_resolve_column_width(
                table,
                col_idx,
            ),
            no_wrap=not col.wrap,
            overflow="fold",
            vertical="top",
        )

    # =====================================================
    # Rows
    # =====================================================

    for row_idx, row in enumerate(
        table.rows,
    ):
        row_meta = None

        if hasattr(
            table,
            "row_meta",
        ):
            if row_idx < len(
                table.row_meta,
            ):
                row_meta = table.row_meta[row_idx]

        # -------------------------------------------------
        # Blank spacer rows
        # -------------------------------------------------

        if all((c is None or c == "") for c in row):
            rich_table.add_row(*["" for _ in row])
            continue

        # -------------------------------------------------
        # Structural section rows
        # -------------------------------------------------

        if (
            isinstance(
                row_meta,
                dict,
            )
            and row_meta.get("kind") == "section"
        ):
            rich_table.add_row(*["" for _ in table.columns])

            cells = [row[0]]

            cells.extend(["" for _ in table.columns[1:]])

            rich_table.add_row(
                *cells,
                style="bold cyan",
            )

            continue

        formatted = []

        # -------------------------------------------------
        # Row style
        # -------------------------------------------------

        row_style = None

        if isinstance(
            row_meta,
            dict,
        ):
            if row_meta.get("dim"):
                row_style = "dim"

        # -------------------------------------------------
        # Row-level metadata
        # -------------------------------------------------

        row_wrap = False
        row_width = None

        if isinstance(
            row_meta,
            dict,
        ):
            meta_column = row_meta.get(
                "column",
            )

            if meta_column is not None:
                row_wrap = bool(
                    getattr(
                        meta_column,
                        "wrap",
                        False,
                    )
                )

                row_width = getattr(
                    meta_column,
                    "width",
                    None,
                )

        # -------------------------------------------------
        # Cells
        # -------------------------------------------------

        for col_idx, (
            value,
            column,
        ) in enumerate(
            zip(
                row,
                table.columns,
                strict=False,
            )
        ):
            fmt = column.fmt

            if row_meta is not None and col_idx > 0:
                if isinstance(
                    row_meta,
                    dict,
                ):
                    meta_column = row_meta.get(
                        "column",
                    )

                    if meta_column is not None:
                        fmt = meta_column.fmt

                else:
                    fmt = row_meta.fmt

            rendered = format_value(
                value,
                fmt,
            )

            if (
                col_idx > 0
                and row_wrap
                and row_width
                and isinstance(
                    rendered,
                    str,
                )
                and rendered
            ):
                rendered = _wrap_preserving_lines(rendered, row_width)

            formatted.append(
                rendered,
            )

        rich_table.add_row(
            *formatted,
            style=row_style,
        )

    return rich_table


# =========================================================
# Rendering
# =========================================================


def render_rich_table(
    table,
):
    """
    Render RoostTable using Rich.
    """

    console = Console()

    console.print(
        build_rich_table(
            table,
        )
    )

    return ""


# =========================================================
# Width Resolution
# =========================================================


def _measure_column_width(
    table,
    col_idx,
):
    """
    Return maximum rendered width
    observed in a column.
    """

    column = table.columns[col_idx]

    width = len(column.label or "")

    for row in table.rows:
        if col_idx >= len(row):
            continue

        value = row[col_idx]

        rendered = format_value(
            value,
            column.fmt,
        )

        if rendered is None:
            continue

        rendered = str(
            rendered,
        )

        for line in rendered.splitlines():
            width = max(
                width,
                len(line),
            )

    return width


def _resolve_column_width(
    table,
    col_idx,
):
    """
    Resolve effective Rich width
    from DisplayProfile settings.
    """

    column = table.columns[col_idx]

    width = column.width

    # Rich-managed sizing
    if width is None:
        return None

    # Fixed width
    if isinstance(
        width,
        int,
    ):
        return width

    # Auto width
    if width == "auto":
        width = _measure_column_width(
            table,
            col_idx,
        )

        if column.min_width is not None:
            width = max(
                width,
                column.min_width,
            )

        if column.max_width is not None:
            width = min(
                width,
                column.max_width,
            )

        return width

    return None


def _wrap_preserving_lines(
    text: str,
    width: int,
) -> str:
    parts = []

    for line in text.splitlines():
        if not line:
            parts.append("")
            continue

        wrapped = textwrap.wrap(
            line,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )

        parts.extend(wrapped)

    return "\n".join(parts)
