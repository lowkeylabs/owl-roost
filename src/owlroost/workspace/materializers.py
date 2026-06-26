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


def workspace_lookup(
    field_name: str,
) -> Callable:
    """
    Resolve workspace values from
    row["_workspace"].

    Example
    -------
    workspace.name

        -> _workspace.name

    workspace.paths.results

        -> _workspace.paths.results
    """

    path_parts = field_name.split(".")[1:]

    def compute_fn(
        row,
    ):
        value = row.get(
            "_workspace",
            {},
        )

        for part in path_parts:
            if not isinstance(
                value,
                dict,
            ):
                return None

            value = value.get(
                part,
            )

            if value is None:
                return None

        return value

    return compute_fn


def workspace_value(
    row,
    field_name,
):
    """
    Resolve a materialized workspace
    observation.

    Example
    -------

    workspace.is_initialized

        -> row["_workspace"]["is_initialized"]

    workspace.paths.results

        -> row["_workspace"]["paths"]["results"]
    """

    value = row.get(
        "_workspace",
        {},
    )

    parts = field_name.split(".")[1:]

    for part in parts:
        if not isinstance(
            value,
            dict,
        ):
            return None

        value = value.get(
            part,
        )

        if value is None:
            return None

    return value


# =========================================================
# Nested Assignment
# =========================================================


def _set_workspace_value(
    row,
    field_name,
    value,
):
    """
    Store a workspace observation
    into row["_workspace"].

    Example
    -------

    workspace.has_results

        -> _workspace["has_results"]

    workspace.paths.results

        -> _workspace["paths"]["results"]
    """

    current = row.setdefault(
        "_workspace",
        {},
    )

    parts = field_name.split(".")[1:]

    for part in parts[:-1]:
        current = current.setdefault(
            part,
            {},
        )

    current[parts[-1]] = value


def materialize_workspace(
    row,
    workspace_registry,
):
    """
    Materialize workspace observations.

    Writes values into:

        row["_workspace"]
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

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        _set_workspace_value(
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
    Materialize workspace observations as
    a presentation tree.

    Writes into:

        row["_workspace_tree"]
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
        "label": "Workspace",
        "children": [],
    }

    row["_workspace_tree"] = root

    #
    # Cache of section nodes so multiple
    # fields in the same group share the
    # same parent.
    #
    sections = {}

    for field in workspace_registry.all():
        if field.compute_fn is None:
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

        #
        # Everything except the leaf becomes
        # nested section nodes.
        #
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

        #
        # Leaf node.
        #
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
            "choice_templates": {},
        }

        templates = study_registry.choice_templates_for_scenario_family(
            scenario_family.name,
        )

        for template in templates:
            applicable = all(
                workspace_value(
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
                template_data["required_levers"][lever_name] = workspace_value(
                    row,
                    lever_name,
                )

            family["choice_templates"][template.name] = template_data

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

        templates = study_registry.choice_templates_for_scenario_family(
            scenario_family.name,
        )

        if templates:
            template_group = {
                "kind": "section",
                "label": "Choice Templates",
                "meta": {},
                "children": [],
            }

            for template in templates:
                applicable = all(
                    workspace_value(
                        row,
                        lever_name,
                    )
                    for lever_name in (template.required_levers)
                )

                template_section = {
                    "kind": "section",
                    "label": template.title,
                    "field": (f"choice_template.{template.name}"),
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
                                    "applicable": workspace_value(
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
