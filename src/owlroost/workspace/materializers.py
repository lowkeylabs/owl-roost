# src/owlroost/workspace/materializers.py
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

from collections.abc import Callable


def row_lookup(
    field_name: str,
) -> Callable:
    """
    Resolve a materialized row value.

    Examples
    --------

    context.has_results
        -> row["_context"]["has_results"]

    workspace.identity.name
        -> row["_workspace"]["identity"]["name"]
    """

    namespace, *path_parts = field_name.split(".")

    root_name = f"_{namespace}"

    def compute_fn(row):
        value = row.get(root_name, {})

        for part in path_parts:
            if not isinstance(value, dict):
                return None

            value = value.get(part)

            if value is None:
                return None

        return value

    return compute_fn


def row_value(
    row,
    field_name,
):
    """
    Resolve a materialized row value.

    The first component of the field name
    selects the row namespace.

    Examples
    --------

    context.has_results

        -> row["_context"]["has_results"]

    workspace.identity.title

        -> row["_workspace"]["identity"]["title"]
    """

    namespace, *parts = field_name.split(".")

    value = row.get(
        f"_{namespace}",
        {},
    )

    for part in parts:
        if not isinstance(value, dict):
            return None

        value = value.get(part)

        if value is None:
            return None

    return value


# =========================================================
# Nested Assignment
# =========================================================


def _set_row_value(
    row,
    field_name,
    value,
):
    """
    Store a computed observation into
    the appropriate row namespace.

    Examples
    --------

    context.has_results

        -> row["_context"]["has_results"]

    workspace.identity.title

        -> row["_workspace"]["identity"]["title"]
    """

    namespace, *parts = field_name.split(".")

    current = row.setdefault(
        f"_{namespace}",
        {},
    )

    for part in parts[:-1]:
        current = current.setdefault(
            part,
            {},
        )

    current[parts[-1]] = value


def materialize_context(
    row,
    workspace_registry,
):
    """
    Materialize planning-context observations.

    Writes values into:

        row["_context"]

    Only variables within the
    'context.' namespace participate.
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    for field in workspace_registry.all():
        if field.compute_fn is None:
            continue

        if not field.name.startswith(
            "context.",
        ):
            continue

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        _set_row_value(
            row,
            field.name,
            value,
        )

    return row


def materialize_context_tree(
    row,
    workspace_registry,
):
    """
    Materialize planning-context observations
    as a presentation tree.

    Writes into:

        row["_context_tree"]

    Only variables within the
    'context.' namespace participate.
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    root = {
        "kind": "section",
        "label": "Planning Context",
        "children": [],
    }

    row["_context_tree"] = root

    #
    # Cache of section nodes so multiple
    # fields in the same group share the
    # same parent.
    #
    sections = {}

    for field in workspace_registry.all():
        if field.compute_fn is None:
            continue

        if not field.name.startswith(
            "context.",
        ):
            continue

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        parts = field.name.split(".")

        #
        # Skip the leading "context".
        #
        path = parts[1:]

        parent = root

        for part in path[:-1]:
            key = (
                id(parent),
                part,
            )

            section = sections.get(
                key,
            )

            if section is None:
                section = {
                    "kind": "section",
                    "label": (
                        part.replace(
                            "_",
                            " ",
                        ).title()
                    ),
                    "children": [],
                }

                parent["children"].append(
                    section,
                )

                sections[key] = section

            parent = section

        parent["children"].append(
            {
                "kind": "section",
                "label": (
                    path[-1]
                    .replace(
                        "_",
                        " ",
                    )
                    .title()
                ),
                "field": field.name,
                "value": value,
                "children": [],
            }
        )

    return row


def materialize_workspace(
    row,
    workspace_registry,
):
    """
    Materialize workspace observations.

    Writes values into:

        row["_workspace"]

    Only variables within the
    'workspace.' namespace participate.

    If the planning context does not
    contain an initialized workspace,
    no materialization occurs.
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    #
    # No initialized workspace.
    #
    if "_workspace" not in row:
        return row

    for field in workspace_registry.all():
        if field.compute_fn is None:
            continue

        if not field.name.startswith(
            "workspace.",
        ):
            continue

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        _set_row_value(
            row,
            field.name,
            value,
        )

    return row


def materialize_workspace_tree(
    row,
    workspace_registry,
):
    """
    Materialize workspace observations
    as a presentation tree.

    Writes into:

        row["_workspace_tree"]

    Only variables within the
    'workspace.' namespace participate.

    If the planning context does not
    contain an initialized workspace,
    no tree is generated.
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    #
    # No initialized workspace.
    #
    if "_workspace" not in row:
        return row

    root = {
        "kind": "section",
        "label": "Workspace",
        "children": [],
    }

    row["_workspace_tree"] = root

    #
    # Cache of section nodes so multiple
    # fields in the same group share
    # the same parent.
    #
    sections = {}

    for field in workspace_registry.all():
        if field.compute_fn is None:
            continue

        if not field.name.startswith(
            "workspace.",
        ):
            continue

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        parts = field.name.split(".")

        #
        # Skip the leading "workspace".
        #
        path = parts[1:]

        parent = root

        for part in path[:-1]:
            key = (
                id(parent),
                part,
            )

            section = sections.get(
                key,
            )

            if section is None:
                section = {
                    "kind": "section",
                    "label": (
                        part.replace(
                            "_",
                            " ",
                        ).title()
                    ),
                    "children": [],
                }

                parent["children"].append(
                    section,
                )

                sections[key] = section

            parent = section

        parent["children"].append(
            {
                "kind": "section",
                "label": (
                    path[-1]
                    .replace(
                        "_",
                        " ",
                    )
                    .title()
                ),
                "field": field.name,
                "value": value,
                "children": [],
            }
        )

    return row


# =========================================================
# Study Materialization
# =========================================================


def materialize_study(
    row,
    study_registry,
):
    """
    Materialize study information.

    Produces a semantic study model.

    Writes into:

        row["_study"]

    This structure intentionally contains
    no presentation information.

    Presentation trees are constructed
    later by materialize_study_tree().
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    study = row.setdefault(
        "_study",
        {},
    )

    study.clear()

    study["scenario_families"] = {}

    # -----------------------------------------------------
    # Scenario Families
    # -----------------------------------------------------

    for scenario_family in study_registry.all_scenario_families():
        family = {
            "name": scenario_family.name,
            "title": scenario_family.title,
            "description": (scenario_family.description),
            "experiments": {},
        }

        templates = study_registry.experiments_for_scenario_family(
            scenario_family.name,
        )

        for template in templates:
            applicable = all(
                row_value(
                    row,
                    lever_name,
                )
                for lever_name in (template.required_levers)
            )

            template_data = {
                "name": template.name,
                "title": template.title,
                "description": (template.description),
                "applicable": applicable,
                "required_levers": {},
            }

            for lever_name in template.required_levers:
                template_data["required_levers"][lever_name] = row_value(
                    row,
                    lever_name,
                )

            family["experiments"][template.name] = template_data

        study["scenario_families"][scenario_family.name] = family

    return row


def materialize_study_tree(
    row,
    study_registry,
):
    """
    Materialize study information.

    Produces a generic hierarchical tree
    suitable for tree expansion.

    Writes into:

        row["_study_tree"]
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    study = row.setdefault(
        "_study_tree",
        {},
    )

    study.clear()

    root = {
        "kind": "section",
        "label": "Scenario Families",
        "children": [],
    }

    study["scenario_families"] = root

    # -----------------------------------------------------
    # Scenario Families
    # -----------------------------------------------------

    for scenario_family in study_registry.all_scenario_families():
        family_section = {
            "kind": "section",
            "label": scenario_family.title,
            "field": (f"scenario_family.{scenario_family.name}"),
            "meta": {
                "blank_before": False,
            },
            "children": [],
        }

        templates = study_registry.experiments_for_scenario_family(
            scenario_family.name,
        )

        if templates:
            template_group = {
                "kind": "section",
                "label": "Experiments",
                "meta": {},
                "children": [],
            }

            for template in templates:
                applicable = all(
                    row_value(
                        row,
                        lever_name,
                    )
                    for lever_name in (template.required_levers)
                )

                template_section = {
                    "kind": "section",
                    "label": template.title,
                    "field": (f"experiment.{template.name}"),
                    "meta": {
                        "applicable": applicable,
                    },
                    "children": [],
                }

                if template.required_levers:
                    lever_group = {
                        "kind": "section",
                        "label": "Required Levers",
                        "meta": {},
                        "children": [],
                    }

                    for lever_name in template.required_levers:
                        label = lever_name.split(".")[-1].replace("_", " ").title()

                        lever_group["children"].append(
                            {
                                "kind": "section",
                                "label": label,
                                "field": lever_name,
                                "meta": {
                                    "applicable": row_value(
                                        row,
                                        lever_name,
                                    ),
                                },
                                "children": [],
                            }
                        )

                    template_section["children"].append(
                        lever_group,
                    )

                template_group["children"].append(
                    template_section,
                )

            family_section["children"].append(
                template_group,
            )

        root["children"].append(
            family_section,
        )

    return row
