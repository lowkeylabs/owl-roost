# src/owlroost/display/materializers/materialize.py
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

from owlroost.display.explain import (
    build_explanation_cell,
)
from owlroost.display.operations.profiles import (
    resolve_display_profile,
)
from owlroost.display.operations.resolution import (
    resolve_display_field,
    resolve_field_value,
)
from owlroost.display.registry import DisplayRegistry
from owlroost.display.renderers.specs import (
    RoostTable,
    TableColumn,
)
from owlroost.display.specs import DisplayProfile

# =========================================================
# Entry Normalization
# =========================================================


def normalize_entry(
    entry,
):
    """
    Normalize all entry styles into dict form.

    Supported
    ---------

        "field_name"

        (
            "field_name",
            {
                "modes": ["pivot"],
                ...
            },
        )
    """

    # -----------------------------------------------------
    # Simple field
    # -----------------------------------------------------

    if isinstance(entry, str):
        return {
            "field": entry,
        }

    # -----------------------------------------------------
    # Section
    # -----------------------------------------------------

    if (
        isinstance(entry, tuple)
        and len(entry) == 2
        and entry[0] == "section"
        and isinstance(entry[1], str)
    ):
        return {
            "kind": "section",
            "label": entry[1],
            "level": 0,
        }

    # -----------------------------------------------------
    # Decorated field
    # -----------------------------------------------------

    if (
        isinstance(entry, tuple)
        and len(entry) == 2
        and isinstance(entry[0], str)
        and isinstance(entry[1], dict)
    ):
        field_name, metadata = entry

        spec = {
            "field": field_name,
        }

        spec.update(
            metadata,
        )

        return spec

    # -----------------------------------------------------
    # Tree
    # -----------------------------------------------------

    if (
        isinstance(entry, tuple)
        and len(entry) == 2
        and entry[0] == "tree"
        and isinstance(entry[1], dict)
    ):
        spec = {
            "kind": "tree",
        }

        spec.update(
            entry[1],
        )

        return spec

    raise ValueError(f"Unsupported entry: {entry}")


def normalize_entries(
    entries,
):
    """
    Normalize an expanded view into a list
    of entry specifications.
    """

    return [
        normalize_entry(
            entry,
        )
        for entry in entries
    ]


# =========================================================
# Tree resolver
# =========================================================


def resolve_tree_root(
    row,
    root,
):
    """
    Resolve symbolic tree roots.

    Examples
    --------

    study.scenario_families

        -> row["_study"]["scenario_families"]

    workspace.inventory

        -> row["_workspace"]["inventory"]
    """

    if root.startswith(
        "study.",
    ):
        value = row.get(
            "_study",
            {},
        )

        parts = root.split(".")[1:]

    elif root.startswith(
        "workspace.",
    ):
        value = row.get(
            "_workspace",
            {},
        )

        parts = root.split(".")[1:]

    else:
        raise ValueError(f"Unknown tree root: {root}")

    for part in parts:
        value = value.get(
            part,
            {},
        )

    return value


# =========================================================
# View Expansion
# =========================================================


def expand_entries(
    registry,
    entries,
    row=None,
):
    """
    Expand groups and runtime trees.

    Returns raw view entries.
    """

    out = []

    for entry in entries:
        #
        # Groups
        #

        if isinstance(entry, tuple) and len(entry) == 2 and entry[0] == "group":
            group = registry.get_group(
                entry[1],
            )

            out.extend(
                expand_entries(
                    registry,
                    group.entries,
                    row=row,
                )
            )

            continue

        #
        # Trees
        #

        if isinstance(entry, tuple) and len(entry) == 2 and entry[0] == "tree":
            if row is None:
                continue

            out.extend(
                expand_tree(
                    row,
                    entry[1],
                )
            )

            continue

        out.append(
            normalize_entry(
                entry,
            )
        )

    return out


# =========================================================
# Tree expansion
# =========================================================


def expand_tree(
    row,
    spec,
):
    """
    Expand a materialized tree into ordinary
    view entries.

    Sections may optionally own a display field.

    The returned list contains only ordinary
    view entries understood by the existing
    materializer.
    """

    root = spec["root"]

    depth = spec.get(
        "depth",
        99,
    )

    order = spec.get(
        "order",
        [],
    )

    label_override = spec.get("label", None)

    # -----------------------------------------------------
    # Resolve root
    # -----------------------------------------------------

    node = row

    for part in root.split("."):
        if not isinstance(
            node,
            dict,
        ):
            return []

        node = node.get(
            f"_{part}",
            node.get(
                part,
            ),
        )

        if node is None:
            return []

        #
        # Optional view-specific root label.
        #
        if label_override and isinstance(node, dict):
            node = dict(node)
            node["label"] = label_override

    entries = []

    # -----------------------------------------------------
    # Ordering helper
    # -----------------------------------------------------

    def ordered_children(
        children,
    ):
        if not order:
            return children

        lookup = {}

        for child in children:
            if not isinstance(
                child,
                dict,
            ):
                continue

            name = (
                child.get(
                    "label",
                    "",
                )
                .lower()
                .replace(
                    " ",
                    "_",
                )
            )

            lookup[name] = child

        ordered = []

        used = set()

        for name in order:
            child = lookup.get(
                name,
            )

            if child is None:
                continue

            ordered.append(
                child,
            )

            used.add(
                id(child),
            )

        ordered.extend(child for child in children if id(child) not in used)

        return ordered

    # -----------------------------------------------------
    # Recursive walk
    # -----------------------------------------------------

    def walk(
        node,
        level,
    ):
        if node is None or level > depth:
            return

        #
        # Lists
        #
        if isinstance(
            node,
            list,
        ):
            for child in node:
                walk(
                    child,
                    level,
                )

            return

        if not isinstance(
            node,
            dict,
        ):
            return

        kind = node.get(
            "kind",
        )

        # -------------------------------------------------
        # Section
        # -------------------------------------------------

        if kind == "section":
            meta = dict(
                node.get(
                    "meta",
                    {},
                )
            )

            meta["level"] = level

            #
            # If the section owns a field,
            # emit ONE field row rather than
            # a section followed by a field.
            #
            if "field" in node:
                meta.update(
                    {
                        "kind": "field",
                        "field": node["field"],
                        #
                        # Override the display
                        # label for this field.
                        #
                        "profiles": {
                            "pivot": {
                                "label": node.get(
                                    "label",
                                    "",
                                ),
                            },
                            "table": {
                                "label": node.get(
                                    "label",
                                    "",
                                ),
                            },
                        },
                    }
                )

                entries.append(
                    meta,
                )

            else:
                meta.update(
                    {
                        "kind": "section",
                        "label": node.get(
                            "label",
                            "",
                        ),
                    }
                )

                entries.append(
                    meta,
                )

        # -------------------------------------------------
        # Standalone field
        # -------------------------------------------------

        elif kind == "field":
            meta = dict(
                node.get(
                    "meta",
                    {},
                )
            )

            meta["level"] = level

            meta.update(
                {
                    "kind": "field",
                    "field": node["field"],
                }
            )

            entries.append(
                meta,
            )

        # -------------------------------------------------
        # Children
        # -------------------------------------------------

        children = list(
            node.get(
                "children",
                [],
            )
        )

        if order and level == 0:
            children = ordered_children(
                children,
            )

        for child in children:
            walk(
                child,
                level + 1,
            )

    walk(
        node,
        0,
    )

    return entries


# =========================================================
# Pivot Transform
# =========================================================


def pivot_table(
    table,
    registry: DisplayRegistry | None = None,
    explain_facets=None,
    catalog_index=None,
    visible_entries=None,
    show_header=True,
    title=None,
):
    """
    Flip rows/columns for pivot display.

    Notes
    -----
    Pivot rendering uses synthetic display
    fields:

        pivot_metric
        pivot_value
        pivot_explanation

    so pivot presentation participates in
    the normal display/profile system.
    """

    explain_enabled = bool(
        explain_facets,
    )

    visible_entries = visible_entries or []

    # =====================================================
    # Synthetic Pivot Profiles
    # =====================================================

    metric_profile = None
    value_profile = None
    explanation_profile = None

    if registry is not None:
        try:
            metric_profile = resolve_display_profile(
                registry.get_display_field(
                    "pivot_metric",
                ),
                mode="pivot",
            )
        except KeyError:
            pass

        try:
            value_profile = resolve_display_profile(
                registry.get_display_field(
                    "pivot_value",
                ),
                mode="pivot",
            )
        except KeyError:
            pass

        try:
            explanation_profile = resolve_display_profile(
                registry.get_display_field(
                    "pivot_explanation",
                ),
                mode="pivot",
            )
        except KeyError:
            pass

    # =====================================================
    # Pivot Columns
    # =====================================================

    new_columns = [
        TableColumn(
            key="pivot_metric",
            label=str(metric_profile.label if metric_profile else "Metric"),
            wrap=(metric_profile.wrap if metric_profile else True),
            content_align=(metric_profile.content_align if metric_profile else "left"),
            width=(metric_profile.width if metric_profile else 25),
            min_width=(metric_profile.min_width if metric_profile else None),
            max_width=(metric_profile.max_width if metric_profile else None),
        )
    ]

    for idx in range(
        len(
            table.rows,
        )
    ):
        new_columns.append(
            TableColumn(
                key=str(idx),
                label=(
                    getattr(
                        value_profile,
                        "label",
                        None,
                    )
                    or str(idx)
                ),
                wrap=getattr(
                    value_profile,
                    "wrap",
                    True,
                ),
                content_align=getattr(
                    value_profile,
                    "content_align",
                    "right",
                ),
                width=getattr(
                    value_profile,
                    "width",
                    80,
                ),
                min_width=getattr(
                    value_profile,
                    "min_width",
                    None,
                ),
                max_width=getattr(
                    value_profile,
                    "max_width",
                    None,
                ),
            )
        )

    if explain_enabled:
        new_columns.append(
            TableColumn(
                key="pivot_explanation",
                label=str(explanation_profile.label if explanation_profile else "Explanation"),
                width=(explanation_profile.width if explanation_profile else 50),
                wrap=(explanation_profile.wrap if explanation_profile else True),
                content_align=(
                    explanation_profile.content_align if explanation_profile else "left"
                ),
                min_width=(explanation_profile.min_width if explanation_profile else None),
                max_width=(explanation_profile.max_width if explanation_profile else None),
            )
        )

    # =====================================================
    # Legacy callers
    # =====================================================

    if not visible_entries:
        visible_entries = [
            {
                "kind": "field",
                "field": column.field_name,
            }
            for column in table.columns
        ]

    # =====================================================
    # Build pivot rows
    # =====================================================

    new_rows = []

    new_row_meta = []

    field_column = 0

    for entry in visible_entries:
        kind = entry.get(
            "kind",
            "field",
        )

        # -------------------------------------------------
        # Section rows
        # -------------------------------------------------

        if kind == "section":
            row = [
                entry.get(
                    "label",
                    "",
                )
            ]

            row.extend(["" for _ in table.rows])

            if explain_enabled:
                row.append(
                    "",
                )

            new_rows.append(
                row,
            )

            #
            # Preserve metadata exactly.
            #
            new_row_meta.append(
                dict(
                    entry,
                )
            )

            continue

        # -------------------------------------------------
        # Field rows
        # -------------------------------------------------

        column = table.columns[field_column]

        field_column += 1

        row = [
            column.label,
        ]

        row_values = []
        source_rows = []

        for row_index, original_row in enumerate(
            table.rows,
        ):
            value = original_row[field_column - 1]
            row.append(
                value,
            )
            row_values.append(
                value,
            )
            source_rows.append(table.row_meta[row_index]["row"])

        if explain_enabled:
            row.append(
                build_explanation_cell(
                    field_name=column.field_name,
                    registry=registry,
                    catalog_index=catalog_index,
                    explain_facets=explain_facets,
                    row=(source_rows[0] if source_rows else None),
                    row_values=row_values,
                )
            )

        new_rows.append(
            row,
        )

        meta = dict(
            entry,
        )

        meta["column"] = column

        new_row_meta.append(
            meta,
        )

    #    print("row_meta -----")
    #    from pprint import pprint
    #    pprint(new_row_meta)

    return RoostTable(
        columns=new_columns,
        rows=new_rows,
        row_meta=new_row_meta,
        show_header=show_header,
        title=title,
    )


# =========================================================
# Materialization
# =========================================================


def materialize_view(
    *,
    rows,
    registry,
    catalog_index=None,
    view_name,
    level="case",
    mode="table",
    explain_facets=None,
    show_header=True,
    title=None,
):
    """
    Materialize rows + view into a RoostTable.

    Responsibilities
    ----------------
    - resolve DisplayView
    - expand DisplayGroups
    - apply visibility rules
    - resolve DisplayFields
    - resolve row values
    - construct renderer-facing RoostTable

    Does NOT
    --------
    - render output
    - aggregate rows
    - discover rows
    """

    explain_facets = explain_facets or set()

    # =====================================================
    # Resolve View
    # =====================================================

    view = registry.get_view(
        level,
        view_name,
    )

    # =====================================================
    # Explain Requires Pivot
    # =====================================================

    if explain_facets and mode != "pivot":
        raise ValueError("--explain requires pivot mode")

    # =====================================================
    # Expand View
    # =====================================================

    expand_row = rows[0] if rows else []

    expanded_entries = expand_entries(
        registry,
        view.entries,
        row=expand_row,
    )

    normalized_entries = expanded_entries

    # =====================================================
    # Apply Visibility
    # =====================================================

    visible_entries = []

    for entry in normalized_entries:
        if entry.get("kind") == "section":
            visible_entries.append(
                entry,
            )
            continue

        modes = entry.get(
            "modes",
        )

        if modes is not None and mode not in modes:
            continue

        visible_entries.append(
            entry,
        )

    # =====================================================
    # Columns
    # =====================================================

    columns: list[TableColumn] = []

    # field_entries = [entry for entry in visible_entries if entry.get("kind") != "section"]

    field_entries = visible_entries

    for entry in field_entries:
        if entry.get("kind") == "section":
            continue

        field_name = entry["field"]

        display_field = resolve_display_field(
            registry,
            entry,
        )

        override = entry.get(
            "profiles",
            {},
        ).get(
            mode,
            {},
        )

        #
        # Registered DisplayField?
        #
        if display_field is None:
            profile = DisplayProfile()

        else:
            profile = resolve_display_profile(
                display_field,
                mode=mode,
            )

        column = TableColumn(
            key=field_name,
            field_name=field_name,
            label=override.get(
                "label",
                profile.label or field_name,
            ),
            label_align=override.get(
                "label_align",
                profile.label_align,
            ),
            content_align=override.get(
                "content_align",
                profile.content_align,
            ),
            fmt=override.get(
                "fmt",
                profile.fmt,
            ),
            width=override.get(
                "width",
                profile.width,
            ),
            wrap=override.get(
                "wrap",
                profile.wrap,
            ),
            display_field=display_field,
        )
        columns.append(column)
        entry["column"] = column

    # =====================================================
    # Rows
    # =====================================================

    materialized_rows = []

    row_meta = []

    for source_row in rows:
        materialized_row = []

        for entry in field_entries:
            if entry.get("kind") == "section":
                continue

            field_name = entry["field"]

            # display_field = resolve_display_field(
            #    registry,
            #    entry,
            # )
            # display_field was computed and stored above.  Reuse it.

            display_field = entry["column"].display_field

            value = resolve_field_value(
                row=source_row,
                field_name=field_name,
                display_field=display_field,
            )

            materialized_row.append(
                value,
            )

        materialized_rows.append(
            materialized_row,
        )

        meta = {
            "row": source_row,
        }

        if source_row.get(
            "_meta",
            {},
        ).get(
            "is_superseded",
        ):
            meta["dim"] = True

        row_meta.append(
            meta,
        )

    # =====================================================
    # Table
    # =====================================================

    table = RoostTable(
        columns=columns,
        rows=materialized_rows,
        row_meta=row_meta,
        show_header=show_header,
        title=title,
    )

    # =====================================================
    # Pivot
    # =====================================================

    if mode == "pivot":
        table = pivot_table(
            table,
            registry=registry,
            explain_facets=explain_facets,
            catalog_index=catalog_index,
            visible_entries=visible_entries,
            show_header=show_header,
            title=title,
        )

    return table
