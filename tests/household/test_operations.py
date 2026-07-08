# tests/household/test_operations.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Tests for Household operations.

Notes
-----
Verifies filesystem mutations
performed by Household operations.

The operations module owns semantic
lifecycle operations rather than
filesystem discovery.
"""

from __future__ import annotations

import pytest

from owlroost.household.operations import (
    create_household,
    delete_household,
    export_household,
    household_root,
    import_household,
    rename_household,
)
from owlroost.household.specs import (
    HouseholdSpec,
)

# =========================================================
# Helpers
# =========================================================


def test_household_root(
    writable_library,
):
    """
    Household roots are computed
    relative to the library.
    """

    assert household_root(
        writable_library,
        "smith",
    ) == (writable_library.root / "smith")


# =========================================================
# Creation
# =========================================================


def test_create_household(
    writable_library,
):
    """
    Creating a household creates
    the project directory.
    """

    root = create_household(
        writable_library,
        "smith",
    )

    assert root.is_dir()
    assert root.name == "smith"


def test_create_household_existing_raises(
    writable_library,
):
    """
    Existing households are not
    recreated.
    """

    create_household(
        writable_library,
        "smith",
    )

    with pytest.raises(
        FileExistsError,
    ):
        create_household(
            writable_library,
            "smith",
        )


def test_create_household_readonly_raises(
    readonly_library,
):
    """
    Read-only libraries reject
    creation.
    """

    with pytest.raises(
        PermissionError,
    ):
        create_household(
            readonly_library,
            "smith",
        )


# =========================================================
# Rename
# =========================================================


def test_rename_household(
    household,
):
    """
    Household projects may be
    renamed.
    """

    new_root = rename_household(
        household,
        "jones",
    )

    assert new_root.exists()
    assert new_root.name == "jones"
    assert not household.root.exists()


def test_rename_household_readonly_raises(
    readonly_library,
):
    """
    Read-only libraries reject
    renaming.
    """

    root = readonly_library.root / "smith"

    root.mkdir()

    household = HouseholdSpec(
        title="Smith",
        library=readonly_library,
        root=root,
    )

    assert household.id == "smith"

    with pytest.raises(
        PermissionError,
    ):
        rename_household(
            household,
            "jones",
        )


# =========================================================
# Deletion
# =========================================================


def test_delete_household(
    household,
):
    """
    Household projects may be
    removed.
    """

    delete_household(
        household,
    )

    assert not household.root.exists()


def test_delete_household_readonly_raises(
    readonly_library,
):
    """
    Read-only libraries reject
    deletion.
    """

    root = readonly_library.root / "smith"

    root.mkdir()

    household = HouseholdSpec(
        title="Smith",
        library=readonly_library,
        root=root,
    )

    assert household.id == "smith"

    with pytest.raises(
        PermissionError,
    ):
        delete_household(
            household,
        )


# =========================================================
# Placeholders
# =========================================================


def test_import_household_not_implemented(
    writable_library,
    tmp_path,
):
    """
    Import is reserved for future
    implementation.
    """

    with pytest.raises(
        NotImplementedError,
    ):
        import_household(
            tmp_path,
            writable_library,
        )


def test_export_household_not_implemented(
    household,
    tmp_path,
):
    """
    Export is reserved for future
    implementation.
    """

    with pytest.raises(
        NotImplementedError,
    ):
        export_household(
            household,
            tmp_path,
        )
