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

from owlroost.activity.materializers import materialize_activity, materialize_activity_trees
from owlroost.workspace.specs import (
    OverridePolicy,
)

# =========================================================
# Generic, nested lookup
# =========================================================

_MISSING = object()


def resolve_nested_value(
    mapping,
    parts,
    default=_MISSING,
):
    """
    Resolve a nested dictionary value.

    Parameters
    ----------
    mapping
        Root mapping.

    parts
        Sequence of path components.

    default
        Returned when any component
        is absent.

    Returns
    -------
    object
    """

    value = mapping

    for part in parts:
        if not isinstance(
            value,
            dict,
        ):
            return default

        if part not in value:
            return default

        value = value[part]

    return value


# =========================================================
# row lookups
# =========================================================


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
        return resolve_nested_value(
            row.get(
                root_name,
                {},
            ),
            path_parts,
            default=None,
        )

    return compute_fn


def row_value(
    row,
    field_name,
):
    """
    Resolve a materialized row value.

    Examples
    --------
    context.has_results

        -> row["_context"]["has_results"]

    workspace.identity.title

        -> row["_workspace"]["identity"]["title"]
    """

    namespace, *parts = field_name.split(".")

    return resolve_nested_value(
        row.get(
            f"_{namespace}",
            {},
        ),
        parts,
        default=None,
    )


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


def apply_configuration_override(
    row,
    field,
    value,
):
    """
    Apply persisted workspace
    configuration to a computed
    semantic observation.
    """

    if field.override_policy is OverridePolicy.NEVER:
        return value

    workspace = row.get(
        "_workspace",
    )

    if workspace is None:
        return value

    definition = workspace.get(
        "definition",
        {},
    )

    override = resolve_nested_value(
        definition,
        field.name.split("."),
    )

    if override is _MISSING:
        return value

    #
    # Replace the computed semantic value.
    #
    if field.override_policy is OverridePolicy.REPLACE:
        return override

    #
    # Recompute the semantic value from
    # the configured override.
    #
    if field.override_policy is OverridePolicy.RECOMPUTE:
        return field.compute_fn(
            row,
            override,
        )

    return value


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

        #
        # Only materialize primary fields.
        #
        #        if field.analytic_kind != "primary":
        #            continue

        try:
            value = field.compute_fn(
                row,
            )

        except Exception:
            continue

        value = apply_configuration_override(
            row,
            field,
            value,
        )

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

    The tree is built from the already
    materialized semantic context rather
    than recomputing observations.
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

    sections = {}

    for field in workspace_registry.all():
        if not field.name.startswith(
            "context.",
        ):
            continue

        value = row_value(
            row,
            field.name,
        )

        #
        # Variable was not materialized.
        #
        if value is None:
            continue

        path = field.name.split(".")[1:]

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

        value = apply_configuration_override(
            row,
            field,
            value,
        )

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

    The tree is built from the already
    materialized workspace model rather
    than recomputing observations.
    """

    level = row.get(
        "_meta",
        {},
    ).get(
        "level",
    )

    if level != "workspace":
        return row

    if "_workspace" not in row:
        return row

    root = {
        "kind": "section",
        "label": "Workspace",
        "children": [],
    }

    row["_workspace_tree"] = root

    sections = {}

    for field in workspace_registry.all():
        if not field.name.startswith(
            "workspace.",
        ):
            continue

        value = row_value(
            row,
            field.name,
        )

        #
        # Variable was not materialized.
        #
        if value is None:
            continue

        path = field.name.split(".")[1:]

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

    study["studies"] = {}

    # -----------------------------------------------------
    # Studies
    # -----------------------------------------------------

    for study_spec in study_registry.all_studies():
        study_data = {
            "name": study_spec.name,
            "title": study_spec.title,
            "description": study_spec.description,
            "experiments": {},
        }

        experiments = study_registry.experiments_for_study(
            study_spec.name,
        )

        for experiment in experiments:
            applicable = all(
                row_value(
                    row,
                    lever_name,
                )
                for lever_name in (experiment.required_levers)
            )

            experiment_data = {
                "name": experiment.name,
                "title": experiment.title,
                "description": (experiment.description),
                "applicable": applicable,
                "required_levers": {},
            }

            for lever_name in experiment.required_levers:
                experiment_data["required_levers"][lever_name] = row_value(
                    row,
                    lever_name,
                )

            study_data["experiments"][experiment.name] = experiment_data

        study["studies"][study_spec.name] = study_data

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
        "label": "Studies",
        "children": [],
    }

    study["studies"] = root

    # -----------------------------------------------------
    # Studies
    # -----------------------------------------------------

    for study_spec in study_registry.all_studies():
        study_section = {
            "kind": "section",
            "label": study_spec.title,
            "field": (f"study.{study_spec.name}"),
            "meta": {
                "blank_before": False,
            },
            "children": [],
        }

        experiments = study_registry.experiments_for_study(
            study_spec.name,
        )

        if experiments:
            experiment_group = {
                "kind": "section",
                "label": "Experiments",
                "meta": {},
                "children": [],
            }

            for experiment in experiments:
                applicable = all(
                    row_value(
                        row,
                        lever_name,
                    )
                    for lever_name in (experiment.required_levers)
                )

                experiment_section = {
                    "kind": "section",
                    "label": experiment.title,
                    "field": (f"experiment.{experiment.name}"),
                    "meta": {
                        "applicable": applicable,
                    },
                    "children": [],
                }

                if experiment.required_levers:
                    lever_group = {
                        "kind": "section",
                        "label": "Required Levers",
                        "meta": {},
                        "children": [],
                    }

                    for lever_name in experiment.required_levers:
                        label = (
                            lever_name.split(".")[-1]
                            .replace(
                                "_",
                                " ",
                            )
                            .title()
                        )

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

                    experiment_section["children"].append(
                        lever_group,
                    )

                experiment_group["children"].append(
                    experiment_section,
                )

            study_section["children"].append(
                experiment_group,
            )

        root["children"].append(
            study_section,
        )

    return row


# =========================================================
# Planning Context
# =========================================================


def materialize_planning_context(
    row,
    catalog,
):
    """
    Materialize a complete planning context.

    This computes every semantic namespace
    currently owned by ROOST.

    The input row is always a planning
    context. If the planning context
    contains an initialized workspace,
    workspace observations are also
    materialized.

    Parameters
    ----------
    row
        Planning context row.

    catalog
        CatalogContext returned by
        build_catalog_context().
    """

    #
    # Context
    #

    row = materialize_context(
        row,
        catalog.workspace_registry,
    )

    row = materialize_context_tree(
        row,
        catalog.workspace_registry,
    )

    #
    # Workspace
    #

    row = materialize_workspace(
        row,
        catalog.workspace_registry,
    )

    row = materialize_workspace_tree(
        row,
        catalog.workspace_registry,
    )

    #
    # Study
    #

    row = materialize_study(
        row,
        catalog.study_registry,
    )

    row = materialize_study_tree(
        row,
        catalog.study_registry,
    )

    #
    # Guide
    #

    row = materialize_activity(
        row,
        catalog.activity_registry,
    )

    row = materialize_activity_trees(
        row,
    )

    return row
