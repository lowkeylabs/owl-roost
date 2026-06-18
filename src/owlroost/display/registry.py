# src/owlroost/display/registry.py
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

from owlroost.display.specs import (
    DisplayDashboard,
    DisplayField,
    DisplayGroup,
    DisplayView,
)
from owlroost.exceptions import (
    RoostError,
)


class DisplayRegistry:
    """
    Central registry for display-layer objects.

    Owns:

        - DisplayField
        - DisplayGroup
        - DisplayView

    DisplayRegistry owns presentation
    semantics layered atop canonical
    schema and metrics ontology.

    SchemaRegistry owns meaning.

    DisplayRegistry owns presentation.
    """

    # =====================================================
    # Construction
    # =====================================================

    def __init__(self):
        self._display_fields: dict[
            str,
            DisplayField,
        ] = {}

        self._groups: dict[
            str,
            DisplayGroup,
        ] = {}

        self._views: dict[
            tuple[str, str],
            DisplayView,
        ] = {}

        self._dashboards: dict[
            str,
            DisplayDashboard,
        ] = {}

    # =====================================================
    # Display Fields
    # =====================================================

    def _merge_display_profile(
        self,
        existing,
        incoming,
    ):
        """
        Merge two DisplayProfiles.

        Notes
        -----
        DisplayProfiles participate in
        overlay composition.

        Explicitly specified incoming
        values replace existing values.

        Unspecified (None) incoming
        values preserve the existing
        profile value.
        """

        return existing.__class__(
            label=(incoming.label if incoming.label is not None else existing.label),
            fmt=(incoming.fmt if incoming.fmt is not None else existing.fmt),
            label_align=(
                incoming.label_align if incoming.label_align is not None else existing.label_align
            ),
            content_align=(
                incoming.content_align
                if incoming.content_align is not None
                else existing.content_align
            ),
            width=(incoming.width if incoming.width is not None else existing.width),
            min_width=(
                incoming.min_width if incoming.min_width is not None else existing.min_width
            ),
            max_width=(
                incoming.max_width if incoming.max_width is not None else existing.max_width
            ),
            wrap=(incoming.wrap if incoming.wrap is not None else existing.wrap),
            visible=(incoming.visible if incoming.visible is not None else existing.visible),
        )

    def _merge_display_field(
        self,
        existing: DisplayField,
        incoming: DisplayField,
    ) -> DisplayField:
        profiles = dict(
            existing.profiles,
        )

        for (
            profile_name,
            incoming_profile,
        ) in incoming.profiles.items():
            if profile_name in profiles:
                profiles[profile_name] = self._merge_display_profile(
                    profiles[profile_name],
                    incoming_profile,
                )
            else:
                profiles[profile_name] = incoming_profile

        return DisplayField(
            field_name=existing.field_name,
            path=(incoming.path if incoming.path != incoming.field_name else existing.path),
            display_fn=(incoming.display_fn or existing.display_fn),
            catalog_declaration=(incoming.catalog_declaration or existing.catalog_declaration),
            profiles=profiles,
            description=(
                incoming.description if incoming.description is not None else existing.description
            ),
            defined_in=(
                incoming.defined_in if incoming.defined_in is not None else existing.defined_in
            ),
            notes=(incoming.notes if incoming.notes is not None else existing.notes),
        )

    def register_display_field(
        self,
        field: DisplayField,
    ):
        existing = self._display_fields.get(
            field.field_name,
        )

        if existing is None:
            self._display_fields[field.field_name] = field
            return

        self._display_fields[field.field_name] = self._merge_display_field(
            existing,
            field,
        )

    def get_display_field(
        self,
        field_name: str,
    ) -> DisplayField:
        """
        Lookup DisplayField.
        """

        try:
            return self._display_fields[field_name]

        except KeyError as err:
            raise KeyError(f"DisplayField not found: {field_name}") from err

    def has_display_field(
        self,
        field_name: str,
    ) -> bool:
        """
        Return True if field exists.
        """

        return field_name in self._display_fields

    def all_display_fields(
        self,
    ) -> list[DisplayField]:
        """
        Return all DisplayFields.
        """

        return list(self._display_fields.values())

    # -----------------------------------------------------
    # Compatibility Aliases
    # -----------------------------------------------------

    def all(
        self,
    ) -> list[DisplayField]:
        """
        Compatibility alias.

        Returns all display fields.
        """

        return self.all_display_fields()

    def get_all_display_fields(
        self,
    ) -> list[DisplayField]:
        return self.all_display_fields()

    # =====================================================
    # Groups
    # =====================================================

    def register_group(
        self,
        group: DisplayGroup,
    ):
        key = group.key

        if key in self._groups:
            raise ValueError(f"Duplicate DisplayGroup registered: {key}")

        self._groups[key] = group

    def get_group(
        self,
        key: str,
    ) -> DisplayGroup:
        try:
            return self._groups[key]

        except KeyError as err:
            raise KeyError(f"DisplayGroup not found: {key}") from err

    def has_group(
        self,
        key: str,
    ) -> bool:
        return key in self._groups

    def all_groups(
        self,
    ) -> list[DisplayGroup]:
        return list(self._groups.values())

    def get_all_groups(
        self,
    ) -> list[DisplayGroup]:
        return self.all_groups()

    # =====================================================
    # Group Expansion
    # =====================================================

    def expand_group(
        self,
        key: str,
    ) -> list[str]:
        """
        Expand a DisplayGroup into a flat
        ordered list of field names.

        Notes
        -----
        Expansion is recursive.

        Duplicate fields are removed while
        preserving first-seen ordering.

        Cyclic group references are rejected.
        """

        expanded: list[str] = []

        visited: set[str] = set()

        def _expand(
            group_key: str,
        ):
            if group_key in visited:
                raise ValueError(f"DisplayGroup cycle detected: {group_key}")

            visited.add(group_key)

            group = self.get_group(group_key)

            for entry in group.entries:
                # -----------------------------------------
                # Implicit field
                # -----------------------------------------

                if isinstance(
                    entry,
                    str,
                ):
                    if not self.has_display_field(entry):
                        raise ValueError(f"Unknown DisplayField: {entry}")

                    expanded.append(entry)

                    continue

                # -----------------------------------------
                # Explicit entry
                # -----------------------------------------

                if not isinstance(
                    entry,
                    tuple,
                ):
                    continue

                if len(entry) != 2:
                    raise ValueError(f"Invalid group entry: {entry}")

                kind, value = entry

                if kind == "field":
                    if not self.has_display_field(value):
                        raise ValueError(f"Unknown DisplayField: {value}")

                    expanded.append(value)

                elif kind == "group":
                    if not self.has_group(value):
                        raise ValueError(f"Unknown DisplayGroup: {value}")

                    _expand(value)

            visited.remove(group_key)

        _expand(key)

        seen: set[str] = set()

        unique: list[str] = []

        for field_name in expanded:
            if field_name in seen:
                continue

            seen.add(field_name)

            unique.append(field_name)

        return unique

    # =====================================================
    # Registry Names
    # =====================================================

    def all_field_names(
        self,
    ) -> list[str]:
        """
        Return all registered field names.
        """

        return sorted(self._display_fields.keys())

    def all_group_names(
        self,
    ) -> list[str]:
        """
        Return all registered group names.
        """

        return sorted(self._groups.keys())

    def all_view_keys(
        self,
    ) -> list[tuple[str, str]]:
        """
        Return all registered view keys.

        Returns
        -------
        [
            (level, name),
            ...
        ]
        """

        return sorted(self._views.keys())

    # =====================================================
    # Views
    # =====================================================

    def register_view(
        self,
        view: DisplayView,
    ):
        key = (
            view.level,
            view.name,
        )

        if key in self._views:
            raise ValueError(f"Duplicate DisplayView registered: {view.level}/{view.name}")

        self._views[key] = view

    def get_view(
        self,
        level: str,
        name: str,
    ) -> DisplayView:
        key = (
            level,
            name,
        )

        if key in self._views:
            return self._views[key]

        row_key = ("row", name)

        if row_key in self._views:
            return self._views[row_key]

        raise RoostError(f"DisplayView not found: {level}/{name}")

    def has_view(
        self,
        level: str,
        name: str,
    ) -> bool:
        return (
            level,
            name,
        ) in self._views

    def all_views(
        self,
    ) -> list[DisplayView]:
        return list(self._views.values())

    def get_all_views(
        self,
    ) -> list[DisplayView]:
        return self.all_views()

    def create_view(
        self,
        view: DisplayView,
    ):
        """
        Create a user-defined DisplayView.

        Intended for interactive workflows
        such as Jupyter notebooks and
        Quarto reports.

        Unlike register_view(), duplicate
        names raise a user-facing
        RoostError with actionable
        guidance.
        """

        key = (
            view.level,
            view.name,
        )

        if key in self._views:
            existing = sorted(v.name for v in self._views.values() if v.level == view.level)

            raise RoostError(
                "\n".join(
                    [
                        (f"View already exists: {view.level}/{view.name}"),
                        "",
                        "Choose a different view name.",
                        "",
                        f"Existing {view.level} views:",
                        "  " + ", ".join(existing),
                    ]
                )
            )

        self._views[key] = view

    # =====================================================
    # View Expansion
    # =====================================================

    def expand_view_fields(
        self,
        level: str,
        name: str,
    ) -> list[str]:
        """
        Expand fields referenced by a view.
        """

        view = self.get_view(
            level,
            name,
        )

        expanded: list[str] = []

        def expand_entries(
            entries,
        ):
            for entry in entries:
                if isinstance(
                    entry,
                    str,
                ):
                    if not self.has_display_field(entry):
                        raise ValueError(f"Unknown DisplayField: {entry}")

                    expanded.append(entry)

                elif isinstance(
                    entry,
                    tuple,
                ):
                    if len(entry) != 2:
                        continue

                    kind, value = entry

                    if kind == "field":
                        if not self.has_display_field(value):
                            raise ValueError(f"Unknown DisplayField: {value}")

                        expanded.append(value)

                    elif kind == "group":
                        expanded.extend(self.expand_group(value))

        expand_entries(view.entries)

        seen: set[str] = set()

        unique: list[str] = []

        for field_name in expanded:
            if field_name in seen:
                continue

            seen.add(field_name)

            unique.append(field_name)

        return unique

    # =====================================================
    # Dashboards
    # =====================================================

    def register_dashboard(
        self,
        dashboard: DisplayDashboard,
    ):
        """
        Register DisplayDashboard.
        """

        if dashboard.name in self._dashboards:
            raise ValueError(f"Duplicate DisplayDashboard registered: {dashboard.name}")

        self._dashboards[dashboard.name] = dashboard

    def get_dashboard(
        self,
        name: str,
    ) -> DisplayDashboard:
        """
        Lookup dashboard.
        """

        try:
            return self._dashboards[name]

        except KeyError as err:
            raise KeyError(f"DisplayDashboard not found: {name}") from err

    def has_dashboard(
        self,
        name: str,
    ) -> bool:
        return name in self._dashboards

    def all_dashboards(
        self,
    ) -> list[DisplayDashboard]:
        return list(self._dashboards.values())

    def get_all_dashboards(
        self,
    ) -> list[DisplayDashboard]:
        return self.all_dashboards()

    def all_dashboard_names(
        self,
    ) -> list[str]:
        return sorted(self._dashboards.keys())

    # =====================================================
    # Diagnostics
    # =====================================================

    def summary(
        self,
    ) -> dict:
        return {
            "display_fields": len(self._display_fields),
            "groups": len(self._groups),
            "views": len(self._views),
            "dashboards": len(self._dashboards),
        }

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
    ):
        """
        Validate registry integrity.
        """

        # -------------------------------------------------
        # Groups
        # -------------------------------------------------

        for group in self._groups.values():
            for entry in group.entries:
                if isinstance(
                    entry,
                    str,
                ):
                    if not self.has_display_field(entry):
                        raise ValueError(
                            f"Group '{group.key}' references unknown DisplayField: {entry}"
                        )

                elif isinstance(
                    entry,
                    tuple,
                ):
                    if len(entry) != 2:
                        raise ValueError(f"Invalid group entry in '{group.key}': {entry}")

                    kind, value = entry

                    if kind == "field":
                        if not self.has_display_field(value):
                            raise ValueError(
                                f"Group '{group.key}' references unknown DisplayField: {value}"
                            )

                    elif kind == "group":
                        if not self.has_group(value):
                            raise ValueError(
                                f"Group '{group.key}' references unknown DisplayGroup: {value}"
                            )

        # -------------------------------------------------
        # Views
        # -------------------------------------------------

        for view in self._views.values():
            for entry in view.entries:
                if not isinstance(
                    entry,
                    tuple,
                ):
                    continue

                if len(entry) != 2:
                    raise ValueError(f"Invalid view entry in {view.level}/{view.name}: {entry}")

                kind, value = entry

                if kind == "group":
                    if not self.has_group(value):
                        raise ValueError(
                            f"View {view.level}/{view.name} references unknown group: {value}"
                        )

                elif kind == "field":
                    if not self.has_display_field(value):
                        raise ValueError(
                            f"View {view.level}/{view.name} references unknown field: {value}"
                        )

        # -------------------------------------------------
        # Group Cycles
        # -------------------------------------------------

        for group_name in self.all_group_names():
            self.expand_group(group_name)

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):
        s = self.summary()

        return (
            f"DisplayRegistry("
            f"fields={s['display_fields']}, "
            f"groups={s['groups']}, "
            f"views={s['views']}, "
            f"dashboards={s['dashboards']}"
            f")"
        )

    # =====================================================
    # Convenience Aliases
    # =====================================================

    def expand_view(
        self,
        level: str,
        name: str,
    ) -> list[str]:
        """
        Convenience alias.

        Returns the fully expanded
        field list for a view.
        """

        return self.expand_view_fields(
            level,
            name,
        )

    def available_views(
        self,
        level,
    ):
        rows = []

        for (
            view_level,
            view_name,
        ), view in self._views.items():
            if view_level not in (
                level,
                "row",
            ):
                continue

            source = "?"

            if view.defined_in:
                source = Path(
                    view.defined_in,
                ).name

            rows.append(
                (
                    view_name,
                    source,
                )
            )

        return sorted(
            rows,
        )

    def has_view_for_level(
        self,
        level: str,
        name: str,
    ) -> bool:
        """
        Return True if view is available
        for level, including row fallback.
        """

        return (level, name) in self._views or ("row", name) in self._views
