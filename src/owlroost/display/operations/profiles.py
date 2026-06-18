# src/owlroost/display/operations/profiles.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Display profile resolution.
"""

from __future__ import annotations

# =========================================================
# Profile Resolution
# =========================================================

# =========================================================
# Profile Resolution
# =========================================================


def resolve_display_profile(
    display_field,
    *,
    mode=None,
    profile=None,
):
    """
    Resolve active DisplayProfile.

    Resolution order
    ----------------

    1. Explicit profile request
    2. Profile matching mode
    3. Sole available profile
    4. Default profile

    Returns
    -------
    DisplayProfile

    The returned profile is fully
    materialized and contains all
    renderer-facing defaults.
    """

    profiles = display_field.profiles

    if not profiles:
        raise KeyError(f"{display_field.field_name}: no display profiles registered")

    # =====================================================
    # Explicit Profile
    # =====================================================

    if profile is not None:
        try:
            selected = profiles[profile]

        except KeyError as err:
            raise KeyError(f"{display_field.field_name}: profile '{profile}' not found") from err

    # =====================================================
    # Mode-Matched Profile
    # =====================================================

    elif mode is not None and mode in profiles:
        selected = profiles[mode]

    # =====================================================
    # Sole Profile
    # =====================================================

    elif len(profiles) == 1:
        selected = next(
            iter(
                profiles.values(),
            )
        )

    # =====================================================
    # Default Profile
    # =====================================================

    elif "default" in profiles:
        selected = profiles["default"]

    # =====================================================
    # Ambiguous
    # =====================================================

    else:
        raise KeyError(
            f"{display_field.field_name}: "
            f"unable to resolve profile "
            f"(mode={mode!r}, "
            f"profiles={list(profiles)})"
        )

    # =====================================================
    # Materialize Defaults
    # =====================================================

    return selected.__class__(
        label=selected.label,
        fmt=selected.fmt,
        label_align=(selected.label_align if selected.label_align is not None else "left"),
        content_align=(selected.content_align if selected.content_align is not None else "left"),
        width=selected.width,
        min_width=selected.min_width,
        max_width=selected.max_width,
        wrap=(selected.wrap if selected.wrap is not None else False),
        visible=(selected.visible if selected.visible is not None else True),
    )
